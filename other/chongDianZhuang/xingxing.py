#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json

def start(item):
    url = 'https://app.starcharge.com/webApi/stubGroup/stubGroupDetailNew?id={id}&gisType=1&lat=22.529986&lng=113.950879&stubType=0&versionFlag=1'
    response = requests.get(url.format(id=item),verify=False)
    print(response.text)
    json_obj = json.loads(response.text)

    # 名称，地址，直流桩总数，交流桩总数，运行商，充电费用，服务费用，停车费用，经度，纬度
    name = json_obj['data']['name']
    address = json_obj['data']['address']
    try:
        if '1.40.00' in json.loads(json_obj['data']['stubCntInfo']):
            zhiliu = str(json.loads(json_obj['data']['stubCntInfo'])['1.40.00'])
        else:
            zhiliu = str(json.loads(json_obj['data']['stubCntInfo'])['1.60.00'])
    except:
        zhiliu = '0'

    try:
        jiaoliu = str(json.loads(json_obj['data']['stubCntInfo'])['0.7.00'])
    except:
        jiaoliu = '0'

    if json_obj['data']['type'] == 1:
        yunyingshang = '星星充电'
    elif json_obj['data']['type'] == 0:
        yunyingshang = '人人电站'
    else:
        yunyingshang = '其他'

    #电站类型
    if json_obj['data']['stubGroupType'] == 0:
        dianzanLeix = '公共电站'
    else:
        dianzanLeix = '专用电站'

    totalFee = str(json_obj['data']['totalFee'])

    #处理每一个费用

    dianfenStrList = []
    fuwuStrList = []

    if 'totalFeeInfo' in json_obj['data'] and json_obj['data']['totalFeeInfo']:
        totalFeeInfo_list = json.loads(json_obj['data']['totalFeeInfo'])
        for each in totalFeeInfo_list:
            eachdianfeiFee = str(each[1])
            eachfuwuFee = str(each[2])
            dianfenStrList.append(eachdianfeiFee)
            fuwuStrList.append(eachfuwuFee)

    dianfenStr = '--'.join(dianfenStrList)
    fuwuStr = '--'.join(fuwuStrList)

    tingcheFee = json_obj['data']['parkingFeeInfo']
    lon = str(json_obj['data']['gisGcj02Lng'])
    lat = str(json_obj['data']['gisGcj02Lat'])

    save_res = item+'||'+name+'||'+address+'||'+zhiliu+'||'+jiaoliu+'||'+yunyingshang+'||'+dianzanLeix+'||'+totalFee+'||'+dianfenStr+'||'+fuwuStr+'||'+tingcheFee+'||'+lon+'||'+lat
    save_res = save_res.replace(',','，').replace('\n','').replace('\r','').replace('\t','').replace('||',',').strip()+'\n'
    print(save_res)
    with open('星星充电.csv', 'a', encoding='gbk') as f:
        f.write(save_res)

if __name__ == '__main__':
    with open('星星充电.csv','w',encoding='gbk') as f:
        f.write('id,名称,地址,交流桩数,交流桩数,运行商,电站类型,平均费用,各时段充电费用,各时段服务费用,停车费用,经度,纬度\n')

    item_list = []
    with open('xingxing.txt') as f:
        results = f.readlines()
        for res in results:
            item_list.append(res.strip())

    for item in item_list:
        try:
            start(item)
        except:
            continue