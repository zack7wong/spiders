#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
import time
import re
import requests
from lxml.etree import HTML
from urllib.parse import quote

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    # 'Content-Length': "183",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cookie': "has_recent_activity=1; _ga=GA1.2.1717930341.1550648857; tz=Asia%2FShanghai; _octo=GH1.1.184711898.1550648859; _gat=1; logged_in=no; _gh_sess=MmFsTTFxRW9XeUh6ZDVpVTI3U0RxSW1HQVp6TUtmN3BOUkFDUkIwSzUyM3Z2clJsT1pLZTQyMTlCUm0wYjlZT0d3Q0hYaGh0R0ViMXliS0VNU0RHOGx6L2FzV3Qra1B2NmVaSzFKT2N0M1NKY0ExZktRbG1sSDdGZXdyZTZMZWs5bEsrSXI4bVlRNmVjS0I2dkZsV0NuaVRnaU9CbGwzd0JvTFdCdm1pcnFYYVI4T3hlVFQrUGR5UFRxeEtlUThreXpvT09tREc1b2hPclN1SitYL1R2djVVelpBdm54WE5Oc3dsNXRQblk1SWx6SDlBZlFpeVJrdWErMDZnVzF6R0lCOEZ2d1d4WVVoMmVEWXEyZEJLN3lIbGUxbTR2NjMwSFQydkZXVFpZVVZ4L0tsY1VmNjdEek9iZExva1NkdEUtLXVEem11ZmlkUGR6Z2JucUNPamNuTkE9PQ%3D%3D--787282043f2d74298819050b2b7e072271cac9f2",
    'Host': "github.com",
    'Origin': "https://github.com",
    'Pragma': "no-cache",
    'Referer': "https://github.com/login",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    'cache-control': "no-cache",
}

def reg():

    driver = webdriver.Chrome()
    driver.get('https://github.com/join?source=header-home')
    driver.find_element_by_css_selector('#user_login').send_keys(username)
    driver.find_element_by_css_selector('#user_email').send_keys(email)
    driver.find_element_by_css_selector('#user_password').send_keys(password)

    driver.find_element_by_css_selector('#signup_button').click()

    #检测是否注册完成
    flag = 0
    while True:
        cookies = driver.get_cookies()
        # print(cookies)
        for cookie in cookies:
            if cookie['name'] == 'logged_in':
                if cookie['value'] == 'yes':
                    flag += 1

            if cookie['name'] == 'dotcom_user':
                if cookie['value'] == username:
                    flag += 1

        if flag == 2:
            print('已注册完成！')
            break
        print('注册尚未完成。。')
        time.sleep(3)

def login():
    # 昵称：adse12143
    # 密码：sf32sa12
    # 邮箱：safw32@163.com
    response = requests.get('https://github.com/login',headers=headers)
    authenticity_token =re.search('<input type="hidden" name="authenticity_token" value="(.*?)"',response.text)
    authenticity_token = authenticity_token.group(1)
    authenticity_token = quote(authenticity_token)
    print(authenticity_token)

    # cookiesDic = response.cookies.get_dict()
    # cookieStr = '_gh_sess='+cookiesDic['_gh_sess']
    # print(cookieStr)
    # headers['Cookie'] = cookieStr

    login_url = 'https://github.com/session'
    body = 'commit=Sign+in&utf8=%E2%9C%93&authenticity_token={authenticity_token}&login={username}&password={password}'
    data = body.format(authenticity_token=authenticity_token,username=username,password=password)
    response = requests.post(login_url, headers=headers, data=data)
    cookiesDic = response.cookies.get_dict()
    # print(cookiesDic)
    if 'user_session' in cookiesDic:
        print('登录成功')
        print('登录成功返回的session：' + cookiesDic['user_session'])

def get_info():
    url = 'https://github.com/trending/developers?since=weekly'
    response = requests.get(url,headers=headers)
    # print(response.text)
    html = HTML(response.text)
    name_list = html.xpath('//div[@class="explore-content"]//li//h2/a/@href')
    for name in name_list:
        print(name[1:].strip())

def start():
    reg()

    print('正在登录。。。')
    login()

    print('获取数据。。。')
    get_info()

if __name__ == '__main__':
    print('正在注册。。。')
    username = input('请输入注册昵称：')
    password = input('请输入注册密码：')
    email = input('请输入注册邮箱：')
    start()