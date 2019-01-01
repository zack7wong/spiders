#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import jieba

def deal(filename):
    print('\n正在处理:' + filename)
    with open(filename) as f:
        results = f.read().replace('\n', '')

    pattern_all_zh = r'([\u4e00-\u9fa5])'
    wudong = re.findall(pattern_all_zh, results, re.S)
    wudong = ''.join(wudong)
    wudong_split_res = jieba.cut(wudong, cut_all=False, HMM=True)
    wudong_split_res = " ".join(wudong_split_res)
    wudong_split_res = wudong_split_res.split(' ')
    # print(wudong_split_res)

    item_list = []
    account_list = []
    for sent in wudong_split_res:
        if len(sent) != 4:
            continue
        if sent in account_list:
            for item in item_list:
                if item['key'] == sent:
                    item['value'] += 1
                    break
        else:
            account_list.append(sent)
            obj = {
                'key': sent,
                'value': 1
            }
            item_list.append(obj)

    for item in item_list:
        print('4字词语为 ' + str(item['key']) + ' 的有 ' + str(item['value']) + '个')

deal('武动乾坤.txt')
deal('红楼梦.txt')