#!/usr/bin/env python
# -*- coding:utf-8 -*-

import matplotlib
import matplotlib.pyplot as plt
from snownlp import SnowNLP


xiaoji_list = 0
zhongxing_list = 0
jiji_list = 0
with open('desc.txt') as f:
    results = f.readlines()
    for res in results:
        res = res.strip()
        # print(res)
        if len(res) == 0 or res == '':
            continue
        s = SnowNLP(res)
        print(res,s.sentiments) # positive的概率 情感分析结果是【0，1】区间上的一个值，越接近1，情感越积极，越接近0，情感越消极
        if 0<=s.sentiments and s.sentiments<0.33:
            xiaoji_list+=1
        elif 0.33 <= s.sentiments  and s.sentiments < 0.66:
            zhongxing_list += 1
        else:
            jiji_list+=1
print(xiaoji_list)
print(zhongxing_list)
print(jiji_list)

#柱状图
name_list = ['negative','neutral','positive']
num_list = [xiaoji_list,zhongxing_list,jiji_list]

plt.bar(range(len(num_list)), num_list,tick_label=name_list,color = 'rgb')
plt.savefig("情感分析.jpg")
plt.show()