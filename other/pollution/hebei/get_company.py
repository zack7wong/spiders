#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     get_company
   Description :
   Author :        hayden_huang
   Date：          2019/3/3 16:57
-------------------------------------------------
"""

id_list = []
with open('hebei_id.txt') as f:
    resutls = f.readlines()
    for res in resutls:
        id_list.append(res.strip())
print(id_list)
print(len(id_list))
print(len(set(id_list)))


name_list = []
with open('evenid.txt') as f:
    resutls = f.readlines()
    for res in resutls:
        name_list.append(res.strip())
print(name_list)
print(len(name_list))
print(len(set(name_list)))

for name,id in zip(name_list,id_list):
    save_res = id+','+name+'\n'
    with open('new_hebei_id.txt','a') as f:
        f.write(save_res)