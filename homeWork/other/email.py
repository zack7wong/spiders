#!/usr/bin/env python
# -*- coding:utf-8 -*-


#导入包

import re

#读文本

with open('email.txt') as f:
    results = f.read()

results = results.replace('\n','').replace('\r','')
print(results)

right_reg_str = '[a-zA-Z0-9_]+@[a-zA-Z0-9]+\.[a-zA-Z]+'
right_find_res = re.findall(right_reg_str,results)
print(right_find_res)


with open('right.txt','w') as f:
    save_res = ';'.join(right_find_res)
    f.write(save_res)


false_reg_str = '[a-zA-Z0-9]*[~！#￥@%……&*（）——+!$^()\\/"\':;<>,，：；{}]+[a-zA-Z0-9]*@[a-zA-Z0-9]*.[a-zA-Z0-9]*|[a-zA-Z0-9_]+@\.[a-zA-Z]+|[a-zA-Z0-9_]+@\w+\.\W|[a-zA-Z0-9_]+@[a-zA-Z0-9_]*[~！#￥@%……&*（）——+!$^()\\/"\':;<>,，：；{}]+[a-zA-Z0-9_]*.[a-zA-Z0-9_]+'
false_find_res = re.findall(false_reg_str,results)
print(false_find_res)

with open('false.txt','w') as f:
    save_res = ';'.join(false_find_res)
    f.write(save_res)