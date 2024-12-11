import asyncio
from asyncio import queues
from typing import Union

from nsanic.libs import tool, tool_ws


class WsConnector:
    """Websocket连接管理器"""
    OFFLINE_QUEUE = queues.Queue()
    _WS_MAP = {}
    conf = None

    @classmethod
    def set_conf(cls, conf):
        cls.conf = conf

    @classmethod
    def loginfo(cls, *info):
        cls.conf.log.info(*info) if cls.conf and cls.conf.log else print(*info)

    @classmethod
    def logerr(cls, *info):
        cls.conf.log.error(*info) if cls.conf and cls.conf.log else print(*info)

    @classmethod
    def all_ws(cls):
        return cls._WS_MAP.values()

    @classmethod
    def get_ws(cls, key: Union[str, int, bytes]):
        return cls._WS_MAP.get(key)

    @classmethod
    def init_task(cls, loop=None):
        pass

    @classmethod
    async def save_to_histories(cls, receiver, msg: [dict, list]):
        pass

    @classmethod
    async def send_histories(cls, receiver):
        pass

    @classmethod
    async def set_ws(cls, ukey: Union[str, int, bytes], ws, key_info: str = None):
        """更新连接，如果存在旧连接会关闭旧连接"""
        old_ws = cls.get_ws(ukey)
        cls._WS_MAP[ukey] = ws
        if old_ws:
            await old_ws.close()

    @classmethod
    async def close_ws(cls, ukey: Union[str, int, bytes], msg: Union[str, bytes] = None):
        ws = cls.get_ws(ukey)
        if ws:
            cls._WS_MAP.pop(ukey)
            try:
                msg and (await ws.send(msg))
                await ws.close()
            except Exception as err:
                _ = err

    @classmethod
    async def close_all(cls, reason: str = None):
        for ws in cls._WS_MAP.values():
            try:
                reason and await ws.send(reason)
                await ws.close()
            except Exception as err:
                _ = err
        cls._WS_MAP.clear()

    @classmethod
    async def offline(cls, ukey: Union[str, int, bytes]):
        await cls.close_ws(ukey)


class WsRdsConnector(WsConnector):
    """基于Redis缓存控制的Websocket连接管理器"""

    CHANNEL_LIST = ['']
    MAIN_CHANNEL = ''
    fun_pack_msg = tool_ws.pack_msg
    WS_ONLINE_KEY = 'WS_ONLINE_INFO'
    HISTORY_KEY = 'HISTORIES_USER_MESSAGE'
    HISTORY_COUNT = 50
    HISTORY_TYPE = 1
    '''历史消息存储类型，1--hash 针对数量少存储少的小体量消息，容易清理，2--LIST队列，针对存储量大的或者数量大的大体量消息，清理耗时但性能更好'''
    HISTORY_SEND_WAY = 1
    '''历史消息发送方式，1--一次性发所有历史消息 针对数量少存储少的小体量消息，2--将历史消息逐条发，针对存储量大的或者数量大的大体量消息'''

    @classmethod
    def set_conf(cls, conf):
        cls.conf = conf
        cls.MAIN_CHANNEL = f'NOTICE_{conf.SERVER_NAME.upper()}_{conf.SERVER_ID.upper()}_{conf.proc_name}'
        cls.CHANNEL_LIST.insert(0, cls.MAIN_CHANNEL)

    @classmethod
    def init_task(cls, loop=None):
        if not loop:
            loop = asyncio.get_running_loop()
        loop.create_task(cls.init_rds_listen())

    @classmethod
    async def init_rds_listen(cls):
        try:
            sub_obj = await cls.conf.rds.pub_sub(cls.CHANNEL_LIST)
        except Exception as err:
            cls.loginfo(f'订阅消息频道出错:{cls.CHANNEL_LIST},5秒后即将重启监听任务：{err}')
            await asyncio.sleep(5)
            return cls.init_task()
        while 1:
            try:
                t, c, m = await sub_obj.parse_response()
            except Exception as err:
                cls.logerr(f'监听任务出错:{cls.CHANNEL_LIST},10秒后即将重启监听任务：{err}')
                await asyncio.sleep(10)
                break
            if isinstance(t, bytes):
                t, c, m = t.decode(), c.decode(), (m.decode() if isinstance(m, bytes) else m)
            if t == 'message':
                if c == cls.MAIN_CHANNEL:
                    arg = cls.parse_main_channel(m)
                    arg and (await cls.on_receive_main_channel(*arg))
                    continue
                arg = cls.parse_channel_msg(c, m)
                arg and (await cls.on_receive_channel(c, *arg))
        # 监听失败 5秒后重启监听任务
        await asyncio.sleep(5)
        cls.init_task()

    @classmethod
    def parse_main_channel(cls, msg):
        """主通道监听消消息解析 如有需要可重写"""
        msg = tool.json_parse(msg)
        if (not msg) or not (isinstance(msg, dict)):
            return
        c_type, c_code, data, u = msg.get('t'), msg.get('c'), msg.get('d'), (msg.get('u') or -1)
        if not c_type:
            return
        return [c_type, c_code, data, u]

    @classmethod
    async def on_receive_main_channel(cls, cmd_type, cmd_code, data: dict, receiver):
        if not receiver:
            return
        if receiver == -1:
            for ws in cls.all_ws():
                try:
                    ws and (await ws.send(
                        cls.fun_pack_msg(cmd_type, cmd_code, data=data)))
                except Exception as err:
                    cls.loginfo(f'公共消息推送失败：{err}')
                    pass
            return
        ws = cls.get_ws(receiver)
        if not ws:
            return await cls.save_to_histories(receiver, cls.fun_pack_msg(cmd_type, cmd_code, data=data))
        try:
            return await ws.send(cls.fun_pack_msg(cmd_type, cmd_code, data=data))
        except Exception as err:
            cls.loginfo(f'发送目标消息失败,receiver:{receiver},data:{data},错误信息：{err}')
        return await cls.save_to_histories(receiver, cls.fun_pack_msg(cmd_type, cmd_code, data=data))

    @classmethod
    async def save_to_histories(cls, receiver, msg: [dict, list]):
        if not msg:
            return
        if not isinstance(msg, str):
            msg = tool.json_encode(msg, u_byte=True)
        if cls.HISTORY_TYPE == 1:
            if isinstance(msg, dict):
                msg = [msg]
            msg_list = await cls.conf.rds.get_hash(cls.HISTORY_KEY, receiver, jsparse=True)
            msg_list = msg_list.extend(msg) if msg_list else msg
            out_count = len(msg_list) - cls.HISTORY_COUNT
            if out_count > 0:
                msg_list = msg_list[out_count:]
            return await cls.conf.rds.set_hash(cls.HISTORY_KEY, receiver, msg_list)
        key_name = f"{cls.HISTORY_KEY}:{receiver}"
        await cls.conf.rds.qlpush(key_name, [msg] if isinstance(msg, dict) else msg)
        out_count = ((await cls.conf.rds.qlen(key_name)) or 0) - cls.HISTORY_COUNT
        if out_count > 0:
            _ = await cls.conf.rds.qrpop(key_name, count=out_count)

    @classmethod
    async def __send_msgs(cls, ws, msgs: Union[list, dict]):
        if not ws:
            return
        if cls.HISTORY_SEND_WAY or isinstance(msgs, dict):
            try:
                await ws.send(tool.json_encode(msgs))
                return True
            except Exception as err:
                cls.loginfo(f"推送历史消息失败，将重新入队: {err}")
            return
        for index, msg in enumerate(msgs):
            try:
                await ws.send(tool.json_encode(msg))
                continue
            except Exception as err:
                cls.loginfo(f"推送历史消息失败，将重新入队: {err}")
            return index
        return True

    @classmethod
    async def send_histories(cls, receiver):
        if receiver not in cls._WS_MAP:
            return
        if cls.HISTORY_TYPE == 1:
            msg_list = await cls.conf.rds.get_hash(cls.HISTORY_KEY, receiver, jsparse=True)
            if not msg_list:
                return
            ws = cls._WS_MAP.get(receiver)
            sta = cls.__send_msgs(ws, msg_list)
            sta and (await cls.conf.rds.del_hash(cls.HISTORY_KEY, receiver))
        key_name = f"{cls.HISTORY_KEY}:{receiver}"
        msg_list = await cls.conf.rds.qrpop(key_name, count=cls.HISTORY_COUNT)
        if not msg_list:
            return
        msg_list = [tool.json_parse(i) for i in msg_list]
        ws = cls._WS_MAP.get(receiver)
        idx = await cls.__send_msgs(ws, msg_list)
        if isinstance(idx, int):
            await cls.save_to_histories(receiver, [tool.json_parse(i) for i in msg_list[idx:]])
        if idx is None:
            await cls.save_to_histories(receiver, msg_list)

    @classmethod
    async def set_ws(cls, ukey: Union[str, int, bytes], ws, key_info: str = None):
        """更新连接，如果存在旧连接会关闭旧连接"""
        old_ws = cls.get_ws(ukey)
        cls._WS_MAP[ukey] = ws
        if old_ws:
            cls.conf and cls.conf.rds and await cls.conf.rds.drop_hash(
                cls.WS_ONLINE_KEY, getattr(old_ws, 'ukey', ''))
            await old_ws.close()
        key_info and cls.conf and cls.conf.rds and await cls.conf.rds.set_hash(cls.WS_ONLINE_KEY, ukey, key_info)

    @classmethod
    async def close_ws(cls, ukey: Union[str, int, bytes], msg: Union[str, bytes] = None):
        ws = cls.get_ws(ukey)
        if ws:
            cls._WS_MAP.pop(ukey)
            msg and await ws.send(msg)
            await ws.close()
        cls.conf and cls.conf.rds and await cls.conf.rds.drop_hash(cls.WS_ONLINE_KEY, ukey)

    @classmethod
    async def close_all(cls, reason: str = None):
        for ws in cls._WS_MAP.values():
            try:
                reason and await ws.send(reason)
                await ws.close()
            except Exception as err:
                _ = err
        cls._WS_MAP.clear()
        cls.conf and cls.conf.rds and await cls.conf.rds.del_item(cls.WS_ONLINE_KEY)

    @classmethod
    def parse_channel_msg(cls, channel: str, msg: dict):
        """解析其它通道的消息请重写该方法"""
        raise Exception('未实现其它频道的消息解析方法')

    @classmethod
    async def on_receive_channel(cls, channel: str, cmd_type, cmd_code, data: dict, receiver):
        """
        处理其它频道的消息
        :param channel: 频道标识
        :param cmd_type: 消息类型
        :param cmd_code: 消息标号
        :param data: 消息数据
        :param receiver: 接收者
        """
        raise Exception('未实现其它频道的消息处理方法')


class HeaderSet:

    RESP_TYPE = {
        'JSON': 'application/json',
        'MSGPACK': 'text/msgpack',
        'TEXT': 'text/plain',
        'HTML': 'text/html',
        'PROTO': 'application/octet-stream',
    }

    @classmethod
    def out(cls, conf):
        tp = cls.RESP_TYPE.get(conf.RESP_TYPE)
        if not tp:
            raise Exception('无效的响应类型配置')
        if conf.RESP_TYPE != 'MSGPACK':
            tp += f';charset={conf.CHARSET}'
        headers = {
            'Content-Type': tp,
            'Access-Control-Allow-Methods': ','.join(conf.ALLOW_METHOD),
            'Access-Control-Max-Age': conf.ORIGIN_MAX_AGE,
            'Access-Control-Allow-Headers': '*' if '*' in conf.ALLOW_HEADER else ','.join(conf.ALLOW_HEADER),
            'Access-Control-Allow-Origin': '*' if '*' in conf.ALLOW_ORIGIN else ','.join(conf.ALLOW_ORIGIN),
            'Access-Control-Allow-Credentials': conf.ALLOW_CREDENTIALS
        }
        return headers
