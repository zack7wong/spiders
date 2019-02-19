#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import requests
import json
from coord_convert.transform import wgs2gcj, wgs2bd, gcj2wgs, gcj2bd, bd2wgs, bd2gcj

headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "max-age=0,no-cache",
    'cookie': "guid=cf88-94c4-4017-f4f9",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
}

def get_detail(id):
    start_url = 'https://ditu.amap.com/detail/get/detail?id={id}'

    url = start_url.format(id=id)
    print(url)
    response = requests.get(url,headers=headers,verify=False)
    # response = requests.get(url)
    json_obj = json.loads(response.text)
    print(response.text)

    city_name = json_obj['data']['base']['city_name']
    # alias_name = json_obj['data']['base']['alias_name'] if 'alias_name' in json_obj['data']['base'] else ''
    title = json_obj['data']['base']['title']
    address = json_obj['data']['base']['address']
    name = json_obj['data']['base']['name']
    lon = json_obj['data']['base']['x']
    lat = json_obj['data']['base']['y']
    if 'spec' in json_obj['data'] and 'mining_shape' in json_obj['data']['spec'] and 'shape' in json_obj['data']['spec']['mining_shape']:
        shape = json_obj['data']['spec']['mining_shape']['shape']
        strList = shape.split(';')

        bd_shape = ''
        for each in strList:
            eachLon = float(each.split(',')[0])
            eachLat = float(each.split(',')[1])
            each_bd_lon, each_bd_lat = wgs2bd(eachLon, eachLat)
            bd_shape += str(each_bd_lon)+'，'+ str(each_bd_lat)+';'
    else:
        shape = ''
        bd_shape = ''

    gdlon, gdlat = float(lon), float(lat)
    # gcj_lon, gcj_lat = wgs2gcj(lon, lat)
    bd_lon, bd_lat = wgs2bd(gdlon, gdlat)

    print(name)
    no_cralw_list = ['派出所','居委会','办事处','中学','服务站','体育馆','幼教中心','学校','大学','有限公司','医院','活动中心','服务中心','活动室','太极苑','产业园']
    for noName in no_cralw_list:
        if noName in name:
            print('非住宅区，不抓取')
            return

    save_res = id+'||'+name+'||'+address+'||'+lon+'||'+lat+'||'+shape+'||'+title+'||'+city_name+'||'+str(bd_lon)+'||'+str(bd_lat)+'||'+bd_shape
    save_res = save_res.replace('\n','').replace('\t','').replace(',','，').replace('||',',')+'\n'
    print(save_res)
    with open('结果.csv','a',encoding='gbk') as f:
        f.write(save_res)

    print('暂停5秒')
    time.sleep(5)

if __name__ == '__main__':
    item_list = []
    try:
        with open('结果.csv',encoding='gbk') as f:
            results = f.readlines()
            for res in results:
                id = res.split(',')[0]
                item_list.append(id)
    except:
        pass

    id_list = []
    with open('allid.csv') as f:
        results = f.readlines()
        for res in results:
            id = res.strip()
            if id not in item_list:
                id_list.append(id)
    for id in id_list:
        get_detail(id)