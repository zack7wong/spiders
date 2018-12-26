#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import json
import time

url = 'http://www.cbooo.cn/BoxOffice/getCBD?pIndex=1&dt={mydate}'
mydate = time.strftime('%Y-%m-%d',time.localtime(time.time()-60*60*24))

response = requests.get(url.format(mydate=mydate))
json_obj = json.loads(response.text)
for data in json_obj['data1']:
    CinemaName = data['CinemaName']
    TodayBox = data['TodayBox']
    TodayShowCount = data['TodayShowCount']
    AvgPeople = data['AvgPeople']
    price = data['price']
    Attendance = data['Attendance']
    print(CinemaName,TodayBox,TodayShowCount,AvgPeople,price,Attendance)
