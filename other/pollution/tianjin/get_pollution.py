#!/usr/bin/env python
# -*- coding:utf-8 -*-

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import math
import db

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

def parse(item,ald_json_obj):
    for json_obj in ald_json_obj['rows']:
        name = json_obj['QYMC']
        pollutionType = json_obj['XMLX']
        addressName = json_obj['JCDMC']
        checkTime = json_obj['JCRQ']+' '+json_obj['JCSJ']
        checkName = json_obj['ZBMC']
        checkRes = json_obj['ZSND']
        biaozhunxianzhi = json_obj['BZXZ']
        danwei = json_obj['DW']
        shifouchaobiao = json_obj['SFCB']
        chaobiaobeishu = json_obj['CBBS']
        pingjiabiaozhun = json_obj['BZMC']

        print(name,pollutionType,addressName,checkTime,checkName,checkRes,biaozhunxianzhi,danwei,shifouchaobiao,chaobiaobeishu,pingjiabiaozhun)
        sql = "insert into tianjin(name,pollutionType,addressName,checkTime,checkName,checkRes,biaozhunxianzhi,danwei,shifouchaobiao,chaobiaobeishu,pingjiabiaozhun)" \
                      " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                      % (name,pollutionType,addressName,checkTime,checkName,checkRes,biaozhunxianzhi,danwei,shifouchaobiao,chaobiaobeishu,pingjiabiaozhun)
        dbclient.save(sql)



def start(item):
    url = 'http://60.30.64.234:8888/PollutionMonitor-tj/publishZXJGlist.do?ID='+item['id']

    #获取第一页
    data = 'page=1&rows=10'

    try:
        response = requests.post(url, headers=headers, data=data,timeout=10)
    except:
        return
    print(response.text)
    json_obj = json.loads(response.text)
    if json_obj['total'] == 0:
        return

    #处理第一页
    print('当前页：1')
    parse(item,json_obj)

    #获取总页数
    totalCount = json_obj['total']
    totalPage = math.ceil(totalCount/10)

    #获取剩余页数
    for i in range(2,totalPage+1):
        print('当前页：'+str(i))
        data = 'page={page}&rows=10'.format(page=i)
        try:
            response = requests.post(url, headers=headers, data=data,timeout=10)
        except:
            continue
        json_obj = json.loads(response.text)
        parse(item, json_obj)




if __name__ == '__main__':
    dbclient = db.MysqlClient()
    item_list = []
    with open('tianjin_id.txt') as f:
        results = f.readlines()
        for res in results:
            id = res.split(',')[0]
            name = res.split(',')[1].strip()
            obj ={
                'id':id,
                'name':name,
            }
            item_list.append(obj)
    for item in item_list:
        print(item)
        try:
            start(item)
        except:
            continue
        # break