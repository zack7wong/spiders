#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     redisModule
   Description :
   Author :        hayden_huang
   Date：          2018/12/29 20:07
-------------------------------------------------
"""



import json
import redis
import requests
import time
import random
import download
import config

HOST = 'localhost'
PORT = 6379
db = 1
import os


class Redis_curl(object):
    def __init__(self):
        self.redis_client = redis.Redis(host=HOST, port=PORT, decode_responses=True,db=db)

    def read_task(self):
        task_obj = self.redis_client.lpop('yinyangshi_task_list')
        if task_obj !=None:
            task_obj = json.loads(task_obj)
        return task_obj

    def rpush(self,obj):
        self.redis_client.rpush('yinyangshi_task_list',json.dumps(obj))

    def get_redis_Ip(self):
        for i in range(self.redis_client.llen('thisIp')):
            self.redis_client.lindex('thisIp', i)


def parse_detail(json_obj,task_obj):
    #收藏数
    collect_num = json_obj['equip']['collect_num']
    #价格
    price = json_obj['equip']['price']
    price = int(price / 100)
    # 15御魂数的数据
    equip_desc_obj = json.loads(json_obj['equip']['equip_desc'])
    level_15 = equip_desc_obj['level_15']
    if (collect_num > config.TYPE2_collect_num and (config.TYPE2_START_1 <= price <= task_obj['startPrice'] <= config.TYPE2_END_1)) or ((level_15 > config.TYPE2_YUHUNSHU15_2 and price <= config.TYPE2_PRICE_2) or (level_15 > config.TYPE2_YUHUNSHU15_3 and price <= config.TYPE2_PRICE_3) or (level_15 > config.TYPE2_YUHUNSHU15_4 and price <= config.TYPE2_PRICE_4)):
        flag_str = ';'
        if (collect_num > config.TYPE2_collect_num and (config.TYPE2_START_1 <= price <= task_obj['startPrice'] <= config.TYPE2_END_1)):
            flag_str += '1,'

        if (level_15 > config.TYPE2_YUHUNSHU15_2 and price <= config.TYPE2_PRICE_2):
            flag_str += '2,'

        if (level_15 > config.TYPE2_YUHUNSHU15_3 and price <= config.TYPE2_PRICE_3):
            flag_str += '3,'

        if (level_15 > config.TYPE2_YUHUNSHU15_4 and price <= config.TYPE2_PRICE_4):
            flag_str += '4,'


        save_URL = 'https://yys.cbg.163.com/cgi/mweb/equip/{serverid}/{game_ordersn}?view_loc=all_list'
        save_url = save_URL.format(serverid=str(json_obj['equip']['serverid']),game_ordersn=json_obj['equip']['game_ordersn'])
        print(save_url)

        filename = '公示期' + time.strftime('%Y%m%d-%H%M', time.localtime()) + '.txt'
        filename = os.path.join('公示期',filename)
        with open(filename, 'a') as f:
            f.write(save_url + '\n')


def main():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    redis_obj = Redis_curl()
    down = download.Download()
    task_obj = redis_obj.read_task()

    if task_obj != None:
        print('当前任务  '+str(task_obj))
        #时间不到，不爬取
        if int(time.time()) < task_obj['TYPE2_TIMESTAMP']:
            print('尚未到达指定时间，重新push回队列')
            redis_obj.rpush(task_obj)
        else:
            #超过自定义时间，开始爬取
            game_ordersn = task_obj['game_ordersn']
            serverid = task_obj['serverid']
            startPrice = task_obj['startPrice']

            detail_url = 'https://yys.cbg.163.com/cgi/api/get_equip_detail'

            headers = {
               'Accept': "application/json, text/javascript, */*; q=0.01",
               'Accept-Encoding': "gzip, deflate, br",
               'Accept-Language': "zh-CN,zh;q=0.9",
               'Cache-Control': "no-cache",
               'Connection': "keep-alive",
               # 'Content-Length': "80",
               'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
               # 'Cookie': "_ntes_nuid=94814b19e03b06016dfb804c54a0db08; usertrack=ezq0pVrPFa4zlUrCAyGOAg==; _ntes_nnid=e6bb7727c72bf6eed9771025ac2d509d,1523520941862; _ga=GA1.2.1137804346.1523520943; mail_psc_fingerprint=ef7ad2ac3cc4a73eb8535ba9c2961f86; __gads=ID=5405f793b3cc736d:T=1532326194:S=ALNI_MaygA1PB1BOhuqdi_7JY_6zi5kD4Q; UM_distinctid=164c5c22efa4e8-09259a77a91f5e-16386952-15f900-164c5c22efb747; vjuids=-b6e854263.164fde0bf8b.0.ada218d20b7b1; vjlast=1533267722.1533267722.30; vinfo_n_f_l_n3=1702a993a7145074.1.1.1532326196646.1533267739442.1541993721295; P_INFO=hhh2011jf@163.com|1542715891|0|mail163|11&10|null&null&null#gud&440300#10#0#0|&0||hhh2011jf@163.com; nts_mail_user=hhh2011jf@163.com:-1:1; fingerprint=rx9zee8v6gfptjzy; is_log_active_stat=1",
               'Host': "yys.cbg.163.com",
               'Origin': "https://yys.cbg.163.com",
               'Pragma': "no-cache",
               'Referer': "https://yys.cbg.163.com/",
               'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
               'X-Requested-With': "XMLHttpRequest",
               'cache-control': "no-cache",
            }

            data = 'serverid={serverid}&ordersn={game_ordersn}&view_loc=all_list%EF%BC%9B1'
            body = data.format(game_ordersn=game_ordersn, serverid=serverid)
            try:
                # myip = redis_obj.get_redis_Ip()
                # proxies = {
                #     'http:':'http://'+myip,
                #     'https:':'http://'+myip,
                # }

                # http代理接入服务器地址端口
                proxyHost = "http-proxy-t1.dobel.cn"
                proxyPort = "9180"

                proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
                    "host": proxyHost,
                    "port": proxyPort,
                    "user": config.proxyUser,
                    "pass": config.proxyPass,
                }

                proxies = {
                    "http": proxyMeta,
                    "https": proxyMeta,
                }

                response = requests.post(detail_url,data=body, headers=headers,proxies=proxies,timeout=10)
                # response = down.get_html(detail_url, method='post', data=body, headers=headers)
                print(response.text)
                if response:
                    json_obj = json.loads(response.text)
                    parse_detail(json_obj,task_obj)
            except:
                print('获取数据失败，重新push回队列')
                redis_obj.rpush(task_obj)

    else:
        print('无任务')


if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            print('未知错误')
        time.sleep(2)