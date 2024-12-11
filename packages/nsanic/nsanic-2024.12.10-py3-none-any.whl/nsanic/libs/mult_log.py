import logging
import multiprocessing
import os
from logging import handlers


class NLogger:
    log_fmt = "%(asctime)s - %(process)d:%(lineno)s:%(levelname)s - %(message)s"
    '''日志格式'''
    date_fmt = '%Y-%m-%d %H:%M:%S'
    '''日期格式'''
    base_path = os.path.join(os.getcwd(), 'logs')
    '''基础路径'''
    full_path = None
    proc_split = 0
    '''进程隔离模式 0-不隔离 1-按进程标识隔离 2-按进程pid隔离'''
    proc_tab = None
    '''进程标识  proc_split 为1时有效'''
    log_split = 1
    '''日志分割模式  0-单日志 1-按固定大小分割的滚动日志 2-按时间分割的滚动日志'''
    t_when = 'D'
    '''按时间滚动方式 log_split为2有效 可取值S-秒 M-分 H-小时 D-天 W-周'''
    interval = 1
    '''按时间滚动方式间隔周期 log_split为2有效'''
    keep_count = 10
    '''针对滚动日志类型或时间分割类型日志需要保留的日志个数 log_split为1或2有效'''
    log_size = 104857600
    '''滚动类型日志单个日志的最大限制大小 log_split为1有效'''
    encoding = 'utf-8'
    '''日志存储的编码格式'''
    level = 'INFO'
    '''日志默认记录级别'''
    console = True
    '''控制台输出'''

    @classmethod
    def init_conf(cls, base_path: str = None, folder: str = None, log_fmt: str = None, dt_fmt: str = None,
                  proc_split: int = 0, proc_tab: str = None, log_split: int = 0, t_when: str = None, interval=1,
                  keeps: int = None, log_size: int = None, encoding: str = None, level: str = None, console=True):
        """
        初始化日志管理器
        :param base_path: 日志基础路径
        :param folder: 路径下的存储目录
        :param log_fmt: 日志格式
        :param dt_fmt: 日期格式
        :param proc_split: 进程隔离模式 0-不隔离 1-按进程标识隔离 2-按进程pid隔离
        :param proc_tab: 进程标识  proc_split 为1时有效
        :param log_split: 日志分割模式  0-单日志 1-按固定大小分割的滚动日志 2-按时间分割的滚动日志
        :param t_when: 按时间滚动方式设置 可取值S-秒 M-分 H-小时 D-天 W-周
        :param interval: 按时间滚动方式间隔周期 log_split为2有效
        :param keeps: 针对滚动日志类型或时间分割类型日志需要保留的日志个数 log_split为1或2有效
        :param log_size: 滚动类型日志单个日志的最大限制大小 log_split为1有效
        :param encoding: 日志存储的编码格式 默认utf-8
        :param level: 日志默认记录级别
        :param console: 加控制台输出
        """
        if base_path:
            cls.base_path = base_path
        (not os.path.exists(cls.base_path)) and os.mkdir(cls.base_path)
        if folder:
            cls.full_path = os.path.join(os.path.join(cls.base_path, folder))
            (not os.path.exists(cls.full_path)) and os.mkdir(cls.full_path)
        else:
            cls.full_path = cls.base_path
        if log_fmt:
            cls.log_fmt = log_fmt
        if dt_fmt:
            cls.date_fmt = dt_fmt
        if proc_split and proc_split in (0, 1, 2):
            cls.proc_split = proc_split
        if cls.proc_split == 1:
            cls.proc_tab = proc_tab.lower() if proc_tab else multiprocessing.current_process().name.lower()
        elif cls.proc_split == 2:
            cls.proc_tab = str(os.getpid())
        else:
            cls.proc_tab = ""
        if log_split:
            cls.log_split = log_split
        if cls.log_split == 2:
            cls.t_when = t_when if t_when else 'D'
            cls.interval = interval if interval else 1
            cls.keep_count = keeps if keeps else 10
        elif cls.log_split == 1:
            cls.log_size = log_size if log_size else 104857600
            cls.keep_count = keeps if keeps else 10
        if encoding:
            cls.encoding = encoding
        if level:
            cls.level = level
        cls.console = console

    @classmethod
    def _mklog(cls, log_name='runlog'):
        f_name = f"{log_name}_{cls.proc_tab}.log"
        fp = os.path.join(cls.full_path, f_name)
        log = logging.getLogger(fp)
        if log.handlers:
            return log
        formatter = logging.Formatter(fmt=cls.log_fmt, datefmt=cls.date_fmt)
        if cls.log_split == 1:
            log_handler = handlers.RotatingFileHandler(
                filename=fp, mode="a", maxBytes=cls.log_size, backupCount=cls.keep_count, encoding=cls.encoding)
        elif cls.log_split == 2:
            log_handler = handlers.TimedRotatingFileHandler(
                filename=fp, when=cls.t_when, interval=cls.interval, backupCount=cls.keep_count, encoding=cls.encoding)
        else:
            log_handler = handlers.RotatingFileHandler(filename=fp, mode="a", encoding=cls.encoding)
        log.setLevel(cls.level)
        log_handler.setFormatter(formatter)
        log.addHandler(log_handler)
        if cls.console:
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            log.addHandler(ch)
        return log

    @classmethod
    def error(cls, *out_info):
        """代码或执行失败或报错的日志 调用该方法前请确认init_conf已调用"""
        log = cls._mklog(log_name='error')
        log.error(str(out_info[0]) if len(out_info) == 1 else str(out_info))

    @classmethod
    def critical(cls, *out_info):
        log = cls._mklog(log_name='error')
        log.critical(str(out_info[0]) if len(out_info) == 1 else str(out_info))

    @classmethod
    def info(cls, *out_info):
        """标记或打印类的日志 调用该方法前请确认init_conf已调用"""
        log = cls._mklog()
        log.info(str(out_info[0]) if len(out_info) == 1 else str(out_info))

    @classmethod
    def warning(cls, *out_info):
        """警告类日志 调用该方法前请确认init_conf已调用"""
        log = cls._mklog()
        log.warning(str(out_info[0]) if len(out_info) == 1 else str(out_info))

    @classmethod
    def debug(cls, *out_info):
        """debug日志 调用该方法前请确认init_conf已调用"""
        log = cls._mklog()
        log.debug(str(out_info[0]) if len(out_info) == 1 else str(out_info))
