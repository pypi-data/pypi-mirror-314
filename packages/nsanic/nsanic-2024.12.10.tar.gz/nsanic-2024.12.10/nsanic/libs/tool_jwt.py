import jwt

from nsanic.libs.tool_dt import cur_time


def jencode(
        user_id: int or str,
        jw_type: int,
        safe_key='qazxswedc1234',
        client_info='',
        extra=None,
        useful_life: int = None
):
    """
    JWT加密 默认采用HS256

    :param user_id: 用户ID
    :param jw_type: 授权类型 暂时分四大块： 管理账户、代销账户、常规账户、线下设备
    :param safe_key: 用户随机授权码，一般在用户刷新jwt token、注销登录等操作后会绑定唯一设备等操作时会重置，保证token唯一性
    :param client_info: 客户端唯一标识信息(可选),设置该值可以标识token的唯一性
    :param extra: (可选)授权附加信息,注入后解析可直接获得 勿放置敏感信息
    :param useful_life: token 有效期
    """
    cur_t = cur_time()
    ex_time = (useful_life or 7 * 86400) + cur_t
    preload = {
        'sub': jw_type,
        'iss': 'default',
        'exp': ex_time,
        'iat': cur_t,
        'aud': f'{jw_type}_{client_info}' if client_info else str(jw_type),
        'identify': user_id,
        'extra': extra,
    }
    head_dict = {
        'typ': 'JWT',
        'alg': 'HS256',
    }
    jwt_str = jwt.encode(preload, key=safe_key, headers=head_dict)
    return jwt_str


def get_jwinfo(jwt_str: str):
    """
    获取jwt token 加配信息 账户ID, 授权类型, 附加信息
    """
    try:
        data = jwt.decode(jwt_str, algorithms=['HS256'], options={'verify_exp': False, 'verify_signature': False})
    except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidTokenError):
        return None, 'Invalid authorization'
    if not data:
        return None, 'Invalid authorization'
    uid, jw_type = data.get('identify'), data.get('sub')
    if (not uid) or (not jw_type):
        return None, 'Invalid authorization'
    return uid, data


def jdecode(jwt_str: str, jw_type: int, safe_key='qazxswedc1234', client_info='', new_check=False):
    """
    JWT TOKEN 解析
    """
    try:
        client_info = f'{jw_type}_{client_info}' if client_info else str(jw_type)
        info = jwt.decode(jwt_str, key=safe_key, algorithms=['HS256'], audience=client_info)
    except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidTokenError, jwt.exceptions.InvalidKeyError):
        return None, 'Invalid authorization'
    except jwt.exceptions.InvalidSignatureError:
        return None, 'Error certificate'
    except jwt.exceptions.InvalidAudienceError:
        return None, 'Authorization not match'
    except jwt.exceptions.ExpiredSignatureError:
        return None, 'Authorization expired'
    cur_t, new_token = cur_time(), None
    if new_check and (info.get('exp') - cur_t <= 43200):
        # token有效期低于1天的自动刷新token
        new_token = jencode(
            user_id=info.get('identify'), jw_type=jw_type, safe_key=safe_key,
            client_info=client_info, extra=info.get('extra'))
    return info, new_token
