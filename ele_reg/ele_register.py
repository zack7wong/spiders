#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import requests
import json
import re
import random

success_num = 0

ELE_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36',
    'referer': 'https://h5.ele.me/login/',
    'origin': 'https://h5.ele.me',
    'content-type': 'application/json; charset=utf-8',
    'x-shard': 'loc=113.94,22.53',
    'pragma': 'no-cache',
    'Connection': 'close',
    # 'cookie': 'ubt_ssid=xrcdl8dke750f6bi7m0jsax8tw4n0dae_2018-05-16; track_fingerprint_1=902800516; perf_ssid=st4xdwkflp2pjf72bwxbvdm680azboki_2018-05-16; _utrace=452e0182af08ede380a79e2b58d3e8de_2018-05-16; eleme__ele_me=a21ef9090bed70f13eff8a30d47f85e3%3Aa95fa8d1549dcd1b0f799d08fe52f300d0cb4bdc; track_id=1528863870|8fcef661aeb628115265d821bda442b07ebf87869bec975470|5f63f4d5267dc40dc5e688ff92822dd2'
}
SEND_CODE_URL = 'https://h5.ele.me/restapi/eus/login/mobile_send_code'
LOGIN_URL = 'https://h5.ele.me/restapi/eus/login/login_by_mobile'


class Shenhua(object):
    def __init__(self):
        pass

    def login(self):
        url = 'http://api.shjmpt.com:9002/pubApi/uLogin?uName=&pWord='
        response = requests.get(url,timeout=40)
        token = response.text.split('&')[0]
        return token

    def get_phone(self,token):
        url = 'http://api.shjmpt.com:9002/pubApi/GetPhone?ItemId=378&token={token}'.format(token=token)
        response = requests.get(url,timeout=40)
        return_res = response.text.replace(';', '')
        return return_res

    def get_message(self, token, phone):
        for i in range(8):
            url = 'http://api.shjmpt.com:9002/pubApi/GMessage?token={token}&ItemId=378&Phone={phone}'.format(token=token, phone=phone)
            response = requests.get(url,timeout=40)
            print(response.text)
            if '&' in response.text:
                message = response.text.split('&')[3]
                search_res = re.search('\d{6}', message)
                if search_res:
                    print('获取手机验证码成功')
                    return search_res.group(0)
            time.sleep(5)
        print('获取手机验证码失败')
        return None


def send_code(phone):
    print('请求饿了么发送验证码。。')

    body = '{"mobile":"'+phone+'","captcha_value":"","captcha_hash":""}'
    print(body)
    print(SEND_CODE_URL)
    print(ELE_HEADERS)
    response = requests.post(SEND_CODE_URL, headers=ELE_HEADERS, data=body,verify=False)
    if response is not None:
        print('饿了么发送验证码后返回的token：' + response.text)
        json_obj = json.loads(response.text)
        validate_token = json_obj['validate_token']
        return validate_token
    return None

def login(phone, code, validate_token):
    body = '{"mobile":"'+phone+'","validate_code":"'+code+'","validate_token":"'+validate_token+'"}'
    print(body)
    response = requests.post(LOGIN_URL, headers=ELE_HEADERS, data=body,verify=False)
    if response is not None:
        print(response.text)
        json_obj = json.loads(response.text)
        if 'name' in json_obj and ((json_obj['name'] == 'INVALID_VALIDATE_TOKEN' or json_obj['name'] == 'WRONG_VALIDATE_CODE')):
            print('注册失败')
            return None
        elif 'SID' in response.cookies.get_dict():
            cookie = response.cookies.get_dict()
            print(cookie)
            print('登录成功')
            return True
        else:
            print('注册失败')
            return None

def reset_password():
    url = 'https://restapi.ele.me/eus/v1/users/125645914/password/by_password'
    put = ''
    {
        "old_password": "hhh666",
        "new_password": "hhh555"
    }

def start():
    # try:
        token = shenhua.login()
        phone = shenhua.get_phone(token)
        print('\n' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        print('当前手机号:' + phone)
        validate_token = send_code(phone)
        if validate_token:
            message_res = shenhua.get_message(token, phone)
            if message_res:
                reg_res = login(phone, message_res, validate_token)
                if reg_res:


                    global success_num
                    success_num+=1
                    with open('account.txt', 'a') as f:
                        write_res = phone + ',123456' + '\n'
                        f.write(write_res)
                        return

            print('注册失败')
            return
        else:
            print('发送验证码失败')
            return
    # except:
    #     print('异常，跳过。。')

if __name__ == '__main__':
    shenhua = Shenhua()
    num = input('请输入注册个数：')
    for i in range(int(num)):
        start()
    print('注册数: '+ num+ '  成功数: '+str(success_num))

