from typing import Union

from sanic import Blueprint

from nsanic.base_conf import BaseConf
from nsanic.handler_http import Urls


class BaseBlue:

    DEFAULT_APIS: (list, tuple) = []
    bpo: Blueprint = None
    name: str = None
    url_prefix: str = None
    conf: BaseConf = None
    __loop_handlers: list = []

    @classmethod
    def set_conf(cls, conf: BaseConf, bp_name: str = None):
        cls.conf = conf
        if not bp_name:
            bp_name = cls.__name__
            len_name = len(bp_name)
            bp_name = f'{bp_name[0].lower()}{bp_name[1: len_name]}'
            if bp_name[-2: len_name].lower() == 'bp':
                bp_name = bp_name[0: -2]
        cls.name = bp_name
        srv_arr = conf.SERVER_NAME.split('_')
        srv_str = f"{srv_arr[0]}{''.join([srv_arr[i].capitalize() for i in range(1, len(srv_arr))])}"
        new_prefix = srv_str if cls.name == 'main' else f'{srv_str}/{ cls.name}'
        cls.url_prefix = new_prefix
        cls.bpo = Blueprint(name=cls.name, url_prefix=new_prefix, version=conf.VER_CODE, version_prefix='/v')

    @classmethod
    def load_default_api(cls):
        """加载默认API"""
        cls.DEFAULT_APIS and cls.__load_api(cls.DEFAULT_APIS)

    @classmethod
    def init_loop_task(cls):
        for handler in cls.__loop_handlers:
            handler().init_loop_task()

    @classmethod
    def __load_api(cls, item_list):
        for item in item_list:
            if not item:
                continue
            if not isinstance(item, Urls):
                raise Exception(f'Invalid router urls object: {item}')
            if not item.handler:
                raise Exception(f'Invalid router handler object: {item}')
            if not item.router:
                if hasattr(item.handler, 'as_view') or hasattr(item.handler, 'wsrouter'):
                    item = [f'/{cls.name}', item]
                else:
                    continue
            version = cls.conf.VER_CODE if not item.ver else item.ver
            if item.router and item.router[0] != '/':
                rpath = f'/{item.router}'
            else:
                rpath = item.router
            if hasattr(item.handler, 'as_view'):
                cls.bpo.add_route(item.handler.as_view(), rpath, version=version, name=item.name or None)
                continue
            if hasattr(item.handler, 'wsrouter'):
                ws_obj = item.handler.init_ws()
                cls.bpo.add_websocket_route(ws_obj.wsrouter, rpath, version=version, name=item.name or None)
            hasattr(item.handler, 'init_loop_task') and cls.__loop_handlers.append(item.handler)

    @classmethod
    def load_apis(cls, item_list: list):
        """
        批量注册路由
        :param item_list: 加载模型必须为[(路由,API处理器类,(可选)版本号)]
        """
        cls.__load_api(item_list)

    def register_api(self, url: str, handler, ver: Union[int, str, float] = None):
        """注册单路由"""
        self.bpo and self.bpo.add_route(handler, url, ver)

    def add_signal(self, event: str, handler, condition=None, exclusive=True):
        """
        注册信号

        """
        self.bpo and self.bpo.add_signal(handler, event, condition=condition, exclusive=exclusive)

    # def add_bp(self):
    #     """注册其它蓝图组路由"""
    #     self.__blue_obj.group()
