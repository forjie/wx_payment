import json

from wx_utils import BaseWxApp
from config.path import wx_auth_url_access_token


class ObtainAccessToken(BaseWxApp):

    def get_access_token(self):
        params = {
            'grant_type': 'client_credential',
            'appid': self.appid,
            'secret': self.appsecret
        }
        rep = self.get(url=wx_auth_url_access_token, params=params)
        rep_data = json.loads(rep.text)
        if 'access_token' in rep_data.keys():
            return rep_data['access_token'], rep_data['expires_in']
        return None
