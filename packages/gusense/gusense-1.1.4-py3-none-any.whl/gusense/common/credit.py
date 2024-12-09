# -*- coding:utf-8 -*-

"""
用户认证
Date: 2023.05.09
author: wgp
contact: 284250692@qq.com
"""

import json
import pandas as pd
import os
import requests
from ..common import constant

user_path = os.path.expanduser('~')

"""
    用户认证方法，开发者ID和密匙来源Gusense数据中心
"""

def auth(app_id, app_secret):
    token = get_token(app_id, app_secret)
    if token is None or token == '':
        params = {
            "appId": app_id,
            "appSecret": app_secret
        }
        res = requests.post(contant.LOGIN_URL, params=params, timeout=contant.TIME_OUT)
        json_res = json.loads(res.text)
        code = json_res['code']
        if code == contant.REQ_SUCCESS_CODE:
            token = json_res['data']
            df = pd.DataFrame([[app_id, app_secret, token]], columns=['app_id', 'app_secret', 'token'])
            op = os.path.join(user_path, contant.USER_TOKEN_CN)
            df.to_csv(op, index=False)
        else:
            path = user_path + contant.SEPARATOR + contant.USER_TOKEN_CN
            if os.path.exists(path):
                os.remove(user_path + contant.SEPARATOR + contant.USER_TOKEN_CN)
            msg = json_res['msg']
            raise Exception(msg)


"""
    获取token的方法
"""

def get_token(app_id=None, app_secret=None):
    credit_list = get_credit_list()
    if credit_list is None:
        return None
    if app_id is not None and app_secret is not None:
        oai = credit_list['app_id']
        oas = credit_list['app_secret']
        if app_id != oai:
            return None
        if app_secret != oas:
            return None
    return credit_list['token']


def get_credit_list():
    op = os.path.join(user_path, contant.USER_TOKEN_CN)
    if os.path.exists(op):
        df = pd.read_csv(op)
        credit_list = df.loc[0]
        return credit_list
    else:
        return None
