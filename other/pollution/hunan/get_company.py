#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json

headers = {
    'Pragma': "no-cache",
    'Origin': "http://123.127.175.61:6375",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Cache-Control': "no-cache",
    'X-Requested-With': "XMLHttpRequest",
    'Cookie': "JSESSIONID=05EE09302F239DF386280923A2B01213; insert_cookie_cnemc=94955953",
    'Connection': "keep-alive",
    'Referer': "http://123.127.175.61:6375/eap/hb/homeHb/home_qyjcxx.jsp?id=430000",
    'cache-control': "no-cache",
    'Postman-Token': "1245dad0-659a-42ea-b06c-ce00add0969a"
    }

def start():
    for i in range(168,228):
        url = 'http://123.127.175.61:6375/eap/dtcxAction/qydtcxqx_new.action?'
        body = 'provinceQ4=430000&cityQ4=&countyQ4=&hbSjcjQyJbxx.qymc=&hbSjcjQyJbxx.qylb=&hylb_view=&hbSjcjQyJbxx.hylb=&jumpPage={pageToken}&pageNo={pageToken}&interval=10&total=&totalPage=192&adminjibie=11&province=%E6%B9%96%E5%8D%97%E7%9C%81&city=&county=&provinceid=430000&cityid=&countyid=&provinceSelected=430000&citySelected=&countySelected=&hbSjcjQyJbxx.ztx=100&hbSjcjQyJbxx.sjlb=hbSjcjQyJbxxList'
        data = body.format(pageToken=i)
        response = requests.post(url,headers=headers,data=data)
        print(response.text)
        json_obj = json.loads(response.text)

        for data in json_obj['features']:
            sheng = data['sheng']  if data['sheng'] else ''
            shi = data['shi']  if data['shi'] else ''
            xian = data['xian'] if data['xian'] else ''
            id = data['id']
            title = data['qymc']
            comType = data['qylb'] if data['qylb'] else ''

            save_res = id+','+title+','+comType+','+sheng+','+shi+','+xian+'\n'
            print(save_res)
            with open('hunan_id.txt','a') as f:
                f.write(save_res)

        # break

if __name__ == '__main__':
    start()