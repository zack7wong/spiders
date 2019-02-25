#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import dateutil.parser
import time
import json

headers = {
    'accept': "application/json, text/plain, */*",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "no-cache,no-cache",
    'cookie': "_T_WM=d6a820526b61ec42774925fb64ff699f; ALF=1550141369; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFX9gU.0AvvHpkroN8y6_.s5JpX5K-hUgL.Fo-ESoB0SoMXeh.2dJLoI7L.9JLXSh2Reh2t; SCF=AlH-htFhOOtuSJnrHnxgPfbVUuhc309qQH8-v0vpUXbAOaJweFeTv-fEb02TE0x_poD_Ii8KLCsR-yoG03p74cg.; SUB=_2A25xOb3wDeThGeNM7VYS9inIyzWIHXVSxcO4rDV6PUJbktAKLVLlkW1NTh6TnIuH6Kji-kJs-yMgz7_aPHAEaUX0; SUHB=02M_eArjzMX0Gy; SSOLoginState=1547554208; WEIBOCN_FROM=1110006030; MLOGIN=1; XSRF-TOKEN=fcfdbf; M_WEIBOCN_PARAMS=fid%3D1076035790112354%26uicode%3D10000011",
    'mweibo-pwa': "1",
    'pragma': "no-cache",
    'referer': "https://m.weibo.cn/u/5790112354",
    'user-agent': "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36",
    'x-requested-with': "XMLHttpRequest",
}

def getTimeStamp(dateStr):
    dateTime = dateutil.parser.parse(dateStr)
    time_tuple = (dateTime.year, dateTime.month, dateTime.day, dateTime.hour, dateTime.minute, dateTime.second, 0, 0, 0)
    timestamp = int(time.mktime(time_tuple))
    return timestamp

with open('结果.csv','w',encoding='gbk',errors='ignore') as f:
    f.write('id,commentUrl,commentCount,userId,userName,commentTime,commentText,userUrl\n')

num = 1
since_id = ''
start_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=5790112354&containerid=1076035790112354&since_id='+since_id
response = requests.get(start_url,headers=headers)
print(response.text)
json_obj = json.loads(response.text)

for data in json_obj['data']['cards']:
    if data['card_type'] == 9:
        # print(json.dumps(data))
        postId = str(data['mblog']['id'])
        commentUrl = 'https://m.weibo.cn/api/comments/show?id='+postId
        commentCount = str(data['mblog']['comments_count'])

        max_id = 0
        while True:
            commentDetailUrl = 'https://m.weibo.cn/comments/hotflow?id=4323453953625672&mid=4323453953625672&max_id={max_id}&max_id_type=0'.format(max_id=max_id)
            response = requests.get(commentDetailUrl,headers=headers)
            print(commentDetailUrl)
            print(response.text)
            json_detail = json.loads(response.text)
            if json_detail['ok'] == 0:
                break

            if 'data' in json_detail and 'data' in json_detail['data']:
                for each in json_detail['data']['data']:
                    commentId = each['id']
                    userId = str(each['user']['id'])
                    userName = each['user']['screen_name'].replace(',','，')
                    publishDate = getTimeStamp(each['created_at'])
                    commentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(publishDate))
                    commentText = each['text'].replace('\n','').replace('\r','').replace(',','，').strip()
                    userUrl = each['user']['profile_url']

                    # print(commentId,userId,userName,commentTime,commentText,userUrl)

                    save_res = str(num)+','+commentUrl+','+commentCount+','+userId+','+userName+','+commentTime+','+commentText+','+userUrl+'\n'
                    print(save_res)
                    with open('结果.csv','a',encoding='gbk',errors='ignore') as f:
                        f.write(save_res)
                    num+=1

                if json_detail['data']['max_id']:
                    max_id = json_detail['data']['max_id']
                    if max_id == 0:
                        break
                else:
                    break
            else:
                break

            time.sleep(2)
