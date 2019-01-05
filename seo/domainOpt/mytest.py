#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     mytest
   Description :
   Author :        hayden_huang
   Date：          2019/1/5 19:31
-------------------------------------------------
"""

import requests
import time

url = "https://m.ys7.com/passport/captcha.html"

querystring = {"t":"1546687896864"}

payload = "mobile=15768653529&code=&_csrf=QWt0MzFGcGhyJRNVVRQHATQTPVcGGQI8GFouW2cuKT4ODAIHCRIpXw%3D%3D"
headers = {
    'Accept': "application/json",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Length': "91",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cookie': "SS=cn5j2hq2t42ao9sj1g42svff15; track_identity=929329b917caab8f530e1dca4a7abbe5; _csrf=a9336f0592a4e8e35fed33257697cf45a252ba8742392048cc17310ca7c05fe9a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%223NgfdRwiuxId7_rTY1ZhVhYVOgv48TY7%22%3B%7D",
    'Host': "m.ys7.com",
    'Origin': "https://m.ys7.com",
    'Pragma': "no-cache",
    'Referer': "https://m.ys7.com/passport/register.html?come=dealer&dealer_id=1570203",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest",
    'cache-control': "no-cache",
    'Postman-Token': "9c7062b8-c12c-4edc-8170-db40be1befba"
    }

while True:
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    print(response.text)
    time.sleep(60)