#!/usr/bin/env python
# -*- coding:utf-8 -*-


name_list = ['三亚原始数据.csv','西安原始数据.csv']

item_list = []
for filename in name_list:
    with open(filename) as f:
        results = f.readlines()
        for res in results:
            riqi = res.split(',')[0].replace(' ','')
            tianqi = res.split(',')[1].replace(' ','')
            qiwen = res.split(',')[2].replace(' ','')
            zuigao_qiwen = qiwen.split('/')[0].replace('℃','')
            zuidi_qiwen = qiwen.split('/')[1].replace('℃','').strip()
            if filename == '三亚原始数据.csv':
                write_filename = '三亚清洗数据.csv'
            elif filename == '西安原始数据.csv':
                write_filename = '西安清洗数据.csv'
            with open(write_filename,'a') as f:
                save_res = riqi+','+ tianqi+','+zuidi_qiwen+','+zuigao_qiwen+'\n'
                f.write(save_res)



