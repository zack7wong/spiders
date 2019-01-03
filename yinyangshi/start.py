#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import download
import config
import time
import math
import redis
import time

HOST = 'localhost'
PORT = 6379
db = 1

url = 'https://yys.cbg.163.com/cgi/mweb/pl/role?view_loc=all_list&order_by=selling_time%20DESC'

detail_url = 'https://yys.cbg.163.com/cgi/mweb/equip/11/201812011201616-11-LWVZNO4LTDIQQ?view_loc=all_list%EF%BC%9B1'
flag_id=''
all_game_ordersn_list = []


def read_redis():
    r = redis.Redis(host=HOST, port=PORT, decode_responses=True, db=db)
    all_list = []
    for i in range(r.llen('yinyangshi_task_list')):
        all_list.append(r.lindex('yinyangshi_task_list', i))

    return all_list

def parse_detail(json_obj):
    #先判断是否已经出售
    if json_obj['equip']['status_desc'] =='上架中':
        # 非公示期，可以立即购买，根据fair_show_end_time时间来判断
        serverid = str(json_obj['equip']['serverid'])
        game_ordersn = json_obj['equip']['game_ordersn']

        thisTime = json_obj['equip']['fair_show_end_time']
        ts = time.strptime(thisTime, "%Y-%m-%d %H:%M:%S")
        thisTimestamp = int(time.mktime(ts))

        price = json_obj['equip']['price']
        price = int(price / 100)
        #15御魂数的数据
        equip_desc_obj = json.loads(json_obj['equip']['equip_desc'])
        level_15 = equip_desc_obj['level_15']

        #当前时间大于这个，即可以购买，非公示期
        if int(time.time()) > thisTimestamp:
            # +15御魂数大于500，价格<=2000
            # +15御魂数大于400，价格<=1500
            # +15御魂数大于300，价格<=800

            if (level_15 > config.TYPE1_YUHUNSHU15_1 and price <= config.TYPE1_PRICE_1) or (level_15 > config.TYPE1_YUHUNSHU15_2 and price <= config.TYPE1_PRICE_2) or (level_15 > config.TYPE1_YUHUNSHU15_3 and price <= config.TYPE1_PRICE_3):
                save_URL = 'https://yys.cbg.163.com/cgi/mweb/equip/{serverid}/{game_ordersn}?view_loc=all_list'
                save_url = save_URL.format(serverid=str(json_obj['equip']['serverid']),game_ordersn=json_obj['equip']['game_ordersn'])
                print(save_url)
                filename = '非公示期'+time.strftime('%Y%m%d-%H%M',time.localtime())+'.csv'
                with open(filename,'a') as f:
                    f.write(save_url+'\n')

        # 当前时间小于这个，还在公示期
        else:
            #存储下来，自定义小时后爬取
            type2_Timestamp = thisTimestamp - ((24 - config.TYPE2_TIME) * 3600)
            save_obj = {
                'serverid':serverid,
                'game_ordersn':game_ordersn,
                'startPrice':price,
                'level_15':level_15,
                'thisTime':thisTime,
                'thisTimestamp':thisTimestamp,
                'TYPE2_TIMESTAMP':type2_Timestamp,
            }
            print(save_obj)
            flag = True
            for redisStr in all_list:
                redisObj = json.loads(redisStr)
                if (redisObj['game_ordersn'] == save_obj['game_ordersn']) and (redisObj['serverid'] == save_obj['serverid']):
                    flag = False
                    break
            if flag:
                print('saveing...'+str(save_obj))
                redis_client.rpush('yinyangshi_task_list', json.dumps(save_obj))


def parse_index(json_obj):
    for data in json_obj['result']:
        if data['game_ordersn'] in all_game_ordersn_list:
            return True
        else:
            all_game_ordersn_list.append(data['game_ordersn'])

        game_ordersn = data['game_ordersn']
        serverid = data['serverid']
        detail_url = 'https://yys.cbg.163.com/cgi/api/get_equip_detail'

        headers = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
            'Content-Length': "80",
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            # 'Cookie': "_ntes_nuid=94814b19e03b06016dfb804c54a0db08; usertrack=ezq0pVrPFa4zlUrCAyGOAg==; _ntes_nnid=e6bb7727c72bf6eed9771025ac2d509d,1523520941862; _ga=GA1.2.1137804346.1523520943; mail_psc_fingerprint=ef7ad2ac3cc4a73eb8535ba9c2961f86; __gads=ID=5405f793b3cc736d:T=1532326194:S=ALNI_MaygA1PB1BOhuqdi_7JY_6zi5kD4Q; UM_distinctid=164c5c22efa4e8-09259a77a91f5e-16386952-15f900-164c5c22efb747; vjuids=-b6e854263.164fde0bf8b.0.ada218d20b7b1; vjlast=1533267722.1533267722.30; vinfo_n_f_l_n3=1702a993a7145074.1.1.1532326196646.1533267739442.1541993721295; P_INFO=hhh2011jf@163.com|1542715891|0|mail163|11&10|null&null&null#gud&440300#10#0#0|&0||hhh2011jf@163.com; nts_mail_user=hhh2011jf@163.com:-1:1; fingerprint=rx9zee8v6gfptjzy; is_log_active_stat=1",
            'Host': "yys.cbg.163.com",
            'Origin': "https://yys.cbg.163.com",
            'Pragma': "no-cache",
            'Referer': "https://yys.cbg.163.com/cgi/mweb/equip/11/201812011201616-11-LWVZNO4LTDIQQ?view_loc=all_list%EF%BC%9B1",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            'X-Requested-With': "XMLHttpRequest",
            'cache-control': "no-cache",
        }

        data = 'serverid={serverid}&ordersn={game_ordersn}&view_loc=all_list%EF%BC%9B1'
        body = data.format(game_ordersn=game_ordersn,serverid=serverid)
        try:
            response = down.get_html(detail_url,method='post',data=body,headers=headers)
            if response:
                json_obj = json.loads(response.text)
                parse_detail(json_obj)
        except:
            print('请求详情页出错'+str(game_ordersn))

def start():
    url = 'https://yys.cbg.163.com/cgi/api/role_search?view_loc=all_list&order_by=selling_time%20DESC&page={pageToken}'
    start_url = url.format(pageToken=1)

    response = down.get_html(start_url)
    if response:
        json_obj = json.loads(response.text)
        print(response.text)
        totalNum = json_obj['total_num']
        pageNum = math.ceil(totalNum / 15)
        parseRes = parse_index(json_obj)
        if parseRes:
            return

        # 翻页
        for i in range(2, 6):
            try:
                print('当前页：'+str(i))
                pageToken = str(i)
                response = down.get_html(url.format(pageToken=pageToken))
                if response:
                    json_obj = json.loads(response.text)
                    # print(response.text)
                    each_parseRes = parse_index(json_obj)
                    if each_parseRes:
                        return
            except:
                print('当前页：' + str(i)+' 出错')


if __name__ == '__main__':
    #zhima4837415  123bai
    while True:
        try:
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
            down = download.Download()
            all_list = read_redis()
            redis_client = redis.Redis(host=HOST, port=PORT, decode_responses=True, db=db)
            start()
            print('本次已经完成，30秒后重新请求。。')
            time.sleep(30)
        except:
            print('未知错误，10秒后重新请求')
            time.sleep(10)