#!/usr/bin/env python
# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt

man = 0
woman = 0
unknow = 0
with open('weixin_results.csv') as f:
    results = f.readlines()
    for res in results:
        print(res.split(',')[5])
        if res.split(',')[5] == '男':
            man+=1
        elif res.split(',')[5] == '女':
            woman += 1
        else:
            unknow +=1

plt.rcParams['axes.unicode_minus'] = False
labels = ['man', 'woman']
X = [man, woman]
fig = plt.figure()

plt.pie(X, labels=labels, autopct='%1.2f%%')  # 画饼图

plt.savefig("性别分析.jpg")
plt.show()
