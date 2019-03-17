#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json

def start(item):
    lon = item['lon']
    lat = item['lat']
    print(lon,lat)

    url = "https://app-api-prod.e-chong.com/station/map/list"

    payload = "{\"latitude\":\""+lat+"\",\"longitude\":\""+lon+"\",\"distance\":5000,\"city\":\"%e4%b8%8a%e6%b5%b7%e5%b8%82\"}"
    headers = {
        'USER_TOKEN': "",
        'USER_DEVICE_ID': "863100032895926",
        'APP_VER': "3.0.4",
        'PLAT_TYPE': "android",
        'PLAT_INFO': "Redmi Note 4|6.0",
        'Content-Type': "application/json; charset=utf-8",
        'Host': "app-api-prod.e-chong.com",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'User-Agent': "okhttp/3.11.0",
        'cache-control': "no-cache",
        'Postman-Token': "6b082172-4110-4c24-b46a-bee078e2c157"
    }

    response = requests.request("POST", url, data=payload, headers=headers,verify=False)
    json_obj = json.loads(response.text)

    print(response.text)
    for data in json_obj['data']:
        #id，名称、地址、桩数、电站类型、电费，服务费用，经纬度
        chargingStationId = str(data['chargingStationId'])
        if chargingStationId in id_list:
            continue
        else:
            id_list.append(chargingStationId)

        stationName = data['stationName']
        addrStreet = data['addrStreet']

        if data['isChargeNow'] == 1:
            zhuangshu = str(data['pileNums'])
        else:
            zhuangshu = str(data['pileNums']*2)

        if data['isOpenPublic'] == 1:
            dianzanLeix = '公共充电站'
        else:
            dianzanLeix = '专用充电站'

        electFee = data['electFee']
        serviceFee = data['serviceFee']
        latitude = data['latitude']
        longitude = data['longitude']

        save_res = chargingStationId + '||' + stationName + '||' + addrStreet + '||' + zhuangshu + '||' + dianzanLeix + '||' + electFee + '||' + serviceFee + '||' + latitude + '||' + longitude
        save_res = save_res.replace(',', '，').replace('\n', '').replace('\r', '').replace('\t', '').replace('||',',').strip() + '\n'
        print(save_res)
        with open('E充站.csv', 'a', encoding='gbk') as f:
            f.write(save_res)

if __name__ == '__main__':

    with open('E充站.csv','w',encoding='gbk') as f:
        f.write('id,名称,地址,桩数,电站类型,充电费用,服务费用,经度,纬度\n')

    id_list = []

    item_list = []
    with open('echong_geo.txt') as f:
        results =f.readlines()
        for res in results:
            lon = res.split(',')[0]
            lat = res.split(',')[1].strip()
            obj = {
                'lon':lon,
                'lat':lat,
            }
            item_list.append(obj)

    for item in item_list:
        start(item)