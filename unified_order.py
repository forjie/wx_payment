from wx_utils import BaseWxApp
from wx_utils import get_external_ip
from wx_utils import generate_randomStr
from wx_utils import calc_sign
from wx_utils import dict_to_xml
from wx_utils import xml_to_dict
from config.path import wx_mch_url_unified_order
from config.path import wx_mch_url_order_query
from config.path import wx_mch_url_close_order
from config.path import wx_mch_url_pay_refund
from config.path import wx_mch_url_refund_query

WX_CERT_PATH = "path/to/apiclient_cert.pem"
WX_KEY_PATH = "path/to/apiclient_key.pem.unsecure"


class UnifiedOrder(BaseWxApp):
    """
    不需要证书
    """
    TRADE_TYPE = 'JSAPI'
    SIGN_TYPE = 'MD5'
    FEE_TYPE = 'CNY'
    cert_path = (WX_CERT_PATH, WX_KEY_PATH)  # 发起申请退款时需携带的证书的路径

    """
    key设置路径：微信商户平台(pay.weixin.qq.com)-->账户设置-->API安全-->密钥设置
    参考 https://zhidao.baidu.com/question/1447664017722993060.html
    python无法使用双向证书，使用openssl导出：
    openssl pkcs12 -clcerts -nokeys -in apiclient_cert.p12 -out apiclient_cert.pem
    openssl pkcs12 -nocerts -in apiclient_cert.p12 -out apiclient_key.pem
    导出apiclient_key.pem时需输入PEM phrase, 此后每次发起请求均要输入，可使用openssl解除：
    openssl rsa -in apiclient_key.pem -out apiclient_key.pem.unsecure
    """
    key = ''

    def pay_order(self, mch_id, body,
                  total_fee, notify_url, out_trade_no, client_ip, time_start, time_expire,
                  user_id, detail=None, attach=None, trade_type=TRADE_TYPE, fee_type=FEE_TYPE, goods_tag=None,
                  product_id=None, device_info=None, sign_type=SIGN_TYPE, limit_pay=None):
        """
        统一下单
        """
        time_start = time_start.strftime('%Y%m%d%H%M%S')
        time_expire = time_expire.strftime('%Y%m%d%H%M%S')
        data = {
            'appid': self.appid,
            'mch_id': mch_id,  # 商户号
            'nonce_str': generate_randomStr(),  # 随机字符串，长度要求在32位以内。
            'body': body,  # 商品简单描述
            'out_trade_no': out_trade_no,  # 商户系统内部订单号，要求32个字符内
            'total_fee': total_fee,  # 标价金额
            'spbill_create_ip': client_ip or get_external_ip(),  # 发起提现的ip
            'notify_url': notify_url,  # 异步接收微信支付结果通知的回调地址    --
            'trade_type': trade_type,  # 小程序取值如下：JSAPI
            'device_info': device_info,  # (否)自定义参数，可以为终端设备号(门店号或收银设备ID)
            'sign_type': sign_type,  # 加密类型
            'detail': detail,  # (否)商品详细描述，对于使用单品优惠的商户，
            'attach': attach,  # (否) 附加数据，在查询API和支付通知中原样返回，可作为自定义参数使用
            'fee_type': fee_type,  # 符合ISO 4217标准的三位字母代码，默认人民币：CNY
            'time_start': time_start,  # 订单生成时间，格式为yyyyMMddHHmmss，如2009年12月25日9点10分10秒表示为20091225091010
            'time_expire': time_expire,  # 订单失效时间，格式为yyyyMMddHHmmss
            'goods_tag': goods_tag,  # (否) 订单优惠标记，使用代金券或立减优惠功能时需要的参数
            'product_id': product_id,  # (否) trade_type=NATIVE时，此参数必传。此参数为二维码中包含的商品ID，商户自行定义
            'limit_pay': limit_pay,  # (否) 指定支付方式:上传此参数no_credit--可限制用户不能使用信用卡支付
            'openid': user_id,  # (否) trade_type=JSAPI，此参数必传，用户在商户appid下的唯一标识
        }
        return self.get_return_data(wx_mch_url_unified_order, data=data)

    def order_query(self, mch_id,
                    transaction_id,
                    out_trade_no,
                    sign_type=SIGN_TYPE):
        """
        查询订单
        :param transaction_id: 微信的订单号
        """
        data = {
            'appid': self.appid,
            'mch_id': mch_id,
            'transaction_id': transaction_id,
            'out_trade_no': out_trade_no,
            'nonce_str': generate_randomStr(),
            'sign_type': sign_type,
        }
        return self.get_return_data(wx_mch_url_order_query, data=data)

    def close_order(self, mch_id, out_trade_no,
                    sign_type=SIGN_TYPE):
        """
        关闭订单
        """
        data = {
            'appid': self.appid,
            'mch_id': mch_id,
            'out_trade_no': out_trade_no,
            'nonce_str': generate_randomStr(),
            'sign_type': sign_type,
        }
        return self.get_return_data(wx_mch_url_close_order, data=data)

    def refund_pay(
            self, mch_id, total_fee, refund_fee, out_refund_no,
            out_trade_no, notify_url, fee_type='CNY', op_user_id=None,
            refund_account='REFUND_SOURCE_UNSETTLED_FUNDS'):
        """
        申请退款  需要证书
        :param total_fee: 订单总金额，单位为分，只能为整数
        :param refund_fee: 退款总金额，订单总金额，单位为分，只能为整数
        :param out_refund_no: 商户系统内部的退款单号，商户系统内部唯一
        :param nonce_str: 
        :param out_trade_no: 商户系统内部订单号，要求32个字符内
        :param notify_url: 异步接收微信支付退款结果通知的回调地址
        :param fee_type:    货币类型
        :param op_user_id: 
        :param refund_account: 退款资金来源
        
        
        返回:
            appid
            mch_id
            nonce_str
            req_info        #加密的信息--需要解密
        
        退款结果对重要的数据进行了加密，商户需要用商户秘钥进行解密后才能获得结果通知的内容
        解密步骤如下： 
            （1）对加密串A做base64解码，得到加密串B
            （2）对商户key做md5，得到32位小写key* ( key设置路径：微信商户平台(pay.weixin.qq.com)-->账户设置-->API安全-->密钥设置 )
            （3）用key*对加密串B做AES-256-ECB解密（PKCS7Padding）
        """
        data = {
            'appid': self.appid,
            'mch_id': mch_id,
            'nonce_str': generate_randomStr(),
            'out_trade_no': out_trade_no,
            'out_refund_no': out_refund_no,
            'total_fee': total_fee,
            'refund_fee': refund_fee,
            'refund_fee_type': fee_type,
            'op_user_id': op_user_id if op_user_id else mch_id,
            'refund_account': refund_account,
            'notify_url': notify_url,
        }
        return self.get_return_data(wx_mch_url_pay_refund, data=data, cert=self.cert_path)

    def refund_query(self, mch_id, nonce_str, out_trade_no):
        """
        查询退款 不需要证书
        """
        data = {
            'appid': self.appid,
            'mch_id': mch_id,
            'nonce_str': nonce_str,
            'out_trade_no': out_trade_no,
        }
        return self.get_return_data(wx_mch_url_refund_query, data=data)

    def get_return_data(self, url, **kwargs):
        """
        获取最终返回结果
        """
        data = kwargs['data']
        data = {k: v for k, v in data.items() if v is not None}
        sign = calc_sign(data, self.key)
        data['sign'] = sign
        kwargs['data'] = dict_to_xml(data).encode('utf-8')
        rep = super(UnifiedOrder, self).post(url, **kwargs)
        return xml_to_dict(rep.content)
