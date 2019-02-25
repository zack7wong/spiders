#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json

headers = {
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    # 'Content-Length': "14",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Cookie': "JSESSIONID=86BD2B085C0C0956CB01CFE16CC1786A",
    'Host': "60.30.64.234:8888",
    'Origin': "http://60.30.64.234:8888",
    'Pragma': "no-cache",
    'Referer': "http://60.30.64.234:8888/PollutionMonitor-tj/publish.do",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest",
    'cache-control': "no-cache",
}

def start():
    for i in range(1,21):
        url = 'http://60.30.64.234:8888/PollutionMonitor-tj/publishEnterpriseList.do'
        data = 'page={page}&rows=20'.format(page=i)
        response = requests.post(url,data=data,headers=headers)
        print(response.text)

        json_obj = json.loads(response.text)
        for data in json_obj['rows']:
            comid = data['ID']
            name = data['QYMC']
            with open('tianjin_id.txt','a') as f:
                f.write(comid+','+name+'\n')



if __name__ == '__main__':
    start()