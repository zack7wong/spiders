#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
from time import sleep
from requests import RequestException

#是否开启代理
proxy_on = True

#代理url
proxy_url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=c31c7f8986124188b7ef9f164aa37e5a&orderno=YZ20181219934NkS8qm&returnType=2&count=1'


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