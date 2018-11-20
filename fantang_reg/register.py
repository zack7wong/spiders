#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     register
   Description :
   Author :        hayden_huang
   Date：          2018/11/20 10:14
-------------------------------------------------
"""

import time
import requests
import json
import re
import random

Area_list = ['浙江','江苏', '福建', '上海', '海南', '湖北']

class Shenhua(object):
    def __init__(self):
        pass

    def login(self):
        url = 'http://api.shjmpt.com:9002/pubApi/uLogin?uName=caojiani1&pWord=4623369'
        response = requests.get(url)
        token = response.text.split('&')[0]
        return token

    def get_phone(self,token):
        area = random.sample(Area_list, 1)
        url = 'http://api.shjmpt.com:9002/pubApi/GetPhone?ItemId=229266&token={token}'.format(token=token)
        response = requests.get(url)
        return_res = response.text.replace(';', '')
        return return_res

    def get_message(self, token, phone):
        for i in range(8):
            url = 'http://api.shjmpt.com:9002/pubApi/GMessage?token={token}&ItemId=229266&Phone={phone}'.format(token=token, phone=phone)
            response = requests.get(url)
            print(response.text)
            if '&' in response.text:
                message = response.text.split('&')[3]
                search_res = re.search('\d{4}', message)
                if search_res:
                    print('获取手机验证码成功')
                    return search_res.group(0)
            time.sleep(5)
        print('获取手机验证码失败')
        return None

success_num = 0

headers = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Content-Length':'20',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie':'JSESSIONID=6AD01F446B390E2F95810AB24B99CF64',
    'Host':'www.topfans.cc',
    'Origin':'http://www.topfans.cc',
    'Pragma':'no-cache',
    'Referer':'http://www.topfans.cc/sweetfansH5/shareIt.html?id=412222',
    'User-Agent':'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
}

def send_code(phone):
    url = 'http://www.topfans.cc/tupu/LoginAPI/getPhoneCode.do'
    body = 'phonenum={phone}'.format(phone=phone)
    response = requests.post(url, headers=headers, data=body)
    if response.status_code == 200:
        json_boj = json.loads(response.text)
        if json_boj['resultCode'] == '1000':
            return True

    return None

def register(phone,code):
    url = 'http://www.topfans.cc/tupu/LoginAPI/oAuthLoginNew.do'
    body = 'checkcode={code}&clientType=android&inviteuserid=412222&latitude=30.31&longitude=120.20&openid={phone}&password=e10adc3949ba59abbe56e057f20f883e&phonenum={phone}&phoneType=1'.format(phone=phone,code=code)
    response = requests.post(url, headers=headers, data=body)
    print(response.text)
    if response.status_code == 200:
        json_boj = json.loads(response.text)
        if json_boj['resultCode'] == '1000':
            return True

    return None

def start():
    token = shenhua.login()
    phone = shenhua.get_phone(token)
    print('\n')
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    print('当前手机号:' + phone)
    send_res = send_code(phone)
    if send_res:
        message_res = shenhua.get_message(token, phone)
        if message_res:
            reg_res = register(phone, message_res)
            if reg_res:
                print('注册成功')
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

if __name__ == '__main__':
    shenhua = Shenhua()
    num = input('请输入注册个数：')
    for i in range(int(num)):
        start()
    print('注册数: '+ num+ '  成功数: '+str(success_num))

