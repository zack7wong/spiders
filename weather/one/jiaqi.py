#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     jiaqi
   Description :
   Author :        hayden_huang
   Date：          2018/11/30 18:40
-------------------------------------------------
"""
import json
import requests

jiaqi_list = []
all_list = []

year_list = ['2015','2016','2017','2018']
month_list = ['01','02','03','04','05','06','07','08','09','10','11','12']
day_list = []

url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query={mydate}&co=&resource_id=6018&t=1543507095724&ie=utf8&oe=gbk'
for year in year_list:
    for month in month_list:
        date_str = year+'年'+month+'月'
        start_url = url.format(mydate=date_str)
        print(start_url)
        response = requests.get(start_url)
        json_obj = json.loads(response.text)
        try:
            for onedata in json_obj['data'][0]['holiday']:
                for data in onedata['list']:
                    if data['status'] == '1':
                        thisyear = data['date'].split('-')[0]
                        thismonth = data['date'].split('-')[1]
                        thisday = data['date'].split('-')[2]
                        if len(thismonth) == 1:
                            thismonth = '0'+thismonth

                        if len(thisday) == 1:
                            thisday = '0' + thisday

                        save_res = thisyear + '-' + thismonth + '-' + thisday
                        print(save_res)
                        jiaqi_list.append(save_res)
        except:
            pass



        for data in json_obj['data'][0]['almanac']:
            thisyear = data['date'].split('-')[0]
            thismonth = data['date'].split('-')[1]
            thisday = data['date'].split('-')[2]
            if len(thismonth) == 1:
                thismonth = '0' + thismonth

            if len(thisday) == 1:
                thisday = '0' + thisday

            save_res = thisyear + '-' + thismonth + '-' + thisday
            all_list.append(save_res)


for data in all_list:
    if data in jiaqi_list:
        with open('jiaqi.csv', 'a') as f:
            f.write(data+','+'1'+'\n')
    else:
        with open('jiaqi.csv', 'a') as f:
            f.write(data + ',' + '0' + '\n')