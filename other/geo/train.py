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
from coord_convert.transform import wgs2gcj, wgs2bd, gcj2wgs, gcj2bd, bd2wgs, bd2gcj


file_list = ['编号','高德代码','住区名称','住区地址','类型','城市','高德POI经度','高德POI纬度','高德地图折点经度','高德地图折点纬度','百度POI经度','百度POI纬度','百度地图折点经度','百度地图折点纬度','WGS84POI经度','WGS84POI纬度','WGS84折点经度','WGS84折点纬度']

async def example():

    api_bulk_config = GetterConfig.RCSVConfig('结果2用于改格式.csv',encoding='gbk')
    getter = ProcessFactory.create_getter(api_bulk_config)
    mongo_config = WriterConfig.WXLSXConfig('最终结果.xlsx', headers=file_list)
    with ProcessFactory.create_writer(mongo_config) as mongo_writer:
        async for items in getter:
            newItems_list = []
            for item in items:
                print(item)
                item['WGS84POI经度'],item['WGS84POI纬度'] = gcj2wgs(float(item['高德POI经度']), float(item['高德POI纬度']))

                strList = item['高德拐点左边'].split(';')

                bd_shape = ''
                if strList[0] != '':
                    for each in strList:
                        try:
                            eachLon = float(each.split('，')[0])
                            eachLat = float(each.split('，')[1])
                        except:
                            eachLon = float(each.split('')[0])
                            eachLat = float(each.split('')[1])

                        each_bd_lon, each_bd_lat = wgs2bd(eachLon, eachLat)
                        bd_shape += str(each_bd_lon) + '，' + str(each_bd_lat) + ';'

                item['WGS84拐点坐标'] = bd_shape


                newItem = copy.deepcopy(item)
                del newItem['高德拐点左边']
                del newItem['百度拐点坐标']
                del newItem['WGS84拐点坐标']
                if item['高德拐点左边']:
                    allStr_gaode = item['高德拐点左边']
                    allStr_baidu = item['百度拐点坐标']
                    allStr_WGS84 = item['WGS84拐点坐标']
                    allStr_gaode_list = allStr_gaode.split(';')
                    allStr_baidu_list = allStr_baidu.split(';')
                    allStr_WGS84_list = allStr_WGS84.split(';')
                    for gaode,baidu,WGS84 in  zip(allStr_gaode_list,allStr_baidu_list,allStr_WGS84_list):
                        print(gaode)
                        print(baidu)
                        print(WGS84)
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

                        try:
                            lon_WGS84 = WGS84.split('，')[0]
                            lat_WGS84 = WGS84.split('，')[1]
                        except:
                            lon_WGS84 = WGS84.split('')[0]
                            lat_WGS84 = WGS84.split('')[1]

                        newItem['高德地图折点经度'] = lon_gaode
                        newItem['高德地图折点纬度'] = lat_gaode
                        newItem['百度地图折点经度'] = lon_baidu
                        newItem['百度地图折点纬度'] = lat_baidu
                        newItem['WGS84折点经度'] = lon_WGS84
                        newItem['WGS84折点纬度'] = lat_WGS84
                        saveItem = copy.deepcopy(newItem)
                        newItems_list.append(saveItem)
                else:
                    newItems_list.append(newItem)

                # newItems_list.append(item)
            mongo_writer.write(newItems_list)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(example())