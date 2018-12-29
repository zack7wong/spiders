#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     deal
   Description :
   Author :        hayden_huang
   Date：          2018/12/28 21:34
-------------------------------------------------
# """
year_list = ['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
with open('aa.csv','a') as ff:
    with open('results.csv') as f:
        results = f.readlines()
        for res in results:
            year = res.split(',')[1].replace('，',',')
            for myyear in year_list:
                if myyear in year:
                    address = eval(res.split(',')[6].replace('，',','))
                    geolist = eval(res.split(',')[7].replace('，',','))
                    save_res = res.split(',')[1].replace('，',',') +','
                    for add in address:
                        for geo in geolist:
                            if add == geo['address']:
                                temp_res = add+'('+str(geo['geo']['lng'])+'，'+str(geo['geo']['lat'])+'，'+geo['district']+')'+','
                                save_res+=temp_res
                                break
                    print(save_res)
                    ff.write(save_res+'\n')
#         # print(address)
        # print(geo)
