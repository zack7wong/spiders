#!/usr/bin/env python
# -*- coding:utf-8 -*-

with open('word.txt') as f:
    results = f.read()

results = results.replace('\n',' ')
split_res = results.split(' ')
print('文章内容为：'+results)
print('单词的个数为：'+str(len(split_res)))