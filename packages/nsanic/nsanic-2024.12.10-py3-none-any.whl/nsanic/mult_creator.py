import os
import random
import re
import string


def input_fun(check_fun, tips='请输入：'):
    while 1:
        item_val = input(tips)
        val = check_fun(item_val)
        if val:
            return val


def check_name(val: str):
    val = val.strip()
    if not val:
        print('必须指定服务名')
        return
    val = val.lower()
    if not re.match(r'^[a-z][a-z0-9_]*[a-z0-9]$', val):
        print('服务命名不符合规范，命名只能包含数字/字母/下划线，且不能以数字或下划线开头或结尾')
        return
    if val.find('__') != -1:
        print('服务命名不符合规范，命名不能包含空格或多个下划线')
        return
    return val


def check_id(val: str):
    val = val.strip()
    val = val.upper() if val else f"{''.join(random.sample(string.ascii_uppercase, 1))}{''.join(random.sample(string.digits, 4))}"
    if 3 <= len(val) <= 6 and re.match(r'^[A-Z][A-Z0-9]+[0-9]$', val):
        return val
    print('服务ID应是三到六位字母开头数字结尾组成的字符串，且应具有唯一性')


def check_db(val: str):
    val = val.strip()
    val = val.lower().strip() if val else 'y'
    if val in ('y', 'n'):
        return val
    print('是否使用数据库输入参数不符合规范，请输入y或n')


def check_m_list(val: str):
    val = val.strip()
    if not val:
        return ['main']
    val_list = val.split(';')
    new_list = []
    for v in val_list:
        v = check_name(v)
        if v:
            new_list.append(v)
        else:
            return
    return new_list


def check_redis(val: str):
    val = val.strip()
    val = val.lower() if val else 'y'
    if val in ('y', 'n'):
        return val
    print('是否使用redis缓存输入参数不符合规范，请输入y或n')


def check_port(val: str):
    val = val.strip()
    if not val:
        return 8888
    if val.isdigit() and (80 <= int(val) <= 65535):
        return int(val)
    print('输入的端口号应是数字类型且在80到65535之间')


def check_use_fast(val):
    val = val.strip()
    val = val.lower() if val else 'y'
    if val in ('y', 'n'):
        return val
    print('是否使用自动服务进程配置参数不符合规范，请输入y或n')


def check_ctrl_version(val):
    val = val.strip()
    val = val.lower() if val else 'n'
    if val == 'n':
        return 'n'
    if len(val) > 10:
        print('接口默认版本参数不能超过10个字符长度')
        return None
    if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9.]*[a-zA-Z0-9]$', val):
        return val
    print('是否使用接口版本控制参数只能在数字、大小写字母和点之间选择，并且已数字或字母开头、以及结尾')


engine_map = {
    '1': ('tortoise.backends.mysql', 'python -m pip install tortoise-orm[asyncmy]'),
    '2': ('tortoise.backends.asyncpg', 'python -m pip install tortoise-orm[asyncpg]'),
    # '3': ('tortoise.backends.aiosqlite', 'python -m pip install tortoise-orm[aiosqlite]'),
    # '4': ('tortoise.backends.asyncodbc', 'python -m pip install tortoise-orm[asyncodbc]'),
}


def check_use_engine(val):
    val = val.strip()
    if not val:
        return '2'
    if val in engine_map:
        return val
    print('无效的数据引擎指定')


service_map = {
    1: 'web',
    2: 'ws',
    3: 'srv',
}


def check_use_mode(val):
    val = val.strip()
    if not val:
        return 1
    if val in ('1', '2', '3'):
        return int(val)
    print('无效的服务模式指定')


def check_use_sub(val):
    val = val.strip()
    val = val.lower() if val else 'y'
    if val in ('y', 'n'):
        return val
    print('无效的websocket消息订阅模式')


def add_file(file_path: str, content=''):
    with open(file_path, 'w', encoding='utf-8') as f:
        if content:
            f.write(content)


def add_module(path: str, name: str, init_into=''):
    m_path = os.path.join(path, name)
    try:
        os.makedirs(m_path)
        add_file(os.path.join(m_path, '__init__.py'), content=init_into)
    except FileExistsError:
        print(f'指定的文件或目录已存在，不会重复创建：{m_path}')
        return
    return m_path


s_name = input_fun(check_name, tips='服务名称(建议小写并用下划线连接，长度不超过20字)：')
base_path = os.getcwd()
server_path = add_module(base_path, s_name)
if not server_path:
    raise FileExistsError('指定服务已存在，不能重复创建')
s_id = input_fun(check_id, tips='服务ID(三到六位，不区分大小写，默认随机)：')
use_db = input_fun(check_db, tips='是否使用数据库(y(默认)/n)：')
use_engine = input_fun(check_use_engine, tips='选择数据库存储引擎(1-mysql/2-pgsql(默认))：')
m_list = input_fun(check_m_list, tips='指定迁移模型文件名(多个用分号隔开，默认main)：')
o_list = input_fun(check_m_list, tips='指定不做迁移的模型文件名(多个用分号隔开，默认extra)：')
use_redis = input_fun(check_redis, tips='是否使用redis缓存(y(默认)/n,启用包含websocket的服务则该项自动设置为y)：')
port = input_fun(check_port, tips='服务运行端口号(80到65535之间的数字，默认8888)：')
use_fast = input_fun(check_use_fast, tips='是否自动配置服务进程(y(默认)/n)：')
use_ver = input_fun(check_ctrl_version, tips='接口版本版本控制(n(默认不启用)/数字字母或点的任意组合)：')
use_mode = input_fun(check_use_mode, tips='指定服务模式(1-http(默认),2-websocket,3-混合模式)：')
use_sub = 'y'
if use_mode in (2, 3):
    use_sub = input_fun(check_use_sub, tips='是否启用Websocket消息订阅模式(y(默认)/n)：')

dir_config = add_module(server_path, 'config')
dir_db = add_module(server_path, 'model_db')
dir_cache = add_module(server_path, 'model_rc')
dir_api = add_module(server_path, 'interface')
dir_handler = add_module(server_path, 'handler')
dir_script = add_module(server_path, 'script')

class_conf = f"ConfSrv"
db_val = None if use_db != 'y' else '''{
        'default': {
            'engine': '%s', 
            'credentials': {
                'host': '127.0.0.1', 
                'port': '5432', 
                'user': '', 
                'password': '', 
                'database': ''
            },
            'options': {
                'charset': 'utf8mb4', 
                'minsize': 5, 
                'maxsize': 30
            }
        }
    }''' % engine_map.get(use_engine)[0]
rds_val = None if (use_mode == 1) and use_redis != 'y' else '''{
        'default': {
            'host': '127.0.0.1', 
            'port': 6379, 
            'password': '', 
            'db': 1, 
            # 'max_connections': 5,  # 最大连接数 进程开多按情况降低连接数 最小值为2
            # 'decode_responses': True,  # 默认解析字符串，不解析默认为bytes类型
            'socket_connect_timeout': 5,  # 连接超时时长
            # ‘timeout’: 10,  # 重启连接间隔以及等待连接释放的超时时长
            # ‘ping_interval’: 30,  # ping间隔
            # 'use_block': False,   # 是否使用阻塞式共享连接池管理，阻塞式连接池管理能相对精准管控最大连接数，节省连接资源，但性能有所下降
        }, 
    }'''
conf_data = f'''# coding=utf-8
from nsanic.base_conf import BaseConf


class {class_conf}(BaseConf):
    SERVER_NAME = '{s_name}'
    SERVER_ID = '{s_id}'
    RUN_PORT = {port}
    DEBUG_MODE = False
    ACCESS_LOG = False
    MODEL_LIST = {m_list}
    RUN_FAST = {'False' if use_fast != 'y' else 'True'}
    VER_CODE = {None if use_ver == 'n' else use_ver}
    MODEL_EXTRA = {o_list}
    CONF_DB = {db_val}
    CONF_RDS = {rds_val}
'''
if m_list == ['main']:
    conf_data = conf_data.replace("MODEL_LIST = ['main']", '')
    add_file(os.path.join(dir_db, 'main.py'))
else:
    for dbf in m_list:
        add_file(os.path.join(dir_db, f'{dbf}.py'))
if o_list == ['main']:
    conf_data = conf_data.replace("MODEL_EXTRA = ['main']", '')
    add_file(os.path.join(dir_db, 'extra.py'))
else:
    for dbf in o_list:
        add_file(os.path.join(dir_db, f'{dbf}.py'))
add_file(os.path.join(dir_config, 'conf_start.py'), content=conf_data)
conf_key = s_name.split('_')[0]
init_data = f'''# coding=utf-8
from {s_name}.config.conf_start import {class_conf}


conf_srv = {class_conf}()
migrate_db = conf_srv.migrate_db()
'''
add_file(os.path.join(dir_config, '__init__.py'), content=init_data)

enum_data = '''# coding=utf-8
from nsanic.libs.consts import BaseEnum


# 请在此处创建枚举对象

'''
add_file(os.path.join(dir_config, 'consts.py'), content=enum_data)

ws_class = 'WsRdsConnector' if use_sub == 'y' else 'WsConnector'
connector_str = """WsProtocol.connector_map = {{
    {}.__name__: {}
}}
""".format(ws_class, ws_class)
ws_model = f'''from nsanic.base_ws import BaseWebsocket

from nsanic.libs.manager import {ws_class}''' if use_mode in (2, 3) else ''
ws_base = f'''\n\n\nclass BaseWebsocketApi(BaseWebsocket):

    conf = conf_srv
    ws_manager = {ws_class}''' if use_mode in (2, 3) else ''
api_data = f'''# coding=utf-8
from nsanic.handler_http import BaseHttpApi
{ws_model}
from {s_name}.config import conf_srv, ConfSrv


class BaseApi(BaseHttpApi):
    conf: ConfSrv = conf_srv{ws_base}
'''
add_file(os.path.join(server_path, 'base_api.py'), content=api_data)

test_data = f'''# coding=utf-8
from sanic import Request
from {s_name}.base_api import BaseApi


class TestApi(BaseApi):
    async def get(self, req: Request):
        return self.answer(hint="Here is a api for test.")
'''
add_file(os.path.join(dir_api, 'test_api.py'), content=test_data)

url_data = f'''# coding=utf-8
from nsanic.base_blue import BaseBlue
from nsanic.handler_http import Urls
from {s_name}.interface.test_api import TestApi


class MainBp(BaseBlue):
    # 路由请添加在这里
    DEFAULT_APIS = [
        # 结构为: 接口路由地址, 接口视图处理器, 版本号(可选), 接口命名(可选)
        Urls("/testapi", TestApi),
    ]
'''
add_file(os.path.join(server_path, 'url_main.py'), content=url_data)
ws_proto = 'from nsanic.base_ws import WsProtocol' if use_mode in (2, 3) else ''
ws_run = 'main_server.run(protocol=WsProtocol)' if use_mode in (2, 3) else 'main_server.run()'
connector = "from nsanic.libs.manager import {}".format(ws_class) if use_mode in (2, 3) else ""
start_data = '''# coding=utf-8
from nsanic.base_server import InitServer
{4}
from nsanic.exception import CatchExpt
from nsanic.middleware import CorsMiddle
{1}
from {0}.config import conf_srv as conf
from {0}.url_main import MainBp

signal_map = {{}}
{3}
main_server = InitServer(conf, mws=[CorsMiddle], bps=[MainBp], excps=[CatchExpt])
main_server.add_signal(signal_map)


if __name__ == '__main__':
    {2}
'''.format(s_name, ws_proto, ws_run, connector_str if use_mode in (2, 3) else '', connector)
add_file(os.path.join(base_path, f'{service_map.get(use_mode)}_{s_name}.py'), content=start_data)
if use_db == 'y':
    os.system(engine_map.get(use_engine)[1])
    os.system('pip install aerich')
