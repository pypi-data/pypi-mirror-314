"""
可注入式工具类
可按需要独立注入缓存或日志文件或不重复随机序列等的工具
"""
import decimal
import hashlib
import inspect
import math
from dataclasses import is_dataclass
from datetime import datetime, date
from typing import Union

import aiofiles
import httpx
import orjson


def is_await_fun(func):
    if inspect.isfunction(func) or inspect.ismethod(func):
        return inspect.iscoroutinefunction(func)
    return False


def calc_hash(val: (str, bytes), htype='sha3-256'):
    hash_map = {
        'md5': hashlib.md5,
        'sha256': hashlib.sha256,
        'sha384': hashlib.sha3_384,
        'sha512': hashlib.sha512,
        'sha3-224': hashlib.sha3_224,
        'sha3-256': hashlib.sha3_256,
        'sha3-384': hashlib.sha3_384,
        'sha3-512': hashlib.sha3_512,
    }
    if not isinstance(val, (str, bytes)):
        val = str(val)
    if isinstance(val, str):
        val = val.encode('utf-8')
    hb = hash_map.get(htype) or hashlib.sha3_256
    return hb(val).hexdigest()


def dict_key_to_str(data: dict):
    """将数字型key的字典转化为字符串key类型的字典"""
    if not isinstance(data, dict):
        return data
    new_conf = {}
    for k, v in data.items():
        if isinstance(v, dict):
            v = dict_key_to_str(v)
        elif isinstance(v, list):
            v = [dict_key_to_str(item) for item in v]
        if isinstance(k, (int, float)):
            new_conf[str(k)] = v
        else:
            new_conf[k] = v
    return new_conf


def dict_key_to_int(data: dict):
    """将整数字符串型key的字典转化为整数key类型的字典"""
    if not isinstance(data, dict):
        return data
    new_conf = {}
    for k, v in data.items():
        if isinstance(v, dict):
            v = dict_key_to_str(v)
        elif isinstance(v, list):
            v = [dict_key_to_str(item) for item in v]
        if isinstance(k, str) and k.isdigit():
            new_conf[int(k)] = v
        else:
            new_conf[k] = v
    return new_conf


def json_parse(item_str: Union[str, bytes], log_fun=None):
    """
    序列化json或字典字符串/集合字符串为Python字典/集合数据
    """
    if item_str:
        if isinstance(item_str, (dict, list, tuple)):
            return item_str
        try:
            info = orjson.loads(item_str)
            if isinstance(info, (dict, list, tuple)):
                return info
            return {}
        except (SyntaxError, ValueError, TypeError):
            err_info = f'解析数据出错, 原数据:{item_str}'
            log_fun(err_info) if callable(log_fun) else print(err_info)
    return {}


def json_encode(item, u_byte=False, log_fun=None):
    """
    转换为Json字符串 可以为字典 列表 元组 dataclass等类型
    ps: 使用该方式转换必须保证key不能为数字类型，特别是针对于python字典，有数字类型的key需要先将key转换为字符串
    """
    def dft_set(obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S %z")
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        raise TypeError

    if not item:
        return '' if not u_byte else b''
    option = orjson.OPT_PASSTHROUGH_DATETIME
    if is_dataclass(item):
        option = option | orjson.OPT_SERIALIZE_DATACLASS
    try:
        info = orjson.dumps(item, default=dft_set, option=option)
        return info.decode() if not u_byte else info
    except (SyntaxError, ValueError, TypeError):
        err_info = f'解析数据出错, 原数据:{item}'
        log_fun(err_info) if callable(log_fun) else print(err_info)
        return None


async def read_file(file_path: str, encoding=None, log_fun=None):
    """
    异步读取小文件 大文件请勿使用该方法

    :param file_path: 文件路径(包含文件名)
    :param encoding: (可选)解码模式
    :param log_fun: 日志输出方法
    """
    try:
        async with aiofiles.open(file_path, 'r', encoding=encoding) as f:
            data = await f.read()
            await f.close()
            return data
    except Exception as err:
        err_info = f'读取路径:{file_path} 文件出错:{err}, '
        log_fun(err_info) if callable(log_fun) else print(err_info)
        return None


async def write_file(data, file_path: str, encoding=None, log_fun=None):
    """
    异步写文件

    :param data: 待写入的数据
    :param file_path: 文件路径
    :param encoding: （可选）文件编码格式
    :param log_fun: 日志输出方法
    """
    try:
        async with aiofiles.open(file_path, 'wb', encoding=encoding) as f:
            await f.write(data)
        await f.close()
        return True
    except Exception as err:
        err_info = f'文件写入路径:{file_path} 出错:{err}'
        log_fun(err_info) if callable(log_fun) else print(err_info)
        return False


async def http_get(
        url: str,
        param: dict = None,
        headers: dict = None,
        timeout=10,
        http2=False,
        is_file=False,
        log_fun=None):
    """
    异步http get 请求

    :param url: 请求地址
    :param param: 查询参数
    :param headers: 请求头
    :param timeout: 超时时长 默认10秒
    :param http2: 使用http2.0协议
    :param is_file: 是否为文件
    :param log_fun: 日志输出方法
    """
    async with httpx.AsyncClient(http2=http2) as client:
        if param:
            query_param = ''
            for k, v in param.items():
                query_param += f'{k}={v}&'
            url += f'?{query_param[0: -1]}'
        res = await client.get(url, headers=headers, timeout=timeout)
        if res.status_code < 400:
            if callable(log_fun):
                info = f'Success: {url} \nParams: {param} \nResult: {res.text}'
                log_fun(info)
            return res.text if not is_file else res.content
        err_info = f'Failed: {url} \nParams: {param} \nResult: {res and res.status_code} {res and res.text}'
        log_fun(err_info) if callable(log_fun) else print(err_info)
        return None


async def http_post(
        url: str,
        param: Union[dict, str] = None,
        jsparse=True,
        headers: dict = None,
        timeout=10,
        http2=False,
        log_fun=None):
    """
    异步http post 请求

    :param url: 请求地址
    :param param: 请求参数
    :param jsparse: 是否采用Json格式传输 默认是
    :param headers: 请求头
    :param timeout: 超时时长 默认10秒
    :param http2: 使用http2.0协议
    :param log_fun: 日志输出方法
    """
    async with httpx.AsyncClient(http2=http2) as client:
        if jsparse:
            if not headers:
                headers = {'Content-Type': 'application/json; charset=utf-8'}
            res = await client.post(url, json=param, headers=headers, timeout=timeout)
        else:
            res = await client.post(url, data=param, headers=headers, timeout=timeout)
        if res.status_code < 400:
            if callable(log_fun):
                info = f'Success: {url} \nParams: {param} \nResult: {res.text}'
                log_fun(info)
            return res.text
        err_info = f'Failed: {url} \nParams: {param} \nResult: {res and res.status_code} {res and res.text}'
        log_fun(err_info) if callable(log_fun) else print(err_info)
        return None


def nearby_lonlat(distance: (int, float), lon: float, lat: float):
    """根据经纬度加距离获取矩形坐标范围"""
    radius = 6378137
    r_lon = math.degrees(math.radians(distance / radius * math.cos(math.radians(lon))))
    r_lat = math.degrees(math.radians(distance / radius * math.sin(math.radians(lat))))
    lon_list = (lon + r_lon, lon - r_lon)
    lat_list = (lat + r_lat, lat - r_lat)
    return min(lon_list), max(lon_list), min(lat_list), max(lat_list)
