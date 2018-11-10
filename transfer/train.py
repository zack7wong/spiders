#!/usr/bin/env python
# -*- coding:utf-8 -*-

import db
import config
import download
import json
import math
import time

class Train(object):
    def __init__(self):
        self.mysql = db.MysqlClient()

    def get_site(self):
        sql = "select * from site"
        results = self.mysql.find_all(sql)
        return results

    def judge(self,results):
        return_res = []
        for res in results:
            for city in config.CITY:
                if city in res[2]:
                    return_res.append(res)

        return return_res

    def get_results(self,start_url,start,end,datetime):
        down = download.Download()
        response = down.get_html(start_url)
        if response:
            try:
                json_obj = json.loads(response.text)
                if len(json_obj['data']['result']) == 0:
                    print('no results..')
                    return None
                for data in json_obj['data']['result']:
                    item = data.split('|')

                    datetime = datetime
                    startStation = start[2]
                    endStation = end[2]
                    startStationNum = start[3]
                    endStationNum = end[3]
                    trainName = item[3]
                    startTime = item[8]
                    endTime = item[9]
                    duration = item[10]

                    try:
                        durDate = int(duration.split(':')[0])
                        arrivalDate = str(math.ceil(durDate/24))
                    except:
                        arrivalDate = ''

                    if '列车停运' in data:
                        status = '0'
                    else:
                        status = '1'
                    resultsStr = data
                    ts = time.strptime(datetime, "%Y-%m-%d")
                    timestamp = str(int(time.mktime(ts)))
                    # print(datetime,startStation,endStation,startStationNum,endStationNum,trainName,startTime,endTime,duration,arrivalDate,status,resultsStr,timestamp)
                    sql = "insert into results(datetime,startStation,endStation,startStationNum,endStationNum,trainName,startTime,endTime,duration,arrivalDate,status,resultsStr,timestamp) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
                          %(datetime,startStation,endStation,startStationNum,endStationNum,trainName,startTime,endTime,duration,arrivalDate,status,resultsStr,timestamp)+ "ON DUPLICATE KEY UPDATE startTime='%s', endTime='%s'"%(startTime,endTime)
                    print(sql)
                    self.mysql.save(sql)
            except:
                print('未知错误')
                with open('fail.txt', 'a') as f:
                    f.write(start_url+'\n')

