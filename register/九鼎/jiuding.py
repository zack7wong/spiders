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
import re
from requests import RequestException
from time import sleep
from lxml.etree import HTML



mycookies = ''
myauth = ''



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
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers,
                          timeout=30)
        return r.json()

    def rk_report_error(self, im_id):
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers, timeout=30)
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
                print('获取IP成功，当前IP为：', str(ip_res))
                return ip_res
            elif res_json['ERRORCODE'] == '10036' or res_json['ERRORCODE'] == '10038' or res_json[
                'ERRORCODE'] == '10055':
                print('提前IP过快，5秒后重新请求', res_json)
                sleep(5)
                return get_ip(url)
            else:
                print('未知错误，5秒后重新请求', res_json)
                sleep(5)
                return get_ip(url)
    except RequestException:
        print('请求IP_url出错，正在重新请求', url)
        sleep(5)
        return get_ip(url)



def get_img():
    global mycookies

    verify_url = 'http://www.jiuding288.com/Home/login/verify.html'
    verify_response = requests.get(verify_url,timeout=20, proxies=proxies)
    thiscookie = verify_response.cookies.get_dict()
    thiscookie = 'PHPSESSID=' + thiscookie['PHPSESSID']

    with open('captcha.png', 'wb') as f:
        f.write(verify_response.content)

    mycookies = thiscookie
    print(mycookies)


def login(username, password, code):
    global myauth
    #13469473606
    headers = {
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cache-Control': "no-cache",
        'Connection': "keep-alive",
        # 'Content-Length': "77",
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        # 'Cookie': "PHPSESSID=045htilrjvru2eal6h3egberv4",
        'Host': "www.jiuding288.com",
        'Origin': "http://www.jiuding288.com",
        'Pragma': "no-cache",
        'Referer': "http://www.jiuding288.com/Home/Index/index.html",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        'X-Requested-With': "XMLHttpRequest",
        'cache-control': "no-cache",
    }

    login_url = 'http://www.jiuding288.com/home/Login/logined'
    body = 'ltype=1&type=0&newview=1&account={username}&passwd={password}&pic_code={code}'
    headers['cookie'] = mycookies

    data = body.format(username=username, password=password, code=code)
    resposne = requests.post(login_url, headers=headers, data=data, timeout=20, proxies=proxies)
    json_obj = json.loads(resposne.text)
    print(json_obj)
    if json_obj['status'] == 1:
        thiscookie = resposne.cookies.get_dict()
        thiscookie = 'auth=' + thiscookie['auth']
        myauth = thiscookie
        print('登录成功')
    else:
        print('登录失败')


def click(start_url):
    myheaders = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cache-Control': "no-cache",
        'Connection': "keep-alive",
        # 'Cookie': "PHPSESSID=045htilrjvru2eal6h3egberv4; auth=35a19df9a94eaf8b0538fdfaf3e70047%3Aa56fb68b45bcdc67d4230b9c213c0534",
        'Host': "www.jiuding288.com",
        'Pragma': "no-cache",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        'cache-control': "no-cache",
    }
    myheaders['Cookie'] = mycookies
    myheaders['Cookie'] += ';'+ myauth
    response = requests.get(start_url, headers=myheaders, timeout=20, proxies=proxies)
    html = HTML(response.text)
    content = html.xpath('string(//p[@class="cue"])')
    yuer = html.xpath('string(//p[@class="point"])')
    print(content)
    print(yuer.strip())

def logout(start_url):
    global mycookies,myauth
    logout_headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cache-Control': "no-cache",
        'Connection': "keep-alive",
        # 'Cookie': "PHPSESSID=045htilrjvru2eal6h3egberv4; auth=35a19df9a94eaf8b0538fdfaf3e70047%3Aa56fb68b45bcdc67d4230b9c213c0534",
        'Host': "www.jiuding288.com",
        'Pragma': "no-cache",
        # 'Referer': "http://www.xsj280.com/home/usercenter/redpack/rid/RR812MGW82HOX96TD2EZ",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        'cache-control': "no-cache",
    }
    logout_url = 'http://www.jiuding288.com/Home/Login/logout.html'
    logout_headers['Referer'] = start_url
    logout_headers['Cookie'] = mycookies
    logout_headers['Cookie'] += ';'+ myauth
    response = requests.get(logout_url, headers=logout_headers, timeout=20, proxies=proxies,allow_redirects=False)
    if response.status_code == 302:
        print('退出成功')
    else:
        print('退出失败')


def main(useaname, password, start_url):
    global proxies
    with open('讯代理.txt') as f:
        dingdan = f.read()

    with open('若快.txt') as f:
        readRes = f.read().strip()
        ruokuai_name = readRes.split(',')[0]
        ruokuai_password = readRes.split(',')[1]
        ruokuai_id = int(readRes.split(',')[2])
        ruokuai_md5 = readRes.split(',')[3]

    ip = get_ip(dingdan.strip())
    proxies = {
        'http': 'http://' + ip,
        'https': 'https://' + ip,
    }

    get_img()

    # qwer949 qq123456  118243  1ed8d3f0f613490ea9f01a85a17258a7

    # print(ruokuai_name, ruokuai_password, ruokuai_id, ruokuai_md5)
    rc = RClient(ruokuai_name, ruokuai_password, ruokuai_id, ruokuai_md5)
    with open('captcha.png', 'rb') as f:
        im = f.read()
    captcha_res = rc.rk_create(im, 3040)
    print(captcha_res)
    captcha_res = captcha_res['Result']
    login(useaname, password, captcha_res)
    click(start_url)
    logout(start_url)


if __name__ == '__main__':
    #http://www.xsj280.com/home/usercenter/redpack/rid/RR812MGW82HOX96TD2EZ
    # start_url = input('请输入链接：')
    with open('链接.txt') as f:
        start_url = f.read().strip()
    print('当前链接：'+start_url)
    # start_url = 'http://www.jiuding288.com/home/usercenter/redpack/rid/DA4R5O099IZIYAJCHQ87'
    account_list = []
    with open('手机号.txt') as f:
        results = f.readlines()
        for res in results:
            account_list.append(res.strip())
    for account in account_list:
        print('当前账号：' + account)
        try:
            main(account, account, start_url)
        except:
            print('未知错误')
