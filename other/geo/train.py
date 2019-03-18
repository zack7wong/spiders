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


file_list = ['编号','高德代码','住区名称','住区地址','高德POI经度','高德POI纬度','高德地图折点经度','高德地图折点纬度','类型','城市','百度POI经度','百度POI纬度','百度地图折点经度','百度地图折点纬度']

async def example():

    api_bulk_config = GetterConfig.RCSVConfig('结果2用于改格式.csv',encoding='gbk')
    getter = ProcessFactory.create_getter(api_bulk_config)
    mongo_config = WriterConfig.WXLSXConfig('最终结果.xlsx', headers=file_list)
    with ProcessFactory.create_writer(mongo_config) as mongo_writer:
        async for items in getter:
            newItems_list = []
            for item in items:
                newItem = copy.deepcopy(item)
                del newItem['高德拐点左边']
                del newItem['百度拐点坐标']
                if item['高德拐点左边']:
                    allStr_gaode = item['高德拐点左边']
                    allStr_baidu = item['百度拐点坐标']
                    allStr_gaode_list = allStr_gaode.split(';')
                    allStr_baidu_list = allStr_baidu.split(';')
                    for gaode,baidu in  zip(allStr_gaode_list,allStr_baidu_list):
                        print(gaode)
                        print(baidu)
                        try:
                            lon_gaode = gaode.split('，')[0]
                            lat_gaode = gaode.split('，')[1]
                        except:
                            lon_gaode = gaode.split('')[0]
                            lat_gaode = gaode.split('')[1]

                        try:
                            lon_baidu = baidu.split('，')[0]
                            lat_baidu = baidu.split('，')[1]
                        except:
                            lon_baidu = baidu.split('')[0]
                            lat_baidu = baidu.split('')[1]

                        newItem['高德地图折点经度'] = lon_gaode
                        newItem['高德地图折点纬度'] = lat_gaode
                        newItem['百度地图折点经度'] = lon_baidu
                        newItem['百度地图折点纬度'] = lat_baidu
                        saveItem = copy.deepcopy(newItem)
                        newItems_list.append(saveItem)
            mongo_writer.write(newItems_list)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(example())