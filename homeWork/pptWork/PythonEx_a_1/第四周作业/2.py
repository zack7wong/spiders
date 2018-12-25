#!/usr/bin/env python
# -*- coding:utf-8 -*-

with open('唐诗三百首.txt') as f:
    results =f.read()

results = results.replace('，','').replace('\n','').replace('。','').replace(':','')

item_list = []
account_list = []
for item in results:
    if item not in account_list:
        account_list.append(item)
        item_list.append(
            {
                'key':item,
                'value':1
             }
        )
    else:
        for key in item_list:
            if key['key'] == item:
                key['value']+=1
print(sorted(item_list, key=lambda x: x['value'],reverse=True)[:20])