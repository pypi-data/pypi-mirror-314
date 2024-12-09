import asyncio

from sanic import Sanic

from nsanic.base_conf import BaseConf
from nsanic.libs import consts


class InitServer:

    def __init__(
            self,
            conf,
            mws: (list, tuple) = None,
            bps: (list, tuple) = None,
            excps: (list, tuple) = None,
            forbid_before_evt=True,
            start_evt: list = None,
            stop_evt: list = None):
        """
        :param conf: BaseConf 对象
        :param mws: middleware 对象列表或元组
        :param excps: 全局异常捕获器
        :param forbid_before_evt: 是否在启动事件完成前进行接口拦截
        :param start_evt: 启动需要注册的事件
        :param stop_evt: 服务结束前的注册事件
        """
        self.__conf: BaseConf = conf
        self.__conf.set_conf()
        consts.GLOBAL_TZ = conf.TIME_ZONE
        if not forbid_before_evt:
            consts.GLOBAL_SRV_STATUS = True
        self.__evt_start = start_evt or []
        self.__evt_stop = stop_evt or []
        self.__srv = Sanic(self.__conf.SERVER_NAME, log_config=self.__conf.log_conf())
        self.__srv.update_config(self.__conf)
        self.__bp_list = []
        if self.__conf.db_conf:
            from tortoise.contrib.sanic import register_tortoise
            register_tortoise(self.__srv, config=self.__conf.db_conf())
        for mdw_fun in mws or []:
            mdw_fun.set_conf(self.__conf)
            self.__srv.middleware(mdw_fun.main)
        for bp_cls in bps:
            bp_cls.set_conf(self.__conf)
            bp_cls.load_default_api()
            hasattr(bp_cls, 'init_loop_task') and self.__bp_list.append(bp_cls)
            self.__srv.blueprint(bp_cls.bpo)
        for expt_fun in excps or []:
            expt_fun.set_conf(self.__conf)
            self.__srv.error_handler.add(Exception, expt_fun.catch_req)
        self.__srv.register_listener(self.__after_server_start, 'after_server_start')
        self.__srv.register_listener(self.__before_server_stop, 'before_server_stop')

    async def __after_server_start(self, app, loop):
        if self.__conf.rds:
            self.__conf.rds.init_loop()
            await asyncio.sleep(0.5)
        for bp_cls in self.__bp_list:
            bp_cls.init_loop_task()
        for fun in self.__evt_start:
            (await fun(app, loop)) if asyncio.iscoroutinefunction(fun) else fun(app, loop)
        consts.GLOBAL_SRV_STATUS = True

    async def __before_server_stop(self, app, loop):
        consts.GLOBAL_SRV_STATUS = False
        for fun in self.__evt_stop:
            await fun(app, loop)

    @property
    def main(self):
        return self.__srv

    def add_signal(self, signal_map: dict):
        """信号注册"""
        if not signal_map:
            return
        for k, v in signal_map.items():
            callable(v) and self.__srv.add_signal(v, k)

    def add_start_event(self, events):
        if callable(events):
            self.__evt_start.append(events)
        if isinstance(events, (list, tuple)):
            self.__evt_start.extend(events)

    def add_stop_event(self, events):
        if callable(events):
            self.__evt_stop.append(events)
        if isinstance(events, (list, tuple)):
            self.__evt_stop.extend(events)

    def run(self, protocol=None):

        self.__srv.run(
            host=self.__conf.HOST,
            port=self.__conf.RUN_PORT,
            workers=self.__conf.RUN_WORKER if not self.__conf.RUN_FAST else 1,
            fast=self.__conf.RUN_FAST,
            debug=self.__conf.DEBUG_MODE,
            access_log=self.__conf.ACCESS_LOG,
            protocol=protocol
        )
