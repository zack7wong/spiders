#!/usr/bin/env python
# -*- coding:utf-8 -*-

import download
from lxml.etree import HTML
from lxml import etree
from urllib.parse import quote
import time
import json

city_list = [{'city':'东明石化1','id':'1668'},{'city':'东明石化2','id':'1696'},{'city':'东明中油燃料石化有限公司','id':'14095'}]

headers = {
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Length': "293",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Cookie': "autoLogin=null; user=null; pwd=null; ASP.NET_SessionId=mgo1ur55g1yfwvqjpz251hb4",
    'Host': "219.146.175.226:8406",
    'Origin': "http://219.146.175.226:8406",
    'Pragma': "no-cache",
    'Referer': "http://219.146.175.226:8406/webs/WasteWater/QueryAnalysis/HistoryReportQUIDYN/HistoryReport.aspx",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest",
    'cache-control': "no-cache",
    'Postman-Token': "3b25e77b-5ae3-47b5-82dc-f867322366a1"
    }

feiqi_url = 'http://219.146.175.226:8406/webs/ajax/WasteGas/QueryAnalysis/HistoryReportQUIDYN/HistoryReport.ashx'
feiqi_body = 'Method=QueryHistoryReport&subid={subid}&subname={subname}&start={start}&end={end}&index=1&sort=1&YWGS=&showValidate=0&multiCode=201%2C203%2C207%2C205%2C210&codes=201%2C203%2C207%2C209%2C525%2C210%2C545%2C546%2C205%2C221&showUpload=0&page=1&rows=20'

#东明石化集团 1671
feishui_url = 'http://219.146.175.226:8406/webs/ajax/WasteWater/QueryAnalysis/HistoryReportQUIDYN/HistoryReport.ashx'
feishui_body = 'Method=QueryHistoryReport&subid=1671&subname=%E4%B8%9C%E6%98%8E%E7%9F%B3%E5%8C%96%E9%9B%86%E5%9B%A2&start={start}&end={end}&index=1&sort=1&showValidate=0&multiCode=311%2C313%2C316%2C466%2C494&showUpload=0&YWGS=&codes=302%2C311%2C316%2C494%2C495&page=1&rows=20'

def read():
    #2018-12-18national
    item_list = []
    now_date = time.strftime('%Y-%m-%d',time.localtime())
    filename = str(now_date)+'national.csv'
    try:
        with open(filename) as f:
            resutls = f.readlines()
            for res in resutls:
                cityname = res.split(',')[0]
                hour = res.split(',')[4]
                obj = cityname+hour
                item_list.append(obj)
    except:
        pass

    return item_list

def start():
    start_date = time.strftime('%Y-%m-%d+%H:00:00', time.localtime(time.time()-3600))
    end_date = time.strftime('%Y-%m-%d+%H:59:59', time.localtime(time.time()-3600))
    print(start_date)

    save_res = '公司,时间点,二氧化硫实测浓度,二氧化硫折算浓度,二氧化硫排放量,氮氧化物实测浓度,氮氧化物折算浓度,氮氧化物排放量,颗粒物实测浓度,颗粒物折算浓度,颗粒物排放量,氧含量,烟气温度,废气排放量\n'
    with open('结果.csv','w') as f:
        f.write(save_res)

    for city in city_list:
        data = feiqi_body.format(subid=city['id'],subname=quote(city['city']),start=start_date,end=end_date)
        response = down.get_html(feiqi_url,method='post',headers=headers,data=data)
        if response:
            json_obj = json.loads(response.text)
            if len(json_obj['rows'])>0:
                val_201 = json_obj['rows'][0]['val_201']
                cvt_201 = json_obj['rows'][0]['cvt_201']
                ex_201 = json_obj['rows'][0]['ex_201']

                val_203 = json_obj['rows'][0]['val_203']
                cvt_203 = json_obj['rows'][0]['cvt_203']
                ex_203 = json_obj['rows'][0]['ex_203']

                val_207 = json_obj['rows'][0]['val_207']
                cvt_207 = json_obj['rows'][0]['cvt_207']
                ex_207 = json_obj['rows'][0]['ex_207']

                val_209 = json_obj['rows'][0]['val_209']
                val_525 = json_obj['rows'][0]['val_525']
                val_210 = json_obj['rows'][0]['val_210']

                save_res = city['city']+','+str(start_date)+','+val_201+','+cvt_201+','+ex_201+','+val_203+','+cvt_203+','+ex_203+','+val_207+','+cvt_207+','+ex_207+','+val_209+','+val_525+','+val_210+'\n'
                print(save_res)
                with open('结果.csv','a') as f:
                    f.write(save_res)

    #废水
    with open('结果.csv', 'a') as f:
        f.write('\n公司,时间点,化学需氧量浓度,化学需氧量排放量,氨氮浓度,氨氮排放量,小时流量,PH\n')

    data = feishui_body.format(start=start_date, end=end_date)
    response = down.get_html(feishui_url, method='post', headers=headers, data=data)
    if response:
        json_obj = json.loads(response.text)
        if len(json_obj['rows']) > 0:
            val_316 = json_obj['rows'][0]['val_316']
            flow_316 = json_obj['rows'][0]['flow_316']

            val_311 = json_obj['rows'][0]['val_311']
            flow_311 = json_obj['rows'][0]['flow_311']

            val_494 = json_obj['rows'][0]['val_494']
            PH = ''

            save_res = city['city'] + ',' + str(start_date) + ',' + val_316 + ',' + flow_316 + ',' + val_311 + ',' + flow_311+','+val_494+','+PH+'\n'
            print(save_res)
            with open('结果.csv', 'a') as f:
                f.write(save_res)

if __name__ == '__main__':
    #hb 1703
    down = download.Download()
    while True:
        start()
        print('该轮已经跑完,20分钟获取一次。。程序在后台运行请不要关闭')
        time.sleep(60*20)

