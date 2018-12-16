#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     285200_register
   Description :
   Author :        hayden_huang
   Date：          2018/12/16 13:50
-------------------------------------------------
"""

import requests
from hashlib import md5
import json
import time
from requests import RequestException
from time import sleep

login_url = 'http://www.285200.com/Login/Login'
logout_url = 'http://www.285200.com/Login/Quit'
verif_url = 'http://www.285200.com/Verif/Index'
body = 'account={username}&pwd={password}&code={code}'
mycookies = ''

headers = {
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Length': "66",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Host': "www.285200.com",
    'Origin': "http://www.285200.com",
    'Pragma': "no-cache",
    'Referer': "http://www.285200.com/",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest",
    'cache-control': "no-cache",
}

proxies = {

}

class RClient(object):
    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password.encode()).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('captcha.png', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers,timeout=30)
        return r.json()

    def rk_report_error(self, im_id):
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers,timeout=30)
        return r.json()

def get_ip(url):
    print('正在获取IP。。')
    try:
        response = requests.get(url)
        if response.status_code == 200:
            res_json = json.loads(response.text)
            if res_json['ERRORCODE'] == '0':
                ip = res_json['RESULT'][0]['ip']
                port = res_json['RESULT'][0]['port']
                ip_res = ip + ':' + port
                print('获取IP成功，当前IP为：',str(ip_res))
                return ip_res
            elif res_json['ERRORCODE'] == '10036' or res_json['ERRORCODE'] == '10038' or res_json['ERRORCODE'] == '10055':
                print('提前IP过快，5秒后重新请求', res_json)
                sleep(5)
                return get_ip(url)
            else:
                print('未知错误，5秒后重新请求',res_json)
                sleep(5)
                return get_ip(url)
    except RequestException:
        print('请求IP_url出错，正在重新请求',url)
        sleep(5)
        return get_ip(url)

def start():
    start_url = 'http://www.285200.com/Home/GetRedEnvelope?id=EhbdL7WlQNQ0x10'
    start_headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cache-Control': "no-cache",
        'Connection': "keep-alive",
        'Host': "www.285200.com",
        'Pragma': "no-cache",
        'Referer': "http://www.285200.com/Home/RedBagData?id=EhbdL7WlQNQ0x10",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        'cache-control': "no-cache",
        'Postman-Token': "4e5972b0-ee23-471b-b7ea-ab81ad8ac0e2"
    }
    resposne = requests.get(start_url,headers=start_headers,timeout=20,proxies=proxies)
    # print(resposne.text)

    this_url = 'http://www.285200.com/Login'
    this_headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Host': "www.285200.com",
    'Pragma': "no-cache",
    'Referer': "http://www.285200.com/Home/GetRedEnvelope?id=EhbdL7WlQNQ0x10",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'cache-control': "no-cache",
    }

    resposne = requests.get(this_url, headers=this_headers, timeout=20,proxies=proxies)
    # print(resposne.text)

def get_img():
    global mycookies
    response =requests.get(verif_url,timeout=20,proxies=proxies)
    with open('captcha.png','wb') as f:
        f.write(response.content)
    cookies = response.cookies.get_dict()
    cookies_str = 'ASP.NET_SessionId='+cookies['ASP.NET_SessionId']
    print(cookies_str)
    headers['cookie'] = cookies_str
    mycookies = cookies_str

def login(username,password,code):
    data = body.format(username=username,password=password,code=code)
    resposne = requests.post(login_url,headers=headers,data=data,timeout=20,proxies=proxies)
    print(resposne.text)
    if resposne.text == '1':
        print('登录成功')
    else:
        print('登录失败')

def logout():
    global mycookies
    logout_headers = {
        'Accept': "*/*",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cache-Control': "no-cache",
        'Connection': "keep-alive",
        'Host': "www.285200.com",
        'Pragma': "no-cache",
        'Referer': "http://www.285200.com/Login",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        'X-Requested-With': "XMLHttpRequest",
        'cache-control': "no-cache",
        'Postman-Token': "73432ae9-160b-4e03-9a04-d5bd6f807a1c"
    }
    logout_headers['Cookie'] = mycookies
    response = requests.get(logout_url,headers=logout_headers,timeout=20,proxies=proxies)
    print(response.text)
    if response.text == '1':
        print('退出成功')
    else:
        print('退出失败')


def main(useaname,password):
    global proxies
    ip = get_ip('http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=0b052d8bb1e645adb9eeb91e87502f71&orderno=YZ201812166028Tacx4Q&returnType=2&count=1')
    proxies = {
        'http': 'http://' + ip,
        'https': 'https://' + ip,
    }
    start()
    get_img()
        #qwer949 qq123456  118243  1ed8d3f0f613490ea9f01a85a17258a7
    rc = RClient('qwer949', 'qq123456', '118243', '1ed8d3f0f613490ea9f01a85a17258a7')
    with open('captcha.png', 'rb') as f:
        im = f.read()
    captcha_res = rc.rk_create(im, 3040)
    print(captcha_res)
    captcha_res = captcha_res['Result']
    login(useaname,password,captcha_res)
    logout()


if __name__ == '__main__':
    account_list = []
    with open('account.txt') as f:
        results = f.readlines()
        for res in results:
            account_list.append(res.strip())
    for account in account_list:
        print('当前账号：' + account)
        try:
            main(account,account)
        except:
            print('未知错误')