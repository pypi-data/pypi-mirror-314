import multiprocessing
import os
import threading

from sanic.config import Config

from nsanic.libs.consts import StaCode, GLOBAL_TZ
from nsanic.libs.rds_client import RdsClient
from nsanic.libs.mult_log import NLogger
from nsanic.libs.random_maker import RngMaker


class BaseConf(Config):
    __ins_lock = threading.Lock()
    __ins = None

    def __new__(cls, *args, **kwargs):
        with BaseConf.__ins_lock:
            if not hasattr(BaseConf, '_ins'):
                BaseConf._ins = Config.__new__(cls)
        return BaseConf._ins

    SERVER_NAME = 'MAIN'
    '''服务名称'''
    SERVER_ID = 'M0001'
    '''服务ID，建议4-6个字符 不同的服务之间该标识定义必须不一致'''
    RUN_PORT = 8800
    '''服务监听端口，不同的服务请使用不同的监听端口，否则无法启动'''
    RUN_WORKER = 1
    '''工作进程，该项配置可依据CPU核心数配置，最佳值为CPU核心数'''
    RUN_FAST = True
    HOST = '127.0.0.1'
    '''监听主机'''
    VER_CODE = None
    '''接口默认版本号'''
    DEBUG_MODE = False
    '''是否开启debug模式'''
    ACCESS_LOG = False
    '''是否开启access日志'''
    CHARSET = 'utf-8'
    '''全局字符集'''
    RESP_TYPE = 'JSON'
    USE_TZ = False
    '''数据库时区转化'''
    TIME_ZONE = GLOBAL_TZ
    '''时区配置'''
    REQUEST_TIMEOUT = 60
    '''	请求超时时间'''
    RESPONSE_TIMEOUT = 60
    '''响应超时时间'''
    FALLBACK_ERROR_FORMAT = 'json'
    '''错误响应格式'''
    FORWARDED_FOR_HEADER = 'X-Forwarded-For'
    '''代理IP或客户端IP请求头配置'''
    FORWARDED_SECRET = None
    '''用于安全识别特定的代理服务器'''
    GRACEFUL_SHUTDOWN_TIMEOUT = 30.0
    '''强制关闭非空闲连接的等待时间(秒)'''
    KEEP_ALIVE = True
    '''是否启用长连接'''
    KEEP_ALIVE_TIMEOUT = 30
    '''长连接超时时间'''
    REAL_IP_HEADER = 'X-Real-IP'
    '''客户端真实IP'''
    REGISTER = True
    '''是否应用程序注册'''
    REQUEST_BUFFER_QUEUE_SIZE = 10000
    '''请求缓存区队列大小'''
    REQUEST_ID_HEADER = 'X-Request-ID'
    '''请求头中的请求ID名称'''
    REQUEST_MAX_SIZE = 100000000
    '''Request 的最大字节数'''
    WEBSOCKET_MAX_SIZE = 2 ^ 20
    '''websocket 传入消息最大字节数'''
    WEBSOCKET_PING_INTERVAL = 30
    '''websocket ping 帧 发送间隔'''
    WEBSOCKET_PING_TIMEOUT = 20
    '''websocket pong 帧 响应超时时间'''

    CORS_AUTOMATIC_OPTIONS = True

    # 跨域访问允许的域名 * -- 所有域名
    ALLOW_ORIGIN = ['localhost']
    '''所允许的域'''
    ALLOW_METHOD = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    '''允许的请求方法'''
    ALLOW_HEADER = ['Authorization']
    '''允许的请求头'''
    ALLOW_CREDENTIALS = True
    '''是否允许携带cookie类验证信息'''
    ORIGIN_MAX_AGE = 300
    '''预检最大有效期'''

    PROCESSING_REQ = 'PROCESSING_REQUEST'
    '''当前正在处理的请求缓存KEY'''
    WS_ONLINE_INFO = 'WS_ONLINE_INFO'
    '''在线信息缓存key'''

    CHANNEL_SYSTEM = 'CHANNEL_SYSTEM_MSG'
    '''统一系统消息频道'''

    STA_CODE = StaCode
    '''指定的响应码对象'''

    # 日志基础路径
    LOG_PATH = os.path.join(os.getcwd(), 'logs')

    MODEL_LIST = ['main']
    '''数据库迁移基础表 更换配置请重写'''
    MODEL_EXTRA = ['extra']
    '''只用模型而不需要在当前项目迁移的表，请配置到该目录'''
    proc_name = ''

    # 默认Redis缓存配置 更换配置请重写
    CONF_RDS = {
        'default': {
            'host': '',
            'port': 6379,
            'password': '',
            'db': 1,
            # 'max_connections': 5,  # 最大连接数
            # 'decode_responses': True,  # 默认解析字符串，不解析默认为bytes类型
            'socket_connect_timeout': 5,  # 连接超时时长 s
        }
    }

    # tortoise-orm 默认数据库配置 更换配置请重写
    CONF_DB = {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': '',
                'port': '5432',
                'user': '',
                'password': '',
                'database': '',
            },
            'options': {
                'charset': 'utf8mb4',
                'minsize': 5,
                'maxsize': 20,
            }
        }
    }

    rng: RngMaker = None
    rds: RdsClient = None
    log: NLogger = NLogger

    @classmethod
    def set_conf(cls):
        cls.rng = RngMaker(cls.SERVER_ID)
        name = multiprocessing.current_process().name
        name_arr = name.split('-')
        proc_name = f"{name_arr[-2]}{name_arr[-1]}" if len(name_arr) >= 2 else name
        cls.proc_name = proc_name
        cls.log.init_conf(base_path=cls.LOG_PATH, folder=cls.SERVER_NAME.lower(), proc_split=1, proc_tab=cls.proc_name)
        if cls.CONF_RDS:
            cls.rds = RdsClient.init(cls.CONF_RDS['default'], logs=cls.log)

    @classmethod
    def makeup_db_conf(cls, model_list: list):
        """自定义分离式多库模式请重写该方法"""
        db_conf = {
            'apps': {cls.SERVER_NAME: {'models': model_list}},
            'connections': cls.CONF_DB,
            'use_tz': cls.USE_TZ if cls.TIME_ZONE else False
        }
        cls.USE_TZ and db_conf.update({'timezone': cls.TIME_ZONE})
        return db_conf

    @classmethod
    def db_conf(cls):
        """数据库配置"""
        models = cls.MODEL_LIST + cls.MODEL_EXTRA
        model_list = [f'{cls.SERVER_NAME}.model_db.{item}' for item in models]
        return cls.makeup_db_conf(model_list) if cls.CONF_DB else None

    @classmethod
    def migrate_db(cls):
        model_list = [f'{cls.SERVER_NAME}.model_db.{item}' for item in cls.MODEL_LIST]
        model_list.insert(0, 'aerich.models')
        return cls.makeup_db_conf(model_list)

    @classmethod
    def log_conf(cls):
        (not os.path.exists(cls.LOG_PATH)) and os.mkdir(cls.LOG_PATH)
        log_path = os.path.join(cls.LOG_PATH, cls.SERVER_NAME)
        (not os.path.exists(log_path)) and os.mkdir(log_path)
        mode = 'DEBUG' if cls.DEBUG_MODE else 'INFO'
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'console': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': os.path.join(log_path, 'run.log'),
                    'level': mode,
                    'formatter': 'generic',
                    'maxBytes': 1024 * 1024 * 200,
                    'backupCount': 5,
                    'encoding': 'utf-8'
                },
                'access': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': mode,
                    'formatter': 'access',
                    'filename': os.path.join(log_path, 'access.log'),
                    'maxBytes': 1024 * 1024 * 200,
                    'backupCount': 5,
                    'encoding': 'utf-8'
                },
                'error': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'ERROR',
                    'formatter': 'generic',
                    'filename': os.path.join(log_path, 'error.log'),
                    'maxBytes': 1024 * 1024 * 200,
                    'backupCount': 5,
                    'encoding': 'utf-8'
                },
            },
            'formatters': {
                "generic": {
                    "format": "%(asctime)s [%(process)s] [%(levelname)s] %(message)s",
                    "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
                },
                "access": {
                    "format": "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: "
                    + "%(request)s %(message)s %(status)s %(byte)s",
                    "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
                },
            },
            'loggers': {
                "sanic.root": {"level": "INFO", "handlers": ["console"]},
                "sanic.error": {
                    "handlers": ["error"],
                    "propagate": True,
                    "qualname": "sanic.error",
                },
                "sanic.access": {
                    "handlers": ["access"],
                    "propagate": True,
                    "qualname": "sanic.access",
                },
                "sanic.server": {
                    "handlers": ["console"],
                    "propagate": True,
                    "qualname": "sanic.server",
                },
            }
        }
