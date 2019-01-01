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
    for w in words:
        if str(w.flag)[0] in cixing_dic.keys():
            print(w.word, cixing_dic[str(w.flag)[0]])


deal('武动乾坤.txt')
deal('红楼梦.txt')