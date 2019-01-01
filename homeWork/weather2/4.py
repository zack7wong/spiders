#!/usr/bin/env python
# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt

item_list = []
with open('塔城2015.csv') as f:
    results = f.readlines()
    for res in results:
        fengxiang = res.split(',')[4]
        item_list.append(fengxiang)

print(set(item_list))
List_set = set(item_list)
name_list = []
num_list = []
for item in List_set:
    # print(item)
    # print(pinpaiList.count(item))
    name_list.append(item)
    num_list.append(item_list.count(item))

print(name_list)
print(num_list)

plt.rcParams['font.sans-serif'] = 'SimHei'
fig = plt.figure()

plt.pie(num_list, labels=name_list, autopct='%1.1f%%')  # 画饼图

plt.savefig("饼图.jpg")
plt.show()
