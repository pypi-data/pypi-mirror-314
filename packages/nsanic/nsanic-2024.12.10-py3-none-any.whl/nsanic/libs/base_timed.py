import asyncio
from typing import Union

from nsanic.libs import tool_dt
from nsanic.libs.mult_log import NLogger


class BaseTimed:

    TASK_MAP = {}

    __timed_arr = ('year', 'month', 'day', 'hour', 'minute', 'second')
    __units_map = {'second': 1, 'minute': 60, 'hour': 3600, 'day': 86400}

    def __init__(self, looping=None, run_tz='UTC', log = None):
        self.run_tz = run_tz
        if not looping:
            looping = asyncio.get_event_loop()
        if not log:
            log = NLogger
            log.init_conf()
        self.__run_loop = looping
        self.__logs = log
        self.__run_map = {}

    @property
    def logs(self):
        return self.__logs

    def start(self):
        self.__run_loop and self.__run_loop.run_forever()

    def loginfo(self, *info):
        if not info:
            return
        self.__logs.info(*info) if self.__logs else print(*info)

    def logerr(self, *err):
        if not err:
            return
        self.__logs.error(*err) if self.__logs else print(*err)

    def remove_task(self, name: str):
        tk = self.TASK_MAP.pop(name) if name in self.TASK_MAP else None
        tk and tk.cancel()

    def add_loop_task(self, name: str, interval: int, fun, fun_param: Union[list, tuple] = None, delay=0):
        """
        添加循环任务
        :param name: 任务名称
        :param interval: 运行间隔
        :param fun: 协程或可等待的执行函数
        :param fun_param: 执行函数参数
        :param delay: 启动后延时运行时间，0不运行
        :return:
        """

        async def loop_fun():
            delay and ((await fun(*fun_param)) if asyncio.iscoroutinefunction(fun) else fun(*fun_param))
            while 1:
                interval and (await asyncio.sleep(interval))
                try:
                    (await fun(*fun_param)) if asyncio.iscoroutinefunction(fun) else fun(*fun_param)
                except Exception as err:
                    self.loginfo('循环任务运行出错', err)

        if interval and interval <= 2:
            self.loginfo('存在间隔小于2秒的任务, 将不加入循环任务执行')
        if not fun_param:
            fun_param = []
        self.remove_task(name)
        tk = self.__run_loop.create_task(loop_fun(), name=name)
        self.TASK_MAP.update({name: tk})

    def add_timed_task(
            self,
            name: str,
            timed: Union[list, tuple],
            fun,
            fun_param: Union[list, tuple] = None,
            run_now=False):
        """
        添加定时任务
        :param name: 任务名称 重复的将会覆盖
        :param timed: 定时配置
        :param fun: 定时方法
        :param fun_param: 任务执行参数
        :param run_now: 是否立即执行一次
        """
        async def timed_fun(_timed, _run_now):
            if _run_now:
                ((await fun(*fun_param)) if asyncio.iscoroutinefunction(fun) else fun(*fun_param))
                self.__run_map[name] = tool_dt.cur_dt(tz=self.run_tz)
            while 1:
                g_sta, nt, over_sta = self.__get_next_datetime(_timed)
                if not nt:
                    break
                try:
                    self.__check_run(name, g_sta, timed) and (
                        await fun(*fun_param)) if asyncio.iscoroutinefunction(fun) else fun(*fun_param)
                except Exception as err:
                    self.loginfo('循环任务运行出错', err)
                dt = tool_dt.cur_dt(tz=self.run_tz)
                if dt > nt:
                    self.logs.info(
                        f'当前定时任务执行超时，将跳过当前周期进入下一周期，超时时长：{(dt - nt).total_seconds()}')
                    _, nt, _ = self.__get_next_datetime(timed, dt)
                    if not nt:
                        break
                interval = round((nt - dt).total_seconds(), 4)
                self.logs.info(f'定时任务下次运行等待时长:{interval}', timed, g_sta)
                await asyncio.sleep(interval)
        self.check_timed(timed)
        timed = list(timed)
        if not fun_param:
            fun_param = []
        self.remove_task(name)
        tk = self.__run_loop.create_task(timed_fun(timed, run_now), name=name)
        self.TASK_MAP.update({name: tk})

    @classmethod
    def check_timed(cls, timed: Union[list, tuple]):
        if not timed:
            raise Exception(f'{cls.__class__.__name__}未指定定时运行参数或间隔运行参数')
        if not isinstance(timed, (tuple, list)):
            raise Exception(f'{cls.__class__.__name__}定时参数不符合规范，要求必须是(年 月 日 时 分 秒)')
        if len(timed) != 6:
            raise Exception(f'{cls.__class__.__name__}定时参数不符合规范，要求必须是(年 月 日 时 分 秒)')
        for val in timed:
            if (val != '*') and (not str(val).isdigit()):
                raise Exception(f'{cls.__class__.__name__}定时参数不符合规范，必须是字符型数字或*(不指定)')
        if ''.join(list(map(str, timed))) == ('*' * 6):
            raise Exception(f'{cls.__class__.__name__}定时参数不符合规范，不能全部指定为*')
        if (timed[0] != '*') and (int(timed[0]) < 2023):
            raise Exception(f'{cls.__class__.__name__}定时参数不符合规范，年份不能小于当年')
        if (timed[1] != '*') and ((int(timed[1]) < 0) or (int(timed[1]) > 12)):
            raise Exception(f'{cls.__class__.__name__}定时参数不符合规范，月份不符合要求')
        if (timed[2] != '*') and ((int(timed[2]) < 0) or (int(timed[2]) > 31)):
            raise Exception(f'{cls.__class__.__name__}定时参数不符合规范，日期不符合要求')
        if (timed[3] != '*') and ((int(timed[3]) < 0) or (int(timed[3]) >= 24)):
            raise Exception(f'{cls.__class__.__name__}定时参数不符合规范，小时不符合要求')
        if (timed[4] != '*') and ((int(timed[4]) < 0) or (int(timed[4]) > 60)):
            raise Exception(f'{cls.__class__.__name__}定时参数不符合规范，分钟不符合要求')
        if (timed[5] != '*') and ((int(timed[5]) < 0) or (int(timed[5]) > 60)):
            raise Exception(f'{cls.__class__.__name__}定时参数不符合规范，秒不符合要求')

    def __check_run(self, name: str, sta_list, timed):
        """确保睡眠周期内每天执行一次"""
        if all(sta_list):
            return True
        m_len = timed.count('*')
        new_list = [sta_list[i] for i in range(m_len + 1)]
        if (0 < m_len < 5) and all(new_list):
            last_dt = self.__run_map.get(name)
            if not last_dt:
                return True
            cur_dt = tool_dt.cur_dt(tz=self.run_tz)
            if getattr(cur_dt, self.__timed_arr[m_len - 1]) != getattr(last_dt, self.__timed_arr[m_len - 1]):
                self.__run_map[name] = cur_dt
                return True
        return False

    def __get_next_datetime(self, timed, cur_dt=None):
        gt_sta = [False] * 6
        if not cur_dt:
            cur_dt = tool_dt.cur_dt(tz=self.run_tz)
        dt_list = [cur_dt.year, cur_dt.month, cur_dt.day, cur_dt.hour, cur_dt.minute, cur_dt.second]
        index_nt = -1
        for index, val in enumerate(timed):
            if val != '*':
                if int(val) == dt_list[index]:
                    gt_sta[index] = True
            else:
                gt_sta[index] = True
                index_nt = index
        if index_nt == -1:
            return gt_sta, None, False
        nt_list = [dt_list[i] for i in range(index_nt + 1)] + list(map(int, timed[index_nt + 1:]))
        next_dt = tool_dt.create_dt(*nt_list, tz=self.run_tz)
        over_sta = False
        if next_dt <= cur_dt:
            next_dt = self.cult_second_dt(next_dt, self.__timed_arr[index_nt])
            over_sta = True
        return gt_sta, next_dt, over_sta

    def cult_second_dt(self, dt, add_str: str, add_count: int = 1):
        if add_str in self.__units_map:
            return tool_dt.to_datetime(int(dt.timestamp()) + (add_count * self.__units_map[add_str]), tz=self.run_tz)
        if add_str == 'month':
            days_arr, year, month = [], dt.year, dt.month
            for i in range(add_count):
                month += 1
                if month <= 12:
                    days_arr.append(tool_dt.month_days(year, month))
                else:
                    year += 1
                    month = month - 12
                    days_arr.append(tool_dt.month_days(year, month))
            total_sec = sum(days_arr) * 86400
            return tool_dt.to_datetime(int(dt.timestamp()) + total_sec, tz=self.run_tz)
        total_sec = sum([(365 if not tool_dt.check_leap(dt.year + i) else 366) for i in range(add_count)]) * 86400
        return tool_dt.to_datetime(int(dt.timestamp()) + total_sec, tz=self.run_tz)
