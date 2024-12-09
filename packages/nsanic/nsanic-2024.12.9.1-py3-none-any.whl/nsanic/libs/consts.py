from dataclasses import dataclass
from enum import Enum
from types import DynamicClassAttribute

GLOBAL_TZ = 'UTC'
'''全局时区设置'''
GLOBAL_SRV_STATUS = False
'''全局服务状态控制'''


class BaseEnum(Enum):
    """
    继承自该类的枚举设置的模型必须为： name = (value/值, desc/描述或说明) 否则报错

    该类不允许被二次继承
    """

    @DynamicClassAttribute
    def val(self):
        """值"""
        return self.value[0]

    @DynamicClassAttribute
    def label(self):
        """描述"""
        return self.value[1]

    @DynamicClassAttribute
    def data(self):
        """数据(第三项 可选)"""
        if len(self.value) > 2:
            return self.value[2]
        return None

    @classmethod
    def fetch_name(cls, name) -> bool:
        """是否包含命名"""
        return name in cls._member_names_

    @classmethod
    def fetch_val(cls, value):
        """是否包含指定值"""
        v: BaseEnum
        for v in cls._value2member_map_.values():
            if v.val == value:
                return v
        return None

    @classmethod
    def get_name(cls, value):
        """获取指定值的描述"""
        v: BaseEnum
        for v in cls._value2member_map_.values():
            if v.val == value:
                return v.label
        return ""

    @classmethod
    def map_list(cls, outs: list = None):
        """
        以value -- label map的方式返回类型映射

        :param outs: 不输出的值集合, 该参数内的值不做输出
        """
        v: BaseEnum
        if not outs:
            return {v.val: v.label for v in cls._value2member_map_.values()}
        return {v.val: v.label for v in cls._value2member_map_.values() if v.val not in outs}


@dataclass
class Code:
    """状态码对象"""
    val: int
    '''指定响应码'''
    http: int = 200
    '''映射的状态码'''
    msg: str = ''
    '''附加的消息'''


class StaCode:
    """请求的响应状态码"""
    PASS = Code(0, 200, 'Finished.')
    TEND = Code(10, 410, 'Under maintenance.')
    FAIL = Code(11, 400, 'Failed.')
    '''公用请求失败，不确定响应状态请使用该项，并确保响应的文字描述'''
    ERR_ARG = Code(12, 422, 'Invalid params.',)
    '''参数错误或无效'''
    ERR_AUTH = Code(13, 401, 'Invalid authorization.')
    ERR_SIGN = Code(14, 412, 'Invalid sign in.')
    FORBID = Code(15, 403, 'Forbidden')
    NON_PMS = Code(16, 406, 'Non enough permission.')
    EXPIRED = Code(17, 409, 'Request was expired.')
    REAPED = Code(18, 421, 'Request is repeated.')
    ERR_CONF = Code(21, 501, 'Error by configuration.')


class AreaLevel(BaseEnum):
    """地域级别"""
    NATION = 1, '国家'
    PROVINCE = 2, '省/直辖市/地区'
    CITY = 3, '地级市/州/区/县级市'
    COUNTY = 4, '县/区域'
    TOWN = 5, '镇/城区/片区'
    STREET = 6, '街道/村/乡'


class FileSta(BaseEnum):
    NULL = -1, '未设置'
    UPING = 1, '上传中'
    CHECKING = 2, '校验中'
    ERR = 3, '上传错误'
    FINISHED = 4, '完成'
