import json

from config.path import wx_auth_url_jscode2session
from wx_utils import BaseWxApp


class ObtainOpenidSessionKey(BaseWxApp):

    def get_openid_session_key(self, jscode):
        params = {
            'appid': self.appid,
            'secret': self.appsecret,
            'js_code': jscode,
            'grant_type': 'authorization_code',
        }

        ret = self.get(wx_auth_url_jscode2session, **params)
        ret_json = json.loads(ret.text)
        if 'session_key' in ret_json.keys():
            return ret_json['openid'], ret_json['session_key']
        return None
