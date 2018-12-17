#!/usr/bin/env python
# -*- coding:utf-8 -*-

import jieba
import re

with open('三国演义.txt') as f:
    results = f.read()

pattern_all_zh = r'([\u4e00-\u9fa5])'
text_cn_split = re.findall(pattern_all_zh, results, re.S)
results = ''.join(text_cn_split)
seg_list = jieba.cut(results, cut_all=False, HMM=True)
fenci = " ".join(seg_list)
split_res = fenci.split(' ')
# print(split_res)
results_dic = {}
for res in split_res:
    if res in results_dic.keys():
        results_dic[res]+=1
    else:
        results_dic[res]=1
# print(results_dic)
# print(sorted(results_dic))
sortres = sorted(results_dic.items(), key=lambda e:e[1], reverse=True)
print(sortres[:10])