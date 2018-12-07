wx_api_url_base = 'https://api.weixin.qq.com'
# 用户登录认证
wx_auth_url_jscode2session = wx_api_url_base + '/sns/jscode2session'
# 用户access_token获取
wx_auth_url_access_token = wx_api_url_base + '/cgi-bin/token'
# 小程序码生成
wx_app_url_qr_code = wx_api_url_base + '/wxa/getwxacodeunlimit'

wx_mch_url_base = 'https://api.mch.weixin.qq.com'
# 统一下单
wx_mch_url_unified_order = wx_mch_url_base + '/pay/unifiedorder'
# 查询订单
wx_mch_url_order_query = wx_mch_url_base + '/pay/orderquery'
# 关闭订单
wx_mch_url_close_order = wx_mch_url_base + '/pay/closeorder'
# 申请退款
wx_mch_url_pay_refund = wx_mch_url_base + '/secapi/pay/refund'
# 查询退款
wx_mch_url_refund_query = wx_mch_url_base + '/pay/refundquery'
