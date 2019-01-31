#!/usr/bin/env python
# -*- coding:utf-8 -*-


from coord_convert.transform import wgs2gcj, wgs2bd, gcj2wgs, gcj2bd, bd2wgs, bd2gcj
import requests
import json
import math
import time

# headers = {
#     'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     'accept-encoding': "gzip, deflate, br",
#     'accept-language': "zh-CN,zh;q=0.9",
#     'cache-control': "no-cache,no-cache",
#     'cookie': "guid=cf88-94c4-4017-f4f9; UM_distinctid=165c81d46438e5-04c0c996ef1128-34647908-13c680-165c81d464414d; cna=r1KFFAVLRlICAXkjZRXMAU9r; isg=BJubm_s-QzW6wbgb5yQ0h9V1KvnF2KcvJVcdFI3YcBr2bLxOHkAiwqalAorHmgdq; l=aB9eufATyJCzPDsmkMaiAJLSE707MU5zZzHM1MwHgiThNOUKJBAx2KQkNOzdSOASGo3J5IhvtJz..",
#     'pragma': "no-cache",
#     'upgrade-insecure-requests': "1",
#     'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
# }

headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "max-age=0,no-cache",
    'cookie': "guid=cf88-94c4-4017-f4f9",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
}

id_list = []

def get_detail(id):
    start_url = 'https://ditu.amap.com/detail/get/detail?id={id}'

    url = start_url.format(id=id)
    print(url)
    response = requests.get(url,headers=headers)
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

    save_res = id+'||'+name+'||'+address+'||'+lon+'||'+lat+'||'+shape+'||'+title+'||'+city_name+'||'+str(bd_lon)+'||'+str(bd_lat)+'||'+bd_shape
    save_res = save_res.replace('\n','').replace('\t','').replace(',','，').replace('||',',')+'\n'
    print(save_res)
    with open('结果.csv','a',encoding='gbk') as f:
        f.write(save_res)

    print('暂停5秒')
    time.sleep(5)

def get_index(keywords,city):
    start_url = 'http://restapi.amap.com/v3/place/text?&keywords={keywords}&city={city}&output=json&offset=20&page={pageToken}&key=3def748c5207f7a190b67df5f4633673&extensions=all'
    url = start_url.format(keywords=keywords,city=city,pageToken=1)
    response = requests.get(url)
    json_obj = json.loads(response.text)
    print(response.text)
    totalCount = int(json_obj['count'])
    totalNum = math.ceil(totalCount/20)

    for data in json_obj['pois']:
        id = data['id']
        if id in id_list:
            continue
        else:
            # get_detail(id)
            with open('allid.csv','a') as f:
                f.write(id+'\n')
            id_list.append(id)

    #翻页
    for i in range(2,totalNum+1):
        print('当前页'+str(i))
        start_url = 'http://restapi.amap.com/v3/place/text?&keywords={keywords}&city={city}&output=json&offset=20&page={pageToken}&key=3def748c5207f7a190b67df5f4633673&extensions=all'
        url = start_url.format(keywords=keywords, city=city, pageToken=i)
        response = requests.get(url)
        json_obj = json.loads(response.text)

        for data in json_obj['pois']:
            id = data['id']
            if id in id_list:
                continue
            else:
                # get_detail(id)
                with open('allid.csv', 'a') as f:
                    f.write(id + '\n')
                id_list.append(id)

def start():
    get_index('小区','石景山')


if __name__ == '__main__':
    start()