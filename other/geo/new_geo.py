#!/usr/bin/env python
# -*- coding:utf-8 -*-

import asyncio
import hashlib
import time
import copy
import re
from idataapi_transform import ProcessFactory, GetterConfig, WriterConfig
import math
import requests
import json

file_list = ['编号','地址','幸福指数','年龄','性别','小区名称','经度_百度坐标','纬度_百度坐标']




async def example():

    results_list = []
    api_bulk_config = GetterConfig.RXLSXConfig('居民调查数据.xlsx')
    getter = ProcessFactory.create_getter(api_bulk_config)
    async for items in getter:
        for item in items:
            if item['地址']:
                item['地址'] = item['地址'].replace('-','')
                item['地址2'] = item['地址'].replace('北京市', '').replace('北京', '').replace('石景山区', '').replace('石景山', '')
                # print(item)
                results_list.append(item)

    juzhuqu_list = []
    api_bulk_config = GetterConfig.RXLSXConfig('石景山居住区.xlsx')
    getter = ProcessFactory.create_getter(api_bulk_config)
    async for items in getter:
        for item in items:
            # print(item['地址'])
            item['地址'] = re.sub('\(.*?\)','',item['地址'])
            # print(item['地址'])
            juzhuqu_list.append(item)

    for res in results_list:
        print(res)
        for juzhuqu in juzhuqu_list:
            if res['地址'] == juzhuqu['小区名称']:
                res['小区名称'] = juzhuqu['小区名称']
                res['经度_百度坐标'] = juzhuqu['经度_百度坐标']
                res['纬度_百度坐标'] = juzhuqu['纬度_百度坐标']

            elif res['地址'] == juzhuqu['地址']:
                res['小区名称'] = juzhuqu['小区名称']
                res['经度_百度坐标'] = juzhuqu['经度_百度坐标']
                res['纬度_百度坐标'] = juzhuqu['纬度_百度坐标']
            elif res['地址2'] in juzhuqu['小区名称']:
                res['小区名称'] = juzhuqu['小区名称']
                res['经度_百度坐标'] = juzhuqu['经度_百度坐标']
                res['纬度_百度坐标'] = juzhuqu['纬度_百度坐标']
            elif res['地址2'] in juzhuqu['地址']:
                res['小区名称'] = juzhuqu['小区名称']
                res['经度_百度坐标'] = juzhuqu['经度_百度坐标']
                res['纬度_百度坐标'] = juzhuqu['纬度_百度坐标']
            else:
                # print(res['地址2'])
                lenRes = len(res['地址2'])
                for i in range(math.ceil(lenRes/3)):
                    thisStr = res['地址2'][i*3:(i+1)*3]
                    if len(thisStr)<3:
                        continue
                    # print(thisStr)
                    if thisStr in juzhuqu['地址']:
                        res['小区名称'] = juzhuqu['小区名称']
                        res['经度_百度坐标'] = juzhuqu['经度_百度坐标']
                        res['纬度_百度坐标'] = juzhuqu['纬度_百度坐标']
                        break



    mongo_config = WriterConfig.WXLSXConfig('最终结果.xlsx',headers=file_list)
    with ProcessFactory.create_writer(mongo_config) as mongo_writer:
        mongo_writer.write(results_list)



    num=0
    all_res = []
    api_bulk_config = GetterConfig.RXLSXConfig('最终结果.xlsx')
    getter = ProcessFactory.create_getter(api_bulk_config)
    async for items in getter:
        for item in items:
            if item['小区名称'] == None:
                try:
                    url = 'http://api.map.baidu.com/geocoder?address={address}&output=json&key=37492c0ee6f924cb5e934fa08c6b1676'.format(address=item['地址'])
                    response = requests.get(url)
                    # print(response.text)
                    json_obj = json.loads(response.text)
                    lng = str(json_obj['result']['location']['lng'])
                    lat = str(json_obj['result']['location']['lat'])

                    item['经度_百度坐标'] = lng
                    item['纬度_百度坐标'] = lat
                    print(item)

                    num+=1
                except:
                    print('error')
                    continue
            all_res.append(item)

    print(num)
    mongo_config = WriterConfig.WXLSXConfig('最终结果2.xlsx',headers=file_list)
    with ProcessFactory.create_writer(mongo_config) as mongo_writer:
        mongo_writer.write(all_res)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(example())