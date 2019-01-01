#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import jieba
import jieba.posseg as pseg

cixing_dic = {'a':'形容词','b':'区别词','c':'连词','d':'副词','m':'数词','n':'名词','p':'介词','q':'量词','r':'代词','u':'助词','v':'动词'}

def deal(filename):
    print('\n正在处理:' + filename)
    with open(filename) as f:
        results = f.read().replace('\n', '')

    pattern_all_zh = r'([\u4e00-\u9fa5])'
    wudong = re.findall(pattern_all_zh, results, re.S)
    wudong = ''.join(wudong)
    words = pseg.cut(wudong)
    item_list = []
    account_list = []
    for w in words:
        if str(w.flag)[0] in cixing_dic.keys():
            print(w.word, cixing_dic[str(w.flag)[0]])

            if str(w.flag)[0] in account_list:
                for item in item_list:
                    if item['key'] == str(w.flag)[0]:
                        item['value'] +=1
                        break
            else:
                account_list.append(str(w.flag)[0])
                obj = {
                    'key':str(w.flag)[0],
                    'value':1,
                    'name':cixing_dic[str(w.flag)[0]]
                }
                item_list.append(obj)

    for item in item_list:
        print(item['name']+' 有 '+ str(item['value'])+' 个')

deal('武动乾坤.txt')
deal('红楼梦.txt')