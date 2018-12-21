#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import jieba

def analysis(fileDictory,type=''):
    all_item_list = []
    all_count_list = []
    for root, dirs, files in os.walk(fileDictory):
        # print(root) #当前目录路径
        # print(files) #文件
        for file in files:
            item_list = []
            count_list = []
            file_name = os.path.join(root, file)
            with open(file_name) as f:
                results = f.read()
                results = results.replace('’','').replace('.','').replace('“','').replace('”','').replace(',','').replace('\n',' ')

                if fileDictory =='english':
                    split_res = results.split(' ')
                elif fileDictory =='chinese' and type=='word':
                    split_res = []
                    pattern_all_zh = r'([\u4e00-\u9fa5])'
                    results = re.findall(pattern_all_zh, results, re.S)
                    for ch_res in results:
                        split_res.append(ch_res)
                elif fileDictory == 'chinese' and type=='ci':
                    pattern_all_zh = r'([\u4e00-\u9fa5])'
                    results = re.findall(pattern_all_zh, results, re.S)
                    results = ''.join(results)
                    split_res = jieba.cut(results, cut_all=False, HMM=True)
                    split_res = " ".join(split_res)
                    split_res = split_res.split(' ')

                for res in split_res:
                    if res == '' or res ==' ':
                        continue

                    if res in count_list:
                        for item in item_list:
                            if item['key'] == res:
                                item['value'] +=1
                                break
                    else:
                        obj = {
                            'key':res,
                            'value':1
                        }
                        item_list.append(obj)
                        count_list.append(res)
                #排序
                sort_list = sorted(item_list, key=lambda x:x['value'],reverse = True)
                rank=1
                for sort_res in sort_list:
                    sort_res['rank'] = rank
                    rank+=1
                    sort_res['r*f'] = sort_res['rank']*sort_res['value']
                    # print(sort_res)
                    if sort_res['key'] in all_count_list:
                        for all_item in all_item_list:
                            if all_item['key'] == sort_res['key']:
                                all_item['count_value'] += sort_res['value']
                                all_item['r*f'] +=sort_res['r*f']
                                if sort_res['r*f'] < all_item['min_r*f']:
                                    all_item['min_r*f'] = sort_res['r*f']
                                if sort_res['r*f'] > all_item['max_r*f']:
                                    all_item['max_r*f'] = sort_res['r*f']

                                break
                    else:
                        sort_res['min_r*f'] = sort_res['r*f']
                        sort_res['max_r*f'] = sort_res['r*f']
                        sort_res['count_value'] = sort_res['value']
                        all_item_list.append(sort_res)
                        all_count_list.append(sort_res['key'])

                # print(sort_list)

    # print(all_item_list)
    for item in all_item_list:
        #平均值
        if fileDictory == 'english':
            write_name = 'english.txt'
        elif fileDictory == 'chinese' and type == 'word':
            write_name = 'chinese_word.txt'
        elif fileDictory == 'chinese' and type == 'ci':
            write_name = 'chinese_ci.txt'

        print('单词为：'+item['key']+'， r*f的平均值为:'+str(item['r*f']/10))
        print('单词为：'+item['key']+'， r*f的最小值为:'+str(item['min_r*f']))
        print('单词为：'+item['key']+'， r*f的最大值除以文档词语数为:'+str(item['max_r*f']/item['count_value']))
        with open(write_name,'a') as f:
            f.write('单词为：'+item['key']+'， r*f的平均值为:'+str(item['r*f']/10)+'\n')
            f.write('单词为：'+item['key']+'， r*f的最小值为:'+str(item['min_r*f'])+'\n')
            f.write('单词为：'+item['key']+'， r*f的最大值除以文档词语数为:'+str(item['max_r*f']/item['count_value'])+'\n')


analysis('english')
analysis('chinese','word')
analysis('chinese','ci')