#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json

url = "https://wx2.zj.sgcc.com.cn/ldx/wechat3/customer/notice/searchN.do"

payload = "event=191&areaNo=330500"
headers = {
    'Host': "wx2.zj.sgcc.com.cn",
    'Connection': "keep-alive",
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Origin': "https://wx2.zj.sgcc.com.cn",
    'X-Requested-With': "XMLHttpRequest",
    'User-Agent': "Mozilla/5.0 (Linux; Android 6.0.1; Redmi 3S Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044306 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060739) NetType/WIFI Language/zh_CN",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Referer': "https://wx2.zj.sgcc.com.cn/ldx/static/wechat3/customer/notice-blackout203.html",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,en-US;q=0.8",
    'Cookie': "SESSION=b8f1cede-4d11-44b6-8ad9-027bf9278377; LDXAPISRV=w236|XDv4E|XDv4E; _wx_zj_ldx_session_id_=535756555651565252525056533d0d2a522508080e232e040d1325035105182b5b5b3d56270d2f181337; LDXSRV=w164|XDv4G|XDv4E",
    'Content-Length': "23",
    'cache-control': "no-cache",
}

response = requests.request("POST", url, data=payload, headers=headers)

# print(response.text)
json_obj = json.loads(response.text)

with open('结果.csv','w') as f:
    f.write('停电时间,预计送电时间,影响范围\n')
for data in json_obj['ret']['list']:
    startTime = data['startTime']
    stopTime = data['stopTime']
    scope = data['scope']

    save_res = startTime+'||'+stopTime+'||'+scope+'\n'
    save_res = save_res.replace(',','，').replace('||','，')
    print(save_res)
    with open('结果.csv','a') as f:
        f.write(save_res)