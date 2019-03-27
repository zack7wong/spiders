#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import time


def start():


    url = "http://api.chengdu.gov.cn/cdhbjk/index.php/Weather/station"

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

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    print(response.text)

    json_obj = json.loads(response.text)

    nowTime = time.strftime('%Y-%m-%d')

    for data in json_obj[4]:
        print(data)
        detail_list = []
        name = data['name']

        for detail in data['data']:
            if detail['y']:
                detail_list.append(str(detail['y']))
            else:
                detail_list.append('')
        save_res = nowTime+','+name+','+','.join(detail_list)+'\n'
        with open('结果.csv','a',encoding='gbk') as f:
            f.write(save_res)


if __name__ == '__main__':
    with open('结果.csv', 'w', encoding='gbk') as f:
        f.write('日期,类别,0点,1点,2点,3点,4点,5点,6点,7点,8点,9点,10点,11点,12点,13点,14点,15点,16点,17点,18点,19点,20点,21点,22点,23点\n')
    start()