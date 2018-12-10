#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     excelDeal
   Description :
   Author :        hayden_huang
   Date：          2018/12/6 00:07
-------------------------------------------------
"""

import os


from collections import OrderedDict
from pyexcel_xls import get_data
from pyexcel_xls import save_data
from pylab import *

def main():
    results = read_xls_file('results.xlsx')
    res_2015 = []
    res_2015_num = 0
    res_2016 = []
    res_2016_num = 0
    res_2017 = []
    res_2017_num = 0
    res_2018 = []
    res_2018_num = 0
    res_lx = []
    res_lx_num = 0
    res_other = []
    res_other_num = 0

    #处理
    for res in results:
        res['value'] = str(res['value'])
        if '2015' in res['value']:
            res_2015.append(res)
            res_2015_num +=1
        elif '2016' in res['value']:
            res_2016.append(res)
            res_2016_num += 1
        elif '2017' in res['value']:
            res_2017.append(res)
            res_2017_num += 1
        elif '2018' in res['value']:
            res_2018.append(res)
            res_2018_num += 1
        elif 'lx' == res['value'][0:2]:
            res_lx.append(res)
            res_lx_num += 1
        else:
            res_other.append(res)
            res_other_num += 1

    #保存结果
    save_xls_file(res_2015,'2015.xls')
    save_xls_file(res_2016,'2016.xls')
    save_xls_file(res_2017,'2017.xls')
    save_xls_file(res_2018,'2018.xls')
    save_xls_file(res_lx,'lx.xls')
    save_xls_file(res_other,'other.xls')

    #数据计数合并
    chartResults = [
        {'key':'2015','value':res_2015_num},
        {'key':'2016','value':res_2016_num},
        {'key':'2017','value':res_2017_num},
        {'key':'2018','value':res_2018_num},
        {'key':'lx','value':res_lx_num},
        {'key':'other','value':res_other_num},
    ]
    chart(chartResults)


def read_xls_file(filename):
    xls_data = get_data(filename)
    results = []
    for sheet_n in xls_data.keys():
        for item in xls_data[sheet_n][1:]:
            # print(item)
            key = item[0]
            value = item[1]

            obj ={
                'key': key,
                'value': value,
            }
            results.append(obj)

    return results


def save_xls_file(results,filename):
    data = OrderedDict()
    # sheet表的数据
    sheet_1 = []
    row_1_data = ['key','value']  # 每一行的数据
    sheet_1.append(row_1_data)
    for res in results:
        key = res['key']
        value = res['value']

        row_2_data = [key,value]
        sheet_1.append(row_2_data)
    data.update({filename: sheet_1})
    # 保存成xls文件
    save_data(filename, data)

#图表展示
def chart(obj_list):
    # font = FontProperties(fname=r"/System/Library/Fonts/PingFang.ttc", size=12)
    data = []
    name = []
    for obj in obj_list:
        name.append(obj['key'])
        data.append(obj['value'])
    plt.bar(name, data)

    plt.xticks(range(len(data)), name)
    plt.show()

if __name__ == '__main__':
    main()