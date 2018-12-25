#!/usr/bin/env python
# -*- coding:utf-8 -*-

mystring = input('请输入字符串：')
# mystring = 'abaAdsa1B2178a'

oushunum_list = []
jishunum_list = []
string_list = []
for mystr in mystring:
   try:
        myNum = int(mystr)
        if myNum%2 == 0:
            oushunum_list.append(mystr)
        else:
            jishunum_list.append(mystr)
   except:
       string_list.append(mystr)

oushunum_list = sorted(oushunum_list)
jishunum_list = sorted(jishunum_list)
string_list = sorted(string_list)

oushunum = ''.join(oushunum_list)
jishunum = ''.join(jishunum_list)
thisstring = ''.join(string_list)
res = oushunum+jishunum+thisstring
print('结果为：'+res)