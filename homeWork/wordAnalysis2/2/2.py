import os
import re

with open('归来记.txt') as f:
    guilaiji_results = f.read()

with open('红楼梦.txt') as f:
    houloumeng_results = f.read()

reRes1 = re.findall('------------.*?(\d+).*?。',guilaiji_results,re.S)
reRes2 = re.findall('分节阅读.*?(\d+).*?。',houloumeng_results,re.S)
print('归来记有：'+reRes1[-1]+'章')
print('红楼梦：'+reRes2[-1]+'章')



len_1 = len(guilaiji_results)
len_1 = str(len_1)

len_2 = len(houloumeng_results)
len_2 = str(len_2)
print('归来记 的总字数为：'+len_1)
print('红楼梦 的总字数为：'+len_2)

filePath = '归来记.txt'
fsize = os.path.getsize(filePath)
fsize = fsize/float(1024)
print('归来记文件大小是：'+str(round(fsize,2))+'KB')

filePath = '红楼梦.txt'
fsize = os.path.getsize(filePath)
fsize = fsize/float(1024)
print('红楼梦文件大小是：'+str(round(fsize,2))+'KB')

