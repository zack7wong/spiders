#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random


month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
day = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
mynum = input('请输入班级数')
account = 0
for ci in range(0,int(mynum)):
    item_list = []
    for i in range(0,23):
        mymonth = random.sample(month,1)
        myday = random.sample(day,1)
        res = mymonth[0]+myday[0]
        item_list.append(res)
    print(item_list)
    res_list = list(set(item_list))
    print(len(res_list))
    if len(res_list)!=len(item_list):
        account+=1
print('生日相同的概率有：'+str(account/int(mynum)))