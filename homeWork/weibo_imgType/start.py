#!/usr/bin/env python
# -*- coding:utf-8 -*-

import download
import json
import math
import time
import dateutil.parser
from urllib.parse import quote

# URL = 'https://api.weibo.cn/2/cardlist?networktype=wifi&uicode=10000003&moduleID=708&featurecode=10000085&wb_version=3744&c=android&i=b9a7450&s=4ab66666&ft=0&ua=Xiaomi-Redmi%20Note%203__weibo__8.9.1__android__android6.0.1&wm=20005_0002&aid=01Ag0Lr2Xl5hZl0TWMwP85lItMuOtNsl3aLXdZRC5UdNLcHQk.&fid=100303type%3D63%26q%3D%E5%88%98%E4%BA%A6%E8%8F%B2%26t%3D0&uid=6667036271&v_f=2&v_p=63&from=1089195010&gsid=_2A252ka9PDeRxGeBI7VUR8yjOzD2IHXVTBqWHrDV6PUJbkdAKLUzZkWpNRm6MkwYtOWOEh1o_MCp_OymzU4gFDZT1&imsi=460096637806271&lang=zh_CN&lfid=231091&page=1&skin=default&count=10&oldwm=20005_0002&sflag=1&containerid=100303type%3D63%26q%3D%E5%88%98%E4%BA%A6%E8%8F%B2%26t%3D3&ignore_inturrpted_error=true&luicode=10000010&container_ext=newhistory%3A0%7Cshow_topic%3A1&need_head_cards=0&cum=5EDE8DA8'


def read():
    item_list = []
    with open('keyword.txt') as f:
        results = f.readlines()
        for res in results:
            item_list.append(res.strip())
    return item_list

def getTimeStamp(dateStr):
    dateTime = dateutil.parser.parse(dateStr)
    time_tuple = (dateTime.year, dateTime.month, dateTime.day, dateTime.hour, dateTime.minute, dateTime.second, 0, 0, 0)
    timestamp = int(time.mktime(time_tuple))
    return timestamp

def parse_comment(json_obj,userId,pageToken=''):
    if pageToken==1:
        pass
    else:
        pass


def get_commentTime(id,userId):
    comment_url = 'https://api.weibo.cn/2/comments/build_comments?networktype=wifi&is_mix=1&max_id={pageToken}&is_show_bulletin=2&uicode=10000002&moduleID=700&trim_user=0&is_reload=1&featurecode=10000085&wb_version=3744&is_encoded=0&refresh_type=1&lcardid=seqid%3A1374065575%7Ctype%3A63%7Ct%3A3%7Cpos%3A1-0-0%7Cq%3A%E5%91%A8%E5%BA%84%7Cext%3A%26mid%3D{id}%26qtime%3D1545271481%26&c=android&i=b9a7450&s=4ab66666&ft=0&id={id}&ua=Xiaomi-Redmi%20Note%203__weibo__8.9.1__android__android6.0.1&wm=20005_0002&aid=01Ag0Lr2Xl5hZl0TWMwP85lItMuOtNsl3aLXdZRC5UdNLcHQk.&v_f=2&v_p=63&from=1089195010&gsid=_2A25xHoAEDeRxGeBI7VUR8yjOzD2IHXVTjZTMrDV6PUJbkdAKLUzZkWpNRm6MkwoMUBtNjk9tdh3lu37wWPMKkCY6&lang=zh_CN&lfid=100103type%3D63%26q%3D%E5%91%A8%E5%BA%84%26t%3D0&skin=default&count=20&oldwm=20005_0002&sflag=1&ignore_inturrpted_error=true&luicode=10000003&fetch_level=0&is_append_blogs=1&max_id_type=0&cum=F67F24E7'
    response = down.get_html(comment_url.format(id=id, pageToken=0))
    comment_list = []
    if response:
        print(response.text)
        json_obj = json.loads(response.text)

        obj = parse_comment(json_obj,userId,1)

        while True:
            if json_obj['max_id'] ==0:
                break
            pageToken = str(json_obj['max_id'])
            response = down.get_html(comment_url.format(id=id, pageToken=pageToken))
            json_obj = json.loads(response.text)
            parse_comment(json_obj)
    return comment_list

def get_repostsTime(id,userId):
    pass


def parse(data):
    id = str(data['mblog']['id'])

    userId = str(data['mblog']['user']['id'])
    userName = data['mblog']['user']['screen_name']
    followers_count = str(data['mblog']['user']['followers_count'])
    friends_count = str(data['mblog']['user']['friends_count'])
    location = data['mblog']['user']['location']
    location = location.replace(',','，').replace('\n','')
    reg_time = getTimeStamp(data['mblog']['user']['created_at'])
    reg_timeStr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(reg_time))
    sex = ''
    if data['mblog']['user']['gender'] == 'm':
        sex = '男'
    elif data['mblog']['user']['gender'] == 'f':
        sex = '女'


    content = data['mblog']['longText']['longTextContent'] if 'longText' in data['mblog'] else data['mblog']['text']
    content = content.replace(',','，').replace('\n','').replace('\r','')
    publishDate = getTimeStamp(data['mblog']['created_at'])
    publishDateStr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(publishDate))
    geo = ''
    if 'tag_struct' in data['mblog']:
        geo = data['mblog']['tag_struct'][0]['tag_name']

    reposts_count = str(data['mblog']['reposts_count'])
    comments_count = str(data['mblog']['comments_count'])
    attitudes_count = str(data['mblog']['attitudes_count'])

    save_res = id+','+reposts_count+','+comments_count+','+attitudes_count+','+content+','+str(publishDate)+','+publishDateStr+','+geo+','+userId+','+userName+','+followers_count+','+friends_count+','+location+','+str(reg_time)+','+reg_timeStr+','+sex+'\n'
    print(save_res)

    # commentTime_list = get_commentTime(id,userId)
    # repostsTime_list = get_repostsTime(id,userId)

def main(keyword):
    keyword = quote(keyword)
    URL = 'https://api.weibo.cn/2/cardlist?networktype=wifi&uicode=10000003&moduleID=708&featurecode=10000085&wb_version=3744&c=android&i=b9a7450&s=4ab66666&ft=0&ua=Xiaomi-Redmi%20Note%203__weibo__8.9.1__android__android6.0.1&wm=20005_0002&aid=01Ag0Lr2Xl5hZl0TWMwP85lItMuOtNsl3aLXdZRC5UdNLcHQk.&fid=100303type%3D63%26q%3D%E5%88%98%E4%BA%A6%E8%8F%B2%26t%3D0&uid=6667036271&v_f=2&v_p=63&from=1089195010&gsid=_2A252ka9PDeRxGeBI7VUR8yjOzD2IHXVTBqWHrDV6PUJbkdAKLUzZkWpNRm6MkwYtOWOEh1o_MCp_OymzU4gFDZT1&containerid=100303type%3D63%26q%3D{keyword}&&page={pageToken}'
    start_url = URL.format(keyword=keyword,pageToken=1)
    response = down.get_html(start_url)
    if response:
        # print(response.text)
        json_obj = json.loads(response.text)
        totalNum = json_obj['cardlistInfo']['total']
        pageNum = math.ceil(totalNum/20)

        for data in json_obj['cards'][1]['card_group']:
            parse(data)

        #翻页
        for i in range(2,pageNum+1):
            response = down.get_html(URL.format(keyword=keyword, pageToken=i))
            if response:
                # print(response.text)
                json_obj = json.loads(response.text)
                for data in json_obj['cards'][1]['card_group']:
                    parse(data)
            else:
                continue
    else:
        print('网络请求失败')

if __name__ == '__main__':
    down = download.Download()
    item_list = read()
    for keyword in item_list:
        print('当前关键词：'+keyword)
        main(keyword)