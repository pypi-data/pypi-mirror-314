import asyncio
import traceback
from typing import Union

from redis.asyncio import Redis, ConnectionPool, BlockingConnectionPool

from nsanic.libs.rds_locker import RdsLocker
from nsanic.libs.tool import json_encode, json_parse


class RdsError(Exception):
    pass


class RdsClient:
    """redis连接对象 单例模式请用init方法初始化"""
    CONN_MAP = {}

    def __init__(self, conf: dict, logs=None):
        self.__timeout = conf.pop('timeout') if 'timeout' in conf else 10
        self.__ping = conf.pop('ping_interval') if 'ping_interval' in conf else 30
        self.__block = conf.pop('use_block') if 'use_block' in conf else False
        self.is_decode = conf.get('decode_responses', False)
        self.__conf = conf
        self.__logs = logs
        self.__pool = ConnectionPool(**self.__conf) if not self.__block else BlockingConnectionPool(
            **self.__conf, timeout=self.__timeout)

    @classmethod
    def init(cls, conf: dict, logs=None):
        """单例模型请用该方法进行初始化"""
        if not all(key in conf for key in ['host', 'port', 'db']):
            raise Exception('Redis连接配置错误,没有必须的配置项')
        conf_name = f"{conf['host']}-{conf['port']}-{conf['db']}"
        clt = cls.CONN_MAP.get(conf_name)
        if not clt:
            clt = cls(conf, logs=logs)
            cls.CONN_MAP[conf_name] = clt
        return clt

    def logerr(self, *err):
        self.__logs.error(*err) if self.__logs else print(*err)

    def loginfo(self, *info):
        self.__logs.info(*info) if self.__logs else print(*info)

    def init_loop(self, _=None, loop=None):
        if not loop:
            loop = asyncio.get_event_loop()
        loop.create_task(self.__loop_ping())

    async def __loop_ping(self):
        while 1:
            try:
                await self.conn.ping()
            except Exception as err:
                self.logerr(f'redis连接已失效,将在{self.__timeout}秒后重试: {err} \n{traceback.format_exc()}')
                self.__pool.reset()
                await asyncio.sleep(self.__timeout)
                continue
            await asyncio.sleep(self.__ping)

    @property
    def conn(self):
        return Redis(connection_pool=self.__pool)

    async def locked(self, key: str, fun=None, fun_param: Union[list, tuple] = None, time_out=5, pre_key='LOCKER__'):
        """
        :param key: 锁定标识
        :param fun: 执行函数
        :param fun_param: 函数参数
        :param time_out: 自动释放时间
        :param pre_key: 锁定标识预制前缀，用于区分锁定标识采用redis key本身
        """
        if not fun_param:
            fun_param = ()
        if pre_key:
            key = f'{pre_key}{key}'
        async with self.conn.lock(key, lock_class=RdsLocker, timeout=time_out):
            return callable(fun) and ((await fun(*fun_param)) if asyncio.iscoroutinefunction(fun) else fun(*fun_param))

    async def get_item(self, key: Union[str, bytes], jsparse=False):
        """
        获取缓存
        :param key: 缓存名称
        :param jsparse: 是否解析Json字符串为字典
        """
        if await self.conn.exists(key):
            info = await self.conn.get(key)
            if jsparse:
                return json_parse(info)
            return info.encode() if self.is_decode else info
        return

    async def del_item(self, *args):
        """删除"""
        if not args:
            return
        return await self.conn.delete(*args)

    async def set_item(self, key: Union[str, bytes], value: Union[str, int, float, bytes, list, tuple, dict],
                       ex_time: int = None):
        """
        设置字符串缓存
        :param key: 缓存名称
        :param value: 缓存值，非字符串类型将会自动转换为字符串存储
        :param ex_time: 缓存有效期，默认不设置，既永久有效，类型数字类型 单位：秒 # type:int
        """
        if isinstance(value, (list, tuple, dict)):
            value = json_encode(value)
        return await self.conn.set(key, value, ex=ex_time)

    async def exists(self, key: Union[str, bytes]):
        """检查key是否存在"""
        return await self.conn.exists(key)

    async def drop_item(self, key: Union[str, bytes]):
        """
        根据key删除某项缓存
        :param key: 缓存名称
        """
        return await self.conn.delete(key)

    async def get_hash(self, key: Union[str, bytes], h_key: Union[str, bytes], jsparse=False):
        """
        获取Hash值

        :param key: 缓存名称
        :param h_key: 缓存键名称
        :param jsparse: 是否解析Json字符串为字典
        """
        if await self.conn.hexists(key, h_key):
            info: Union[str, bytes] = await self.conn.hget(key, h_key)
            if jsparse:
                return json_parse(info)
            return info.encode() if self.is_decode else info

    async def set_hash(self, key: Union[str, bytes], h_key: Union[str, bytes], data):
        """
        设置Hash

        :param key: 缓存名称
        :param h_key: 缓存键名称
        :param data: 保存的数据
        """
        if isinstance(data, list) or isinstance(data, dict):
            data = json_encode(data, log_fun=self.__logs.error if self.__logs else None)
        return await self.conn.hset(key, h_key, data)

    async def drop_hash(self, key: Union[str, bytes], h_key: Union[str, bytes]):
        """
        删除Hash值
        :param key: 缓存名称
        :param h_key: 缓存键名称
        """
        return await self.conn.hdel(key, h_key)

    async def drop_hash_bulk(self, key: Union[str, bytes], key_list: Union[list, tuple]):
        """
        批量删除Hash值
        :param key: 缓存名称
        :param key_list: 缓存键列表
        """
        key_list and (await self.conn.hdel(key, *key_list))

    async def get_hash_all(self, key: Union[str, bytes], jsparse=False):
        """
        获取整个Hash
        :param key: 缓存名
        :param jsparse: 是否解析Json字符串为字典
        """
        info = await self.conn.hgetall(key)
        if not info:
            return
        if jsparse:
            new_dict = {}
            for k, v in info.items():
                if isinstance(k, bytes):
                    k = k.decode()
                if jsparse:
                    v = json_parse(v)
                new_dict[k] = v
            return new_dict
        return info

    async def get_hash_val(self, key: Union[str, bytes]):
        """
        获取整个Hash所有值
        :param key: 缓存名
        """
        return await self.conn.hvals(key)

    async def set_hash_bulk(self, key: Union[str, bytes], h_map: dict):
        """
        通过字典映射设置或更新多个Hash
        :param key: 缓存名
        :param h_map: 字典映射 -- 必须是{str: str} 或{bytes: str} 或{bytes: bytes} 几种形式
        """
        return await self.conn.hset(key, mapping=h_map)

    async def scan_hash(self, key: Union[str, bytes], start: int = 0, count: int = None, match: str = None):
        """
        按匹配的条件迭代扫描hash
        """
        return await self.conn.hscan(key, cursor=start, match=match, count=count)

    async def pub_sub(self, channel: Union[str, list, tuple]):
        """消息订阅模型"""
        sub_item = self.conn.pubsub()
        if isinstance(channel, str):
            channel = [channel]
        await sub_item.subscribe(*channel)
        return sub_item

    async def publish(self, channel: str, msg: Union[bytes, str]):
        """
        发布消息
        :param channel: 消息信道
        :param msg: 发布的消息
        """
        return await self.conn.publish(channel, msg)

    async def qlpush(self, key: str, data_list: list):
        """
        左侧入队列
        :param key: 队列/集合名称
        :param data_list: 入队列表 --type: list
        """
        values = []
        for item in data_list:
            if isinstance(item, dict) or isinstance(item, list):
                item = json_encode(item, log_fun=self.__logs.error if self.__logs else None)
            values.append(item)
        return await self.conn.lpush(key, *values)

    async def qrpush(self, key: str, data_list: list):
        """
        右侧入队列
        :param key: 队列/集合名称
        :param data_list: 入队列表 --type: list
        """
        values = []
        for item in data_list:
            if isinstance(item, dict) or isinstance(item, list):
                item = json_encode(item, log_fun=self.__logs.error if self.__logs else None)
            values.append(item)
        return await self.conn.rpush(key, *values)

    async def qrpop(self, key: str, count=1, jsparse=False):
        """
        右侧出队

        :param key: 队列/集合名称
        :param count: 出队数量
        :param jsparse: 是否解析Json字符串为字典
        """
        info: Union[str, bytes, list] = await self.conn.rpop(key, count=None if count <= 1 else count)
        if not info:
            return
        if count <= 1:
            if jsparse:
                return json_parse(info)
            return info.encode() if self.is_decode else info
        if jsparse:
            return [json_parse(item) for item in info]
        return [item.encode() for item in info] if self.is_decode else info

    async def qlpop(self, key: str, count=1, jsparse=False):
        """
        左侧出队

        :param key: 队列/集合名称
        :param count: 出队数量
        :param jsparse: 是否解析Json字符串为字典
        """
        info: Union[str, bytes, list] = await self.conn.lpop(key, count=None if count <= 1 else count)
        if not info:
            return 
        if count <= 1:
            if jsparse:
                return json_parse(info)
            return info.encode() if self.is_decode else info
        if jsparse:
            return [json_parse(item) for item in info]
        return [item.encode() for item in info] if self.is_decode else info

    async def qlen(self, key: str):
        """
        获取队列长度
        :param key: 队列/集合名称
        """
        return await self.conn.llen(key)

    async def expired(self, key: Union[str, bytes], t: int, nx=False, xx=False, gt=False, lt=False):
        return await self.conn.expire(key, time=t, nx=nx, xx=xx, gt=gt, lt=lt)

    async def incr(self, key: Union[str, bytes], count: int):
        return await self.conn.incr(key, int(count))

    async def pipline_fun(self, fun, transaction=True, raise_err=True):
        """
        :param fun: 指定添加pipline的方法，唯一参数为pipline对象
        :param transaction: 是否使用事务执行，redis事务不支持回滚
        :param raise_err: 有失败是否报错
        """
        pl = self.conn.pipeline(transaction=transaction)
        fun(pl)
        if len(pl):
            await pl.execute(raise_on_error=raise_err)
