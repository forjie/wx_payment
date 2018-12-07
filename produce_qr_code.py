import requests
import json

from config.path import wx_app_url_qr_code


def get_wxa_code_image(
        access_token,
        wxa_path,
        scene='wxapp',
        width=430,
        auto_color=False,
        line_color=None,
        is_hyaline=True
):
    """
    :param access_token: 
    :param wxa_path:    '小程序中Page的路径',
    :param scene:       '自定义参数，格式你自己决定'
    """
    if line_color is None:
        line_color = {'r': '0', 'g': '0', 'b': '0'}
    url = wx_app_url_qr_code
    params = {'access_token': access_token}
    data = {
        'scene': scene,
        'page': wxa_path,
        'width': width,
        'auto_color': auto_color,
        'line_color': line_color,
        'is_hyaline': is_hyaline,
    }
    rep = requests.post(url, params=params, data=json.dumps(data))
    is_image = 'image' in rep.headers['Content-Type']
    return rep.content, is_image
