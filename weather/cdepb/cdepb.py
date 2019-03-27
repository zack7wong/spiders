#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import time


def start():


    url = "http://182.150.31.86:9875/Handler/DefaultHandler.ashx?action=GetRealTimeData&_=1553673781816"

    querystring = {"x-msc-token": "EtspXz8xM7Pq7Ds7Lyoh5ZFN9MNGHwXp"}

    payload = ""
    headers = {
        'Accept': "*/*",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cache-Control': "no-cache",
        'Connection': "keep-alive",
        # 'Cookie': "yfx_c_g_u_id_10000063=_ck19032612161617371343118703172; yfx_f_l_v_t_10000063=f_t_1553573776716__r_t_1553660093937__v_t_1553660093937__r_c_1",
        'Host': "www.cdepb.gov.cn",
        'Pragma': "no-cache",
        'Referer': "http://www.cdepb.gov.cn/cdhbj/c111059/kqzl_list.shtml",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'cache-control': "no-cache",
        'Postman-Token': "cc84d93e-c945-4f01-ae6b-44f23503b268"
    }

    response = requests.request("GET", url)

    # print(response.text)

    json_obj = json.loads(response.text)


    for data in json_obj['Head']:

        # 站点,SO2,NO2,CO,O3,PM10,PM2.5,AQI,首要污染物,级别及类别
        #     var level_00 = "-@-@mdxz0";       //=0  增加=0时的判断，不应该显示：一级@优
        #     var level_01 = "一级@优@mdxz1";       //<=50
        #     var level_02 = "二级@良@mdxz2";       //<=100
        #     var level_03 = "三级@轻度污染@mdxz3"; //<=150
        #     var level_04 = "四级@中度污染@mdxz4"; //<=200
        #     var level_05 = "五级@重度污染@mdxz5"; //<=300
        #     var level_06 = "六级@严重污染@mdxz6"; //>>300

        # print(data)

        Rec_Time = data['Rec_Time']
        PointName = data['PointName']
        SO2_1H = data['SO2_1H']
        NO2_1H = data['NO2_1H']
        CO_1H = data['CO_1H']
        O3_1H = data['O3_1H']
        PM10_1H = data['PM10_1H']
        PM25_1H = data['PM25_1H']
        AQI_1H = data['AQI_1H']
        PRIMARY_POLLUTANTS = data['PRIMARY_POLLUTANTS']

        if AQI_1H == '':
            continue

        if int(AQI_1H) <=50:
            jibie = '一级，优'
        elif int(AQI_1H) <=100:
            jibie = '二级，良'
        elif int(AQI_1H) <=150:
            jibie = '三级，轻度污染'
        elif int(AQI_1H) <=200:
            jibie = '四级，中度污染'
        elif int(AQI_1H) <=300:
            jibie = '五级，重度污染'
        elif int(AQI_1H) > 300:
            jibie = '五级，严重污染'
        else:
            jibie = ''

        save_res = Rec_Time+','+PointName+','+SO2_1H+','+NO2_1H+','+CO_1H+','+O3_1H+','+PM10_1H+','+PM25_1H+','+AQI_1H+','+PRIMARY_POLLUTANTS+','+jibie+'\n'
        print(save_res)
        with open('结果.csv','a',encoding='gbk') as f:
            f.write(save_res)


if __name__ == '__main__':
    while True:
        print('当前时间：'+time.strftime('%Y-%m-%d %H:%M:%S') )
        try:
            start()
            print('1小时后重新运行。。')
            time.sleep(60*60)
        except:
            print('error')
            continue