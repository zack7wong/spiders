#!/usr/bin/env python
# -*- coding:utf-8 -*-

weekDic = {'星期一':['1','6'],'星期二':['2','7'],'星期三':['3','8'],'星期四':['4','9'],'星期五':['5','0']}

carNum = input('请输入车牌号')
carNum = carNum[-1]

for item in weekDic.keys():
    if carNum in weekDic[item]:
        print('是'+item+'限行')