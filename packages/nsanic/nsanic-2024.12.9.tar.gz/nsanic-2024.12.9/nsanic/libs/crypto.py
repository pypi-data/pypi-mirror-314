import base64
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


def rsa_decode(item_str: str, pri_key: str, log_fun=None):
    """rsa私钥加密"""
    if not isinstance(item_str, str):
        item_str = str(item_str)
    cipher_pri = PKCS1_v1_5.new(RSA.importKey(pri_key))
    try:
        decp_str = cipher_pri.decrypt(base64.b64decode(item_str.encode('utf-8')), Random.new().read)
    except Exception as err:
        err_info = f"RSA解析失败:{err}\n原数据:{item_str}"
        log_fun(err_info) if callable(log_fun) else print(err_info)
        return None
    return decp_str.decode()


def rsa_encode(item_str: str, pub_key: str, log_fun=None):
    """rsa公钥加密"""
    if not isinstance(item_str, str):
        item_str = str(item_str)
    try:
        cipher_pub = PKCS1_v1_5.new(RSA.importKey(pub_key))
        item_ecp = cipher_pub.encrypt(item_str.encode('utf-8'))
        return base64.b64encode(item_ecp).decode()
    except Exception as err:
        err_info = f'加密数据出错,源数据{item_str}\n错误信息:{err}'
        log_fun(err_info) if callable(log_fun) else print(err_info)


def create_rsa(df_len=2048):
    """
    创建RSA密钥对

    :param df_len: 默认允许加密长度2048--最大加密245长度  设置128生成时将会更快速--最多只能加密117长度的字符串
    :return 私钥,公钥
    """
    gen = RSA.generate(df_len)
    return (gen.exportKey('PEM')).decode('utf8'), (gen.publickey().exportKey()).decode('utf8')
