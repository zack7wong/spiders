#!/usr/bin/env python
# -*- coding:utf-8 -*-

import jieba
import re

with open('武动乾坤.txt') as f:
    results1 = f.read()
    # results1 = results1[:1000]

print('正在计算武动乾坤。。')
pattern_all_zh = r'([\u4e00-\u9fa5])'
wudong = re.findall(pattern_all_zh, results1, re.S)
wudong = ''.join(wudong)
wudong_split_res = jieba.cut(wudong, cut_all=False, HMM=True)
wudong_split_res = " ".join(wudong_split_res)
wudong_split_res = wudong_split_res.split(' ')
wudong_item_list = []
wudong_count_list = []
for res in wudong_split_res:
    if res in wudong_count_list:
        for item in wudong_item_list:
            if item['key'] == res:
                item['value'] += 1
                break
    else:
        obj = {
            'key': res,
            'value': 1
        }
        wudong_item_list.append(obj)
        wudong_count_list.append(res)
wudong_50_list = sorted(wudong_item_list, key=lambda x:x['value'],reverse = True)[:50]

print('武动乾坤的总字数：'+str(len(results1)))
print('武动乾坤的总词频数：'+str(len(wudong_split_res)))
print('武动乾坤的分词如下：'+str(wudong_split_res[:50]))
print('武动乾坤的出现次数最多的前50个分词如下：'+str(wudong_50_list))

print('正在计算红楼梦。。')

with open('红楼梦.txt') as f:
    results2 = f.read()
    # results2 = results2[:1000]

pattern_all_zh = r'([\u4e00-\u9fa5])'
hongloumeng = re.findall(pattern_all_zh, results2, re.S)
hongloumeng = ''.join(hongloumeng)
hongloumeng_split_res = jieba.cut(hongloumeng, cut_all=False, HMM=True)
hongloumeng_split_res = " ".join(hongloumeng_split_res)
hongloumeng_split_res = hongloumeng_split_res.split(' ')
honglonmeng_item_list = []
honglonmeng_count_list = []
for res in hongloumeng_split_res:
    if res in honglonmeng_count_list:
        for item in honglonmeng_item_list:
            if item['key'] == res:
                item['value'] += 1
                break
    else:
        obj = {
            'key': res,
            'value': 1
        }
        honglonmeng_item_list.append(obj)
        honglonmeng_count_list.append(res)
hongloumeng_50_list = sorted(honglonmeng_item_list, key=lambda x:x['value'],reverse = True)[:50]


print('红楼梦的总字数：'+str(len(results2)))
print('红楼梦的总词频数：'+str(len(hongloumeng_split_res)))
print('红楼梦的分词如下：'+str(hongloumeng_split_res[:50]))
print('红楼梦的出现次数最多的前50个分词如下：'+str(hongloumeng_50_list))