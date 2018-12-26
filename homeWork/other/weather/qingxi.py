#!/usr/bin/env python
# -*- coding:utf-8 -*-

item_list = []
with open('三亚原始数据.csv') as f:
    results = f.readlines()
    for res in results:
        riqi = res.split(',')[0].replace(' ','')
        tianqi = res.split(',')[1].replace(' ','')
        qiwen = res.split(',')[2].replace(' ','')
        zuigao_qiwen = qiwen.split('/')[0].replace('℃','')
        zuidi_qiwen = qiwen.split('/')[1].replace('℃','').strip()
        with open('三亚清洗数据.csv','a') as f:
            save_res = riqi+','+ tianqi+','+zuidi_qiwen+','+zuigao_qiwen+'\n'
            f.write(save_res)



