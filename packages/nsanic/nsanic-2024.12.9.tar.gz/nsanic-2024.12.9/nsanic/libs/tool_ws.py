from typing import Union

from nsanic.libs.consts import Code, StaCode
from nsanic.libs.tool import json_encode, json_parse


def pack_msg(
        cmd_type: Union[int, str],
        cmd_code: Union[int, str],
        data: Union[dict, list] = None,
        code: Code = StaCode.PASS,
        hint='',
        req=None,
        log_fun=None):
    """
    WS打包消息
    :param cmd_type: 消息命令类型
    :param cmd_code: 消息标识位
    :param data: 消息体数据
    :param code: 响应状态码
    :param hint: 提示信息
    :param req: 客户端消息标记
    :param log_fun: 日志记录方法
    """
    cmd = None
    if isinstance(cmd_code, int) and isinstance(cmd_type, int):
        if 0 <= cmd_code < 1000:
            cmd = cmd_type * 1000 + cmd_code
    if isinstance(cmd_code, str) or isinstance(cmd_type, str):
        cmd = f'{cmd_type}.{cmd_code}'
    if cmd:
        body = {'cmd': cmd, 'data': data, 'code': code.val, 'req': req, 'hint': hint or code.msg}
        return json_encode(body, u_byte=True, log_fun=log_fun)
    err_info = f'打包消息出错,消息结构错误: {cmd_type}, {cmd_code},{data},{code.val},{hint or code.msg},{req}'
    log_fun(err_info) if callable(log_fun) else print(err_info)
    return None


def parse_msg(data, log_fun=None):
    """消息解析"""
    msg = json_parse(data, log_fun=log_fun)
    if (not msg) or (not isinstance(msg, dict)):
        return None, None, None, None
    try:
        cmd = msg.get('cmd')
        if isinstance(cmd, int):
            cmd_type, cmd_code = cmd // 1000, cmd % 1000
        else:
            cmd_type, cmd_code = str(cmd).split('.')
    except Exception as err:
        log_fun(f'{data}消息解析出错：{err}') if log_fun else print(f'{data}消息解析出错：{err}')
        return None, None, None, None
    return cmd_type, cmd_code, json_parse(msg.get('data')), msg.get('req')
