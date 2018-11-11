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
                if city == res[2]:
                    return_res.append(res)
                # if city in res[2]:
                #     return_res.append(res)

        return return_res

    def get_stationName(self,stationNum):
        sql = "select * from site where transferid = '%s'"%(stationNum)
        results = self.mysql.find_one(sql)
        return results

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
                    startStation = self.get_stationName(item[6])[2]
                    endStation = self.get_stationName(item[7])[2]
                    startStationNum = item[6]
                    endStationNum = item[7]
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
                    timestampStr = datetime + ' ' + startTime

                    if startTime[0:2] == '24':
                        timestampStr = datetime
                        ts = time.strptime(timestampStr, "%Y-%m-%d")
                        timestamp = str(int(time.mktime(ts)) + 86400)
                    else:
                        ts = time.strptime(timestampStr, "%Y-%m-%d %H:%M")
                        timestamp = str(int(time.mktime(ts)))

                    # print(datetime,startStation,endStation,startStationNum,endStationNum,trainName,startTime,endTime,duration,arrivalDate,status,resultsStr,timestamp)
                    sql = "insert into results(datetime,startStation,endStation,startStationNum,endStationNum,trainName,startTime,endTime,duration,arrivalDate,status,resultsStr,timestamp) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
                          %(datetime,startStation,endStation,startStationNum,endStationNum,trainName,startTime,endTime,duration,arrivalDate,status,resultsStr,timestamp)+ "ON DUPLICATE KEY UPDATE startTime='%s', endTime='%s',timestamp='%s'"%(startTime,endTime,timestamp)
                    print(sql)
                    self.mysql.save(sql)
            except:
                print('未知错误')
                with open('fail.txt', 'a') as f:
                    f.write(start_url+'\n')

