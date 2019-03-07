#!/usr/bin/env python
# -*- coding:utf-8 -*-

import download
import json
import config
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

def parse_comment(json_obj,userId):
    comment_time_Str = ''
    if 'datas' in json_obj and json_obj['datas'] and len(json_obj['datas']) > 0:
        for data in json_obj['datas']:
            if data['type'] == 0:
                if str(data['data']['user']['id']) != userId:
                    comment_time = getTimeStamp(data['data']['created_at'])
                    comment_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(comment_time))
                    comment_time_Str +=comment_time+'|'
    elif 'root_comments' in json_obj and len(json_obj['root_comments']) > 0:
        for data in json_obj['root_comments']:
            if str(data['user']['id']) != userId:
                comment_time = getTimeStamp(data['created_at'])
                comment_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(comment_time))
                comment_time_Str +=comment_time+'|'
    # print('comment:'+comment_time_Str)
    return comment_time_Str



def get_commentTime(id,userId):
    comment_url = 'https://api.weibo.cn/2/comments/build_comments?networktype=wifi&is_mix=1&max_id={pageToken}&is_show_bulletin=2&uicode=10000002&moduleID=700&trim_user=0&is_reload=1&featurecode=10000085&wb_version=3744&is_encoded=0&refresh_type=1&lcardid=seqid%3A1374065575%7Ctype%3A63%7Ct%3A3%7Cpos%3A1-0-0%7Cq%3A%E5%91%A8%E5%BA%84%7Cext%3A%26mid%3D{id}%26qtime%3D1545271481%26&c=android&i=b9a7450&s={s}&ft=0&id={id}&ua=Xiaomi-Redmi%20Note%203__weibo__8.9.1__android__android6.0.1&wm=20005_0002&aid=01Ag0Lr2Xl5hZl0TWMwP85lItMuOtNsl3aLXdZRC5UdNLcHQk.&v_f=2&v_p=63&from=1089195010&gsid={gsid}&lang=zh_CN&lfid=100103type%3D63%26q%3D%E5%91%A8%E5%BA%84%26t%3D0&skin=default&count=20&oldwm=20005_0002&sflag=1&ignore_inturrpted_error=true&luicode=10000003&fetch_level=0&is_append_blogs=1&max_id_type=0&cum=F67F24E7'
    response = down.get_html(comment_url.format(id=id, pageToken=0,gsid=config.gsid,s=config.s))
    if response:
        json_obj = json.loads(response.text)
        # print(response.text)

        totalNum = json_obj['total_number']
        pageNum = math.ceil(totalNum / 6)
        if int(totalNum) > config.commentsNum:
            return ''

        comment_time_AllStr = parse_comment(json_obj,userId)


        # 翻页
        for i in range(2, pageNum + 1):
            time.sleep(config.sleepTime)
            if 'top_hot_structs' not in json_obj and json_obj['max_id'] == 0:
                break
            if 'top_hot_structs' in json_obj:
                pageToken = str(json_obj['top_hot_structs']['call_back_struct']['max_id'])
            elif json_obj['max_id'] != 0:
                pageToken = str(json_obj['max_id'])

            response = down.get_html(comment_url.format(id=id, pageToken=pageToken,gsid=config.gsid,s=config.s))
            if response:
                json_obj = json.loads(response.text)
                # print(response.text)
                comment_time_AllStr += parse_comment(json_obj, userId)
    return comment_time_AllStr

def parse_reposts(json_obj,userId):
    reposts_time_Str = ''
    if 'reposts' in json_obj and json_obj['reposts'] and len(json_obj['reposts']) > 0:
        for data in json_obj['reposts']:
            if str(data['user']['id']) != userId:
                reposts_time = getTimeStamp(data['created_at'])
                reposts_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(reposts_time))
                reposts_time_Str +=reposts_time+'|'
    # print('reposts:'+str(reposts_time_Str))
    return reposts_time_Str

def get_repostsTime(id,userId):
    reposts_url = 'https://api.weibo.cn/2/statuses/repost_timeline?networktype=wifi&source=7501641714&uicode=10000002&moduleID=700&featurecode=10000085&wb_version=3744&lcardid=seqid%3A184040130%7Ctype%3A63%7Ct%3A4%7Cpos%3A1-0-0%7Cq%3A%E5%91%A8%E5%BA%84%7Cext%3A%26mid%3D{id}%26qtime%3D1545828027%26&c=android&i=b9a7450&s={s}&ft=0&id={id}&ua=Xiaomi-Redmi%20Note%203__weibo__8.9.1__android__android6.0.1&wm=20005_0002&aid=01Ag0Lr2Xl5hZl0TWMwP85lItMuOtNsl3aLXdZRC5UdNLcHQk.&v_f=2&v_p=63&from=1089195010&gsid={gsid}&lang=zh_CN&lfid=100103type%3D63%26q%3D%E5%91%A8%E5%BA%84%26t%3D0&page={pageToken}&skin=default&count=20&oldwm=20005_0002&sflag=1&luicode=10000003&has_member=1&cum=36BBF15C'
    response = down.get_html(reposts_url.format(id=id, pageToken=1,gsid=config.gsid,s=config.s))
    if response:
        json_obj = json.loads(response.text)
        # print(response.text)
        totalNum = json_obj['total_number']
        pageNum = math.ceil(totalNum / 16)
        if int(totalNum) > config.repostsNum:
            return ''

        reposts_time_AllStr = parse_reposts(json_obj, userId)

        # 翻页
        for i in range(2, pageNum + 1):
            time.sleep(config.sleepTime)
            pageToken = str(i)
            response = down.get_html(reposts_url.format(id=id, pageToken=pageToken,gsid=config.gsid,s=config.s))
            if response:
                json_obj = json.loads(response.text)
                # print(response.text)
                reposts_time_AllStr += parse_comment(json_obj, userId)
    return reposts_time_AllStr


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

    comment_time_AllStr = ''
    repostsTime_list = ''
    # comment_time_AllStr = get_commentTime(id,userId)
    # print('commentAll:'+comment_time_AllStr)
    # repostsTime_list = get_repostsTime(id,userId)
    # print('repostsAll:'+repostsTime_list)

    save_res = id + ',' + reposts_count + ',' + comments_count + ',' + attitudes_count + ',' + comment_time_AllStr +',' + repostsTime_list + ',' + content + ',' + str(
        publishDate) + ',' + publishDateStr + ',' + geo + ',' + userId + ',' + userName + ',' + followers_count + ',' + friends_count + ',' + location + ',' + str(
        reg_time) + ',' + reg_timeStr + ',' + sex + '\n'
    print(save_res)
    with open('results.csv','a') as f:
        f.write(save_res)

def main(keyword):
    keyword = quote(keyword)
    # URL = 'https://api.weibo.cn/2/cardlist?networktype=wifi&uicode=10000003&moduleID=708&featurecode=10000085&wb_version=3744&c=android&i=b9a7450&s={s}&ft=0&ua=Xiaomi-Redmi%20Note%203__weibo__8.9.1__android__android6.0.1&wm=20005_0002&aid=01Ag0Lr2Xl5hZl0TWMwP85lItMuOtNsl3aLXdZRC5UdNLcHQk.&fid=100303type%3D63%26q%3D%E5%88%98%E4%BA%A6%E8%8F%B2%26t%3D0&uid=6667036271&v_f=2&v_p=63&from=1089195010&gsid={gsid}&containerid=100303type%3D63%26q%3D{keyword}&&page={pageToken}'
    URL = 'https://api.weibo.cn/2/cardlist?networktype=wifi&uicode=10000003&moduleID=708&featurecode=10000085&wb_version=3744&c=android&i=b9a7450&s={s}&ft=0&ua=Xiaomi-Redmi%20Note%203__weibo__8.9.1__android__android6.0.1&wm=20005_0002&aid=01Ag0Lr2Xl5hZl0TWMwP85lItMuOtNsl3aLXdZRC5UdNLcHQk.&fid=100303type%3D63%26q%3D%E5%88%98%E4%BA%A6%E8%8F%B2%26t%3D0&uid=6667036271&v_f=2&v_p=63&from=1089195010&gsid={gsid}&containerid=100303type%3D1%26q%3D{keyword}&&page={pageToken}'
    start_url = URL.format(keyword=keyword,pageToken=1,gsid=config.gsid,s=config.s)
    print(start_url)
    response = down.get_html(start_url)
    if response:
        # print(response.text)
        json_obj = json.loads(response.text)
        totalNum = json_obj['cardlistInfo']['total']
        pageNum = math.ceil(totalNum/20)
        if 'cards' in json_obj and len(json_obj['cards'])>0:
            for data in json_obj['cards'][1]['card_group']:
                parse(data)

        #翻页
        for i in range(2,pageNum+1):
            response = down.get_html(URL.format(keyword=keyword, pageToken=i,gsid=config.gsid,s=config.s))
            if response:
                # print(response.text)
                json_obj = json.loads(response.text)
                for data in json_obj['cards'][0]['card_group']:
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