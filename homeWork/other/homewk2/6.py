#!/usr/bin/env python
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd

with open('data.csv') as f:
    results = f.readlines()
    tongxinList = []
    pinpaiList = []
    for res in results[1:]:
        tongxin = res.split(',')[3]
        pinpai = res.split(',')[2]
        tongxinList.append(tongxin)
        pinpaiList.append(pinpai)


shenzhouxingNum = 0
donggandidaiNum = 0
quanqiutongNum = 0
for tongxin in tongxinList:
    if tongxin == '神州行':
        shenzhouxingNum+=1
    if tongxin == '动感地带':
        donggandidaiNum+=1
    if tongxin == '全球通':
        quanqiutongNum +=1
# plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
labels = ['神州行', '动感地带', '全球通']
X = [shenzhouxingNum, donggandidaiNum, quanqiutongNum]
fig = plt.figure()

plt.pie(X, labels=labels, autopct='%1.2f%%')  # 画饼图
plt.show()
plt.savefig("饼图.jpg")


#柱状图
List_set = set(pinpaiList) #List_set是另外一个列表，里面的内容是List里面的无重复 项
name_list = []
num_list = []
for item in List_set:
    # print(item)
    # print(pinpaiList.count(item))
    name_list.append(item)
    num_list.append(pinpaiList.count(item))

plt.bar(range(len(num_list)), num_list,tick_label=name_list)
plt.show()
plt.savefig("柱状图.jpg")

#横向柱状图
plt.barh(range(len(num_list)), num_list,tick_label=name_list)
plt.show()
plt.savefig("横向柱状图.jpg")

#并列柱状图
df = pd.DataFrame({'key1':pinpaiList,
                  'key2':tongxinList}
                  )
# print(df)
# print(df.groupby('key2'))
# print(df.groupby(['key1','key2']).groups)
quanqiu_List = []
donggan_List = []
shenzhou_List = []
result = df.groupby(['key1','key2']).groups
item_list = []
for res in result:
    print(res)
    print(len(result[res]))
    item_list.append((res,len(result[res])))

print(sorted(item_list))
for item in sorted(item_list):
    if item[0][1] == '全球通':
        quanqiu_List.append(item[1])
    if item[0][1] == '动感地带':
        donggan_List.append(item[1])
    if item[0][1] == '神州行':
        shenzhou_List.append(item[1])

name_list = []
for i in range(0,len(sorted(item_list)),3):
    name_list.append(sorted(item_list)[i][0][0])

total_width, n = 0.8, 3
width = total_width / n
x =list(range(len(num_list)))
print(quanqiu_List)
print(name_list)
plt.bar(range(len(num_list)), quanqiu_List, tick_label=name_list,  width=width, label='全球通')
for i in range(len(num_list)):
    x[i] = x[i] + width
plt.bar(x, donggan_List, tick_label=name_list, width=width, label='动感地带')
for i in range(len(num_list)):
    x[i] = x[i] + width
plt.bar(x, shenzhou_List, tick_label=name_list, width=width, label='神州行')
plt.legend()
plt.show()