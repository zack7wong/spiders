#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re

def deal(filename):
    print('\n正在处理:'+filename)
    with open(filename) as f:
        results = f.read().replace('\n','')

    sentences = re.split('(。|！|\.|\!|？|\?)', results)  # 保留分割符

    new_sents = []
    for i in range(int(len(sentences) / 2)):
        sent = sentences[2 * i] + sentences[2 * i + 1]
        new_sents.append(sent)
    # print(new_sents)
    item_list = []
    account_list = []
    for sent in new_sents:
        len_juzi = len(sent)
        if len_juzi in account_list:
            for item in item_list:
                if item['key'] == len_juzi:
                    item['value'] +=1
                    break
        else:
            account_list.append(len_juzi)
            obj = {
                'key':len_juzi,
                'value':1
            }
            item_list.append(obj)

    for item in item_list:
        print('句子长度为 '+str(item['key'])+' 的句子有 '+str(item['value'])+'个')

deal('武动乾坤.txt')
deal('红楼梦.txt')