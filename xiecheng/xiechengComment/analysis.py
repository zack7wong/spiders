#!/usr/bin/env python
# -*- coding:utf-8 -*-

import jieba

with open('comment.txt') as f:
    results = f.read()


text = results.encode()
# 结巴分词
wordlist = jieba.cut(text, cut_all=True)
print(wordlist)
wl = " ".join(wordlist)


words = wl.split(' ')
print(words)

item_list = []
have_list = []
for word in words:
    if word == '':
        continue
    if len(word) == 1:
        continue
    if word == '#x20':
        continue
    if word in have_list:
        for each in item_list:
            if each['word'] == word:
                each['num']+=1
                break
    else:
        obj = {
            'word':word,
            'num':1
        }
        item_list.append(obj)
        have_list.append(word)

print(item_list)
sort_list = sorted(item_list, key=lambda x:x['num'],reverse = True)
print(sort_list)
for item in item_list:
    with open('结果.csv','a',encoding='gbk') as f:
        save_res = item['word']+','+ str(item['num'])+'\n'
        f.write(save_res)