#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import os

with open('傲慢与偏见.txt') as f:
    words = f.read()

zhangshu = re.findall('--------.*?第(.*?)章.*?--------',words,re.S)
ai = re.findall('爱',words,re.S)
ya = re.findall('丫',words,re.S)
jian = re.findall('简',words,re.S)

changdu = len(words)

fsize = os.path.getsize('傲慢与偏见.txt')
fsize = fsize/float(1024*1024)

print('傲慢与偏见文件大小：'+str(round(fsize,2))+'MB')
print('傲慢与偏见的总字数为：'+str(changdu))
print('傲慢与偏见有'+zhangshu[-1]+'章')
print('爱 的字数有：'+str(len(ai))+' 个')
print('丫 的字数有：'+str(len(ya))+' 个')
print('简 的字数有：'+str(len(jian))+' 个')


with open('步步惊心.txt') as f:
    words = f.read()


zhangshu = re.findall('Chapter.*?(\d+).*?。',words,re.S)

changdu = len(words)

fsize = os.path.getsize('步步惊心.txt')
fsize = fsize/float(1024*1024)

ai = re.findall('爱',words,re.S)
ya = re.findall('丫',words,re.S)
jian = re.findall('马尔泰',words,re.S)

print('步步惊心文件大小：'+str(round(fsize,2))+'MB')
print('步步惊心的总字数为：'+str(changdu))
print('步步惊心有'+zhangshu[-1]+'章')
print('爱 的字数有：'+str(len(ai))+' 个')
print('丫 的字数有：'+str(len(ya))+' 个')
print('马尔泰 的字数有：'+str(len(jian))+' 个')

