#!/usr/bin/env python
# -*- coding:utf-8 -*-

import db
import datetime as dtime

class Calculation(object):
    def __init__(self):
        self.one_results_list = []
        self.mysql = db.MysqlClient()

    def start(self):
        startStation = input('请输入起始站： ')
        trainStation = input('请输入换乘站： ')
        endStation = input('请输入终点站： ')
        datetime = input('请输入出发日期(eg:2018-11-12)： ')
        startTime = input('请输入出发时间(eg:09:00)： ')
        trainTime = input('请输入换乘间隔时间，单位为小时(eg:2)： ')
        # startStation = '广州'
        # trainStation = '深圳'
        # endStation = '福州'
        # datetime = '2018-11-12'
        # startTime = '09:00'
        # trainTime = '2'
        self.get_one(startStation,trainStation,datetime,startTime)
        self.get_two(trainStation,endStation,datetime,startTime,trainTime)

    def get_one(self, startStation, trainStation,datetime,startTime):
        sql = "select * from results where (startStation like '%s' and endStation like '%s' and datetime='%s')"%(startStation+'%', trainStation+'%',datetime)
        results = self.mysql.find_all(sql)
        print('\n')
        print('############### 符合换乘的列车有 ###################')
        print('\n')
        for res in results:
            if startTime < res[7]:
                # print('车次:'+res[6]+'   起始站:' + res[2] + '   终点站:' + res[3] + '   出发时间:' + res[7] + '   到达时间:' + res[8] + '   时长:' + res[9])
                obj = {
                    'datetime':datetime,
                    'startStation': res[2],
                    'endStation': res[3],
                    'trainName': res[6],
                    'startTime': res[7],
                    'endTime': res[8],
                    'duration': res[9]
                }
                self.one_results_list.append(obj)
                break

    def get_two(self,trainStation,endStation,datetime,startTime,trainTime):
        for res in self.one_results_list:
            timeStr = datetime + ' ' + res['startTime']
            gohour = res['duration'].split(':')[0]
            gominute = res['duration'].split(':')[1]
            arriveday,trainday = self.tran_time(timeStr=timeStr, gohour=gohour,gominute=gominute,trainTime=trainTime)
            trainday_datetime = trainday.split(' ')[0]
            trainday_hourminute = trainday.split(' ')[1]
            sql = "select * from results where (startStation like '%s' and endStation like '%s' and datetime='%s')" % (trainStation + '%', endStation + '%', trainday_datetime)
            sql_results = self.mysql.find_all(sql)
            for sql_res in sql_results:
                if trainday_hourminute > sql_res[7]:
                    print('车次:' + res['trainName'] + ' ' + res['startStation'] + '->' + res['endStation']+ ' 出发时间:' + res['startTime'] + ' 到达时间:' + arriveday + ' ==> ' +
                          '车次:' + sql_res[6] + ' ' + sql_res[2] + '->' + sql_res[3] + ' 出发时间:' + sql_res[7])
                    print('\n')

    def tran_time(self,timeStr,gohour,gominute,trainTime):
        year,month,day,hour,minute = self.split_time(timeStr)
        arriveday = (dtime.datetime(year, month, day, hour, minute) + dtime.timedelta(hours=int(gohour),minutes=int(gominute))).strftime('%Y-%m-%d %H:%M')
        year, month, day, hour, minute = self.split_time(arriveday)
        trainday = (dtime.datetime(year, month, day, hour, minute) + dtime.timedelta(hours=int(trainTime))).strftime('%Y-%m-%d %H:%M')
        return arriveday,trainday

    def split_time(self, timeStr):
        year = int(timeStr.split('-')[0])
        month = int(timeStr.split('-')[1])
        day = int(timeStr.split('-')[2].split(' ')[0])
        hour = int(timeStr.split(':')[0].split(' ')[1])
        minute = int(timeStr.split(':')[1])
        return year,month,day,hour,minute
