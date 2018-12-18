#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     ebank
   Description :
   Author :        hayden_huang
   Date：          2018/12/18 12:13
-------------------------------------------------
"""

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import requests
import json
import re
import random

success_num = 0

HEADERS = {
'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'api-version': "1.0",
    'Cache-Control': "no-cache",
    'client-os': "3",
    'client-type': "3",
    'Connection': "keep-alive",
    # 'Content-Length': "50",
    'Content-Type': "application/x-www-form-urlencoded",
    # 'Cookie': "Hm_lvt_93ed0e1334c3b2d4c2a036e42cfbd115=1545100854; Hm_lpvt_93ed0e1334c3b2d4c2a036e42cfbd115=1545100854",
    'Host': "ghesh3.imoba.com.cn",
    # 'nonce': "49797114",
    'Origin': "https://ghesh3.imoba.com.cn",
    'Pragma': "no-cache",
    # 'Referer': "https://ghesh3.imoba.com.cn/modules/views/HTML/activity/decemberActiveShare.html?friend_id=001_45066581333266306_mem&time=2018&from=singlemessage&isappinstalled=0",
    # 'sign': "6DMFYORwmmp70JZue9yXLxpU3r4=",
    'sign-method': "HMAC-SHA1",
    # 'timestamp': "1545100917648",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'cache-control': "no-cache",
}
SEND_CODE_URL = 'https://ghesh3.imoba.com.cn/coupon/prepare_call.ajax'
LOGIN_URL = 'https://ghesh3.imoba.com.cn/coupon/confirm_call.ajax'


class Shenhua(object):
    def __init__(self):
        pass

    def login(self):
        try:
            url = 'http://api.shjmpt.com:9002/pubApi/uLogin?uName=大叶子金融&pWord=lxf1234'
            response = requests.get(url,timeout=20)
            token = response.text.split('&')[0]
            return token
        except:
            print('登录失败')
            return None

    def get_phone(self,token):
        try:
            print('正在获取手机号')
            url = 'http://api.shjmpt.com:9002/pubApi/GetPhone?ItemId=152677&token={token}'.format(token=token)
            response = requests.get(url,timeout=20)
            return_res = response.text.replace(';', '')
            return return_res
        except:
            print('获取手机号失败')
            return None

    def get_message(self, token, phone):
        try:
            for i in range(8):
                url = 'http://api.shjmpt.com:9002/pubApi/GMessage?token={token}&ItemId=152677&Phone={phone}'.format(token=token, phone=phone)
                response = requests.get(url,timeout=20)
                print(response.text)
                if '&' in response.text:
                    message = response.text.split('&')[3]
                    search_res = re.search('\d{4,6}', message)
                    if search_res:
                        print('获取手机验证码成功')
                        return search_res.group(0)
                time.sleep(5)
            print('获取手机验证码失败')
            return None
        except:
            print('获取手机验证码失败')
            return None

    def logout(self,token):
        try:
            url = 'http://api.shjmpt.com:9002/pubApi/uExit?token={token}'.format(token=token)
            response = requests.get(url,timeout=20)
            print(response.text)
            return response
        except:
            print('退出登录失败失败')
            return None


def read():
    mylist = []
    with open('账号.txt') as f:
        results = f.readlines()
        for res in results:
            mylist.append(res.strip())
    return mylist


def send_code(phone,account):
    try:
        print('请求发送验证码。。')
        body = 'phone={phone}&userId={account}'.format(phone=phone,account=account)
        response = requests.post(SEND_CODE_URL, headers=HEADERS, data=body,verify=False,timeout=20)
        if response is not None:
            print(response.text)
            json_obj = json.loads(response.text)
            if json_obj['success'] == True:
                return json_obj
        return None
    except:
        print('发送验证码失败')
        return None

def login(phone, code, account):
    try:
        body = 'code={code}&phone={phone}&userId={account}'.format(phone=phone,code=code,account=account)
        response = requests.post(LOGIN_URL, headers=HEADERS, data=body,verify=False,timeout=20)
        if response is not None:
            print(response.text)
            json_obj = json.loads(response.text)
            if json_obj['success'] == True:
                print('升级电子券成功')
                return True
            else:
                print('升级电子券失败')
                return None
        print('升级电子券失败')
        return None
    except:
        print('升级电子券失败')
        return None

def start(account):
    token = shenhua.login()
    print(token)
    if token:
        phone = shenhua.get_phone(token)
        print(phone)
        if phone and re.search('\d+',phone):
            print('\n' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            send_res = send_code(phone,account)
            if send_res:
                message_res = shenhua.get_message(token, phone)
                if message_res:
                    reg_res = login(phone, message_res, account)
                    if reg_res:
                        global success_num
                        success_num+=1
                        with open('成功的手机.txt', 'a') as f:
                            write_res = phone + ',' +message_res + '\n'
                            f.write(write_res)
                            shenhua.logout(token)
                            return

                print('升级电子券失败')
                shenhua.logout(token)
                return
            else:
                print('发送验证码失败')
                shenhua.logout(token)
                return
    shenhua.logout(token)

if __name__ == '__main__':
    shenhua = Shenhua()
    num = input('请输入每个账号要升级的个数：')
    mylist = read()
    for account in mylist:
        print('正在处理：'+account)
        for i in range(int(num)):
            start(account)
        print('注册数: '+ num+ '  成功数: '+str(success_num))
        success_num = 0

    time.sleep(10)

