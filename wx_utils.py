import requests
import random
import string
import socket
import hashlib
import base64

from xml.etree import ElementTree
from Crypto.Cipher import AES


class BaseWxApp(object):
    _client = requests
    _timeout = 15

    def __init__(self, appid, appsecret):
        self.appsecret = appsecret
        self.appid = appid

    def get(self, url, **kwargs):
        kwargs['timeout'] = self._timeout
        return self._client.get(url, **kwargs)

    def post(self, url, **kwargs):
        kwargs['timeout'] = self._timeout
        return self._client.post(url, **kwargs)


# 生成nonce_str
def generate_randomStr():
    return ''.join(random.sample(string.ascii_letters + string.digits, 32))


# 发起提现的ip
def get_external_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        wechat_ip = socket.gethostbyname('api.mch.weixin.qq.com')
        sock.connect((wechat_ip, 80))
        addr, port = sock.getsockname()
        sock.close()
        return addr
    except socket.error:
        return '127.0.0.1'


def calc_sign(params, sign_key):
    """计算签名
        对接收到数据进行排序,并进行加密
    """
    sign_data = ['{0}={1}'.format(k, params[k]) for k in sorted(params) if params[k]]
    sign_data.append('key={0}'.format(sign_key))
    sign_data = '&'.join(sign_data)
    md5_sign_data = get_str_md5(sign_data)
    return md5_sign_data


def get_str_md5(temp, upper: bool = True):
    """
    字符串进行加密
    并对字符串转换成大写
    """
    md5_str = hashlib.md5(temp.encode('utf-8')).hexdigest()
    return md5_str.upper() if upper else md5_str.lower()


def dict_to_xml(dict_data):
    """
    dict 转为 xml
    <xml>
        <appid>wxd930ea5d5a258f4f</appid>
        <mch_id>10000100</mch_id>
        <device_info>1000</device_info>
        <body>test</body>
        <nonce_str>ibuaiVcKdpRxkhJA</nonce_str>
        <sign>9A0A8659F005D6984697E2CA0A9CF3B7</sign>
    </xml>
    """
    xml = ["<xml>"]
    for k, v in dict_data.items():
        xml.append("<{0}>{1}</{0}>".format(k, v))
    xml.append("</xml>")
    return "".join(xml)


def xml_to_dict(xml_data):
    """
    xml 转为 dict
    :param xml_data:
    :return:
    """
    xml_dict = {}
    root = ElementTree.fromstring(xml_data)
    for child in root:
        xml_dict[child.tag] = child.text
    return xml_dict


def decrypt_wx_refund_data(key, encrypt_data):
    """
    解密微信退款数据
    :param sign_key: 商户key
    :param encrypt_data:  加密的信息
    :return:
    """

    def un_pad(s):
        return s[:-ord(s[len(s) - 1:])]

    sign_key_md5 = get_str_md5(key, upper=False).encode('utf-8')
    encrypt_data_64 = base64.b64decode(encrypt_data)
    aes = AES.new(sign_key_md5, AES.MODE_ECB)
    decrypted_text = aes.decrypt(encrypt_data_64)
    return xml_to_dict(un_pad(decrypted_text))
