import time
import traceback
from functools import wraps
from threading import Lock

from nsanic.libs.mult_log import NLogger


class SingleTon(type):
    """ 单例元类 加线程锁"""
    __instances = {}

    def __new__(cls, *args, **kwargs):
        """ 当类实例化时调用该方法 """
        if not cls.__instances.get(cls):
            # 多线程环境下，若类实例构造方法中有IO任务，则需要加锁让获取锁的线程完成实例化，后续线程访问直接从__instances获取
            with Lock():
                cls.__instances[cls] = super().__new__(*args, **kwargs)
        return cls.__instances[cls]


def with_meta(meta, base_class=object):
    """
    meta: 元类, type或type的派生类, 用于创建类
    等价于继承 base_class, metaclass=meta
    example:
        ```
        class Test(with_meta(type, superclass)):
            pass
        ```
    """
    return meta("NewBase", (base_class,), {})


def singleton(cls):
    """单实例装饰器 加线程锁"""
    ins_map = {}

    def ins(*args, **kwargs):
        if cls not in ins_map:
            with Lock():
                ins_map[cls] = cls(*args, **kwargs)
        return ins_map[cls]
    return ins


def aio_catcher(log: NLogger = None):
    """协程异常捕获器"""

    def expt(fun):
        @wraps(fun)
        async def wrap_fun(*args, **kwargs):
            try:
                return await fun(*args, **kwargs)
            except Exception as err:
                err_str = f"执行出错：{err}\n{ traceback.format_exc()}"
                log.error(err_str) if log else print(err_str)
        return wrap_fun
    return expt


def catcher(log: NLogger = None):
    """常规异常捕获器"""

    def expt(fun):
        @wraps(fun)
        def wrap_fun(*args, **kwargs):
            try:
                return fun(*args, **kwargs)
            except Exception as err:
                err_str = f"执行出错：{err}\n{traceback.format_exc()}"
                log.error(err_str) if log else print(err_str)
        return wrap_fun
    return expt


def aio_runtime(log: NLogger = None):
    """协程 时间检查"""

    def out_runtime(fun):
        @wraps(fun)
        async def wrap_fun(*args, **kwargs):
            s_time = time.time()
            req = await fun(*args, **kwargs)
            e_time = time.time()
            info_str = f'程序执行时间: {(e_time - s_time) * 1000}毫秒'
            log.info(info_str) if log else print(info_str)
            return req
        return wrap_fun
    return out_runtime


def runtime(log: NLogger = None):
    """常规时间检查"""

    def out_runtime(fun):
        @wraps(fun)
        def wrap_fun(*args, **kwargs):
            s_time = time.time()
            req = fun(*args, **kwargs)
            e_time = time.time()
            info_str = f'程序执行时间: {(e_time - s_time) * 1000}毫秒'
            log.info(info_str) if log else print(info_str)
            return req
        return wrap_fun
    return out_runtime
