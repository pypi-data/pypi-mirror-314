from nsanic.base_conf import BaseConf
from nsanic.libs.mult_log import NLogger


class LogMeta:

    logs: NLogger = None

    @classmethod
    def logerr(cls, *err: str):
        cls.logs.error(*err) if cls.logs else print(*err)

    @classmethod
    def loginfo(cls, *info):
        cls.logs.info(*info) if cls.logs else print(*info)


class ConfMeta:

    conf = None

    @classmethod
    def logerr(cls, *err):
        cls.conf.log.error(*err) if (cls.conf and cls.conf.log) else print(*err)

    @classmethod
    def loginfo(cls, *info):
        cls.conf.log.info(*info) if (cls.conf and cls.conf.log) else print(*info)

    @classmethod
    def set_conf(cls, conf):
        cls.conf = conf


class BaseMeta:
    """基础配置依赖模型"""

    conf: BaseConf = None

    @property
    def rds(self):
        """缓存连接池"""
        return self.conf.rds

    @property
    def log(self):
        """文件日志"""
        return self.conf.log

    @property
    def rng(self):
        """随机值相关工具"""
        return self.conf.rng

    @property
    def sta_code(self):
        return self.conf.STA_CODE

    @classmethod
    def set_conf(cls, conf):
        cls.conf = conf
