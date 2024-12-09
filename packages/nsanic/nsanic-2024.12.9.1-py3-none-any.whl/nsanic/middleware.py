from sanic import Request, HTTPResponse

from nsanic.libs import consts
from nsanic.libs.component import BaseMeta
from nsanic.libs.manager import HeaderSet


class CorsMiddle(BaseMeta):

    @classmethod
    async def main(cls, req: Request):
        """通用跨域适配"""
        headers = HeaderSet.out(cls.conf)
        if req.method == 'OPTIONS':
            if ('*' not in cls.conf.ALLOW_ORIGIN) and (req.server_name not in cls.conf.ALLOW_ORIGIN):
                return HTTPResponse('', status=403, headers=headers)
            return HTTPResponse('', status=204, headers=headers)
        if not consts.GLOBAL_SRV_STATUS:
            return HTTPResponse('Server is not running', status=503, headers=headers)
