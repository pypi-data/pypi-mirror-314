from dataclasses import dataclass
from typing import Annotated, Union

from sanic import Request
from sanic.views import HTTPMethodView

from nsanic import verify
from nsanic.base_ws import BaseWebsocket
from nsanic.exception import JsonFinish
from nsanic.libs.component import BaseMeta
from nsanic.libs.consts import Code
from nsanic.libs.tool_dt import to_datetime


@dataclass
class Urls:
    """接口路由对象"""
    router: str
    '''路由'''
    handler: Annotated[Union[HTTPMethodView, BaseWebsocket, type(HTTPMethodView), type(BaseWebsocket)], 'HTTPMethodView or subclass', 'BaseWebsocket or subclass']
    '''API视图处理器'''
    ver: str = ''
    '''接口版本号'''
    name: str = ''
    '''接口名称'''


class BaseRps(BaseMeta):
    def check_int(
            self,
            val,
            require=False,
            default: int = None,
            minval: int = None,
            maxval: int = None,
            inner=True,
            p_name='') -> int or None:
        """
        整形参数校验
        :param val: 待校验值
        :param require: 是否必要参数 默认非必要
        :param default: 非必要状态下的默认值
        :param minval: 最小值范围 type--int 默认不校验
        :param maxval: 最大值范围 type--int 默认不校验
        :param inner: 是否范围内(针对于min_val或max_val有值校验)，默认范围内，False为范围外
        :param p_name: 参数名
        :return 转换的值--int
        """
        sta, val_info = verify.vint(
            val, require=require, default=default, minval=minval, maxval=maxval, inner=inner, p_name=p_name)
        return val_info if sta else self.answer(code=self.conf.STA_CODE.ERR_ARG, hint=val_info)

    def check_str(
            self,
            val,
            require=False,
            default: str = None,
            turn=0,
            minlen: int = None,
            maxlen: int = None,
            p_name='') -> str or None:
        """
        字符串参数校验
        :param val: 待校验对象
        :param require: 是否必要参数 默认非必要
        :param default: 非必要状态下的默认值
        :param turn: 默认转换 1--转化大写 2--转换小写 其它值--不转化
        :param minlen: 最小长度 type--int 默认不校验
        :param maxlen: 最大长度 type--int 默认不校验
        :param p_name: 参数名
        :return 转换的值--str
        """
        sta, val_info = verify.vstr(
            val, require=require, default=default, turn=turn, minlen=minlen, maxlen=maxlen, p_name=p_name)
        return val_info if sta else self.answer(code=self.conf.STA_CODE.ERR_ARG, hint=val_info)

    def check_float(
            self,
            val,
            require=False,
            default: (float, int) = None,
            keep_val=3,
            minval: float or int = None,
            maxval: float or int = None,
            inner=True,
            p_name='') -> float or None:
        """
        浮点数校验
        :param val: 待校验对象
        :param require: 是否必要参数 默认非必要
        :param default: 非必要状态下的默认值
        :param keep_val: 保留小数未 默认3位
        :param minval: 最小值范围 type--int 默认不校验
        :param maxval: 最大值范围 type--int 默认不校验
        :param inner: 是否范围内(针对于min_val或max_val有值校验)，默认范围内，False为范围外
        :param p_name: 参数名
        :return 转换的值--float
        """
        sta, val_info = verify.vfloat(
            val, require=require, default=default, keep_val=keep_val, minval=minval, maxval=maxval,
            inner=inner, p_name=p_name)
        return val_info if sta else self.answer(code=self.conf.STA_CODE.ERR_ARG, hint=val_info)

    def check_time(self, val, require=False, default=None, time_min=None, time_max=None, inner=True, p_name=''):
        sta, val_info = verify.vdatetime(
            val, require=require, default=default, time_min=time_min, time_max=time_max, inner=inner, p_name=p_name)
        return val_info if sta else self.answer(code=self.conf.STA_CODE.ERR_ARG, hint=val_info)

    def check_type(self, val, query_fun, require=False, default=None, is_int=True, p_name=''):
        val = self.check_int(val, require=require, default=default, p_name=p_name) if is_int else \
            self.check_str(val, require=require, default=default, p_name=p_name)
        if val is None:
            return
        if query_fun(val):
            return val
        return self.answer(code=self.conf.STA_CODE.ERR_ARG, hint=f'{p_name}参数不在限定范围')

    def check_phone_number(self, phone_str: str, require=False):
        phone_str = self.check_str(phone_str, require=require, p_name='手机号')
        if phone_str:
            if verify.phone(phone_str):
                return phone_str
            return self.answer(code=self.conf.STA_CODE.ERR_ARG, hint='手机号不符合规范')

    def check_page(self, req: Request, page_max=200):
        """
        公共校验分页参数

        :param req: sanic请求对象
        :param page_max: 分页最大限制
        :return 校验状态, 分页偏移量, 分页限制量
        """
        page, page_size = (req.args.get('page'), req.args.get('page_size')) if req.method == 'GET' else (
            req.json.get('page'), req.json.get('page_size'))
        page = self.check_int(page, default=1, minval=1, p_name='页码')
        page_size = self.check_int(page_size, default=20, minval=1, maxval=page_max, p_name='分页大小')
        return page, page_size

    def check_time_inner(self, req: Request, begin_str='beginTime', end_str='endTime'):
        """检查时间区间 并按指定的查询参数集补充时间区间查询"""
        s_time, e_time = (req.args.get(begin_str), req.args.get(end_str)) if req.method == 'GET' else (
            req.json.get(begin_str), req.json.get(end_str))
        if s_time:
            s_time_str = self.check_str(s_time, require=True, minlen=10, maxlen=20, p_name=begin_str)
            if len(s_time_str) <= 10:
                s_time_str += " 00:00:00"
            s_time = to_datetime(s_time_str)
        if e_time:
            e_time_str = self.check_str(e_time, require=True, minlen=10, maxlen=20, p_name=end_str)
            if len(e_time_str) <= 10:
                e_time_str += " 00:00:00"
            e_time = to_datetime(e_time_str)
        s_time and e_time and e_time <= s_time and self.answer(
            code=self.conf.STA_CODE.ERR_ARG, hint='开始时间至少要大于结束时间')
        return s_time or None, e_time or None

    def answer(
            self, code: Code = None,
            data: (dict, object, list) = None,
            total: int = 0,
            hint: str = '',
            headers: dict = None):
        """
        公共JSON响应函数

        :param code: 响应码,请参照StaCode中取值, 默认响应成功状态
        :param data: 响应数据, 可以是任意符合JSON规范类型的数据模型
        :param total: 针对于分页响应的总数量
        :param hint: 响应消息, 字符串, 设置值后会采取设置的值，否则会使用响应码映射的默认值
        :param headers: 附加响应头
        """
        if not code:
            code = self.sta_code.PASS
        raise JsonFinish(code, data, total, hint, headers)


class BaseHttpApi(BaseRps, HTTPMethodView):
    """
    公用请求基础类
    """
