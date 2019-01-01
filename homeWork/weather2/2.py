#!/usr/bin/env python
# -*- coding:utf-8 -*-

item_list = []
for i in range(3,8):
    filename = '塔城201'+str(i)+'.csv'
    with open(filename) as f:
        results =f.readlines()
        for res in results:
            item_list.append(res)
max_date = ''
max_qiqen = 0
min_date = ''
min_qiqen = 0
max_wencha_date = ''
max_wencha = 0
for item in item_list:
    my_date = item.split(',')[0]
    my_max_qiwen = int(item.split(',')[1])
    my_min_qiwen = int(item.split(',')[2])
    my_wencha = my_max_qiwen - my_min_qiwen
    if my_max_qiwen > max_qiqen:
        max_qiqen = my_max_qiwen
        max_date = my_date
    if my_min_qiwen < min_qiqen:
        min_qiqen = my_min_qiwen
        min_date = my_date

    if my_wencha > max_wencha:
        max_wencha = my_wencha
        max_wencha_date = my_date

print('5年中最高气温是：'+max_date+' 温度是 '+str(max_qiqen))
print('5年中最低气温是：'+min_date+' 温度是 '+str(min_qiqen))
print('5年中温差变化最大的是：'+max_wencha_date+' 温差是 '+str(max_wencha))