#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import re
import json
from lxml import etree

# 汽车之家的需要爬取秦论坛，帖子内容，发帖时间，是否精华，作者，点击量，回复量和回复内容

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Cookie': "CYHTooltip=1; __ah_uuid=263BA464-4B46-4693-ACD3-A29CFF356EC8; fvlid=1547109859431cf0wlckp52; sessionid=5BFF7CEB-1ADB-45D1-9C2F-54DD96B33089%7C%7C2019-01-10+16%3A44%3A27.228%7C%7C0; ahpau=1; area=440305; historybbsName4=c-2761%7C%E7%A7%A6%2Cc-2733%7C%E5%A5%A5%E8%BF%AARS; UM_distinctid=1684bfe1a0f163-09a82743f3ba43-10376654-1fa400-1684bfe1a107a5; CNZZDATA1262640694=597270780-1547460849-https%253A%252F%252Fclub.autohome.com.cn%252F%7C1547460849; ASP.NET_SessionId=2ift50va4wgxontlfoyckfad; autoac=247A21D6A2581BAA247369B962602B6E; autotc=F8A11D4B87CCB2A0098D56769842448F; pvidchain=101061; sessionip=121.35.102.25; sessionvid=458D4941-FE31-44D7-B043-5418967EEF00; clubUserShow=55335774|692|2|%E6%B8%B8%E5%AE%A2|0|0|0||2019-01-15+11%3A43%3A01|0; clubUserShowVersion=0.1; papopclub=32E5E058BC67506B0BE2660A1997D0E3; pbcpopclub=0c2e1852-c646-48ee-bb10-6f97b172a15a; pepopclub=0DC064BDE5D71E43E0C944A829B1596D; ahpvno=24; ref=0%7C0%7C0%7C0%7C2019-01-15+11%3A43%3A47.113%7C2019-01-10+16%3A44%3A27.228",
    'Host': "club.autohome.com.cn",
    'Pragma': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "17408e9f-3981-4f0d-ab0c-25c6a3b713a8"
}

def parse(obj):

    detail_url = 'https://forum.app.autohome.com.cn/forum_v9.8.0/forum/club/topiccontent-a2-pm2-t{id}-o0-p1-s20-c1-nt0-fs0-sp0-al0-cw360-i0-ct0-mid0-abX-isar1.json'
    start_url = detail_url.format(id=obj['id'])
    print(start_url)
    headers = {
        'User-Agent': "Android6.0	autohome9.8.5	Android",
        'sample': "0",
        'reqid': "863100032895926/1547540160089/346",
        'apisign': "2|863100032895926|autohomebrush|1547540157|11D6CEBC22A1C9729C5C683E24F5D6AE",
        'Host': "forum.app.autohome.com.cn",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'cache-control': "no-cache",
        'Postman-Token': "8ca13309-a73f-4acb-8414-921c52aa0665"
    }
    response = requests.get(start_url,headers=headers,verify=False)
    responseRrStr = response.text.replace('<span class="hs_kw0_mainpl"></span>','，').replace('<span class="hs_kw1_mainpl"></span>','了').replace('<span class="hs_kw2_mainpl"></span>','是').replace('<span class="hs_kw3_mainpl"></span>','的').replace('<span class="hs_kw4_mainpl"></span>','不').replace('<span class="hs_kw6_mainpl"></span>','？').replace('<span class="hs_kw5_mainpl"></span>','。')
    html = HTML(responseRrStr)
    id = obj['id']

    url = start_url

    if obj['topictype'] == '精':
        jinghua = '1'
    else:
        jinghua = '0'
    userName = obj['userName']
    title = obj['title']
    publishDate = obj['publishDate']
    replyCount = obj['replyCount']

    clickCount = html.xpath('string(//span[@class="view"])').replace('浏览','')
    content = html.xpath('string(//div[@class="tz-paragraph"])')


    save_res = id + '||' + url + '||' + userName + '||' + title + '||' + jinghua + '||' + clickCount + '||' + replyCount + '||' + content + '||' + publishDate
    save_res = save_res.replace(',', '，').replace(' ', '').replace('\n', ' ').replace('\r', ' ').replace('||',',').strip() + '\n'
    print(save_res)
    with open('post.csv', 'a', encoding='utf8', errors='ignore') as f:
        f.write(save_res)

    commentEtreeList = html.xpath('//ul[@class="post-flow"]/li')
    for eachEtree in commentEtreeList:
        try:
            commentStr = etree.tostring(eachEtree)
            comment_html = HTML(commentStr)
            comment_list = comment_html.xpath('//div[@class="yy_reply_cont"]//text()')
            commentContent = ''.join(comment_list)
            if commentContent == '':
                continue
            with open('comment.csv','a') as f:
                commentRes = id +','+commentContent.replace(',','，').replace('\n', ' ').strip()+'\n'
                f.write(commentRes)
        except:
            continue

def start():
    for i in range(1,2028):
        start_url = 'https://clubnc.app.autohome.com.cn/club_v9.6.0/club/topics?pm=2&b=2761&bt=c&r=0&ss=0&o=0&p={pageToken}&s=50&qf=0&c=440300&t=0&v=9.8.5&d=863100032895926&n=0'.format(pageToken=i)
        print(start_url)
        try:
            response = requests.get(start_url,verify=False)
            # print(response.text)
            json_obj = json.loads(response.text)

            for data in json_obj['result']['list']:
                try:
                    title = data['title']
                    userName = data['postusername']
                    id = str(data['topicid'])
                    topictype = data['topictype']
                    publishDate = data['posttopicdateo']
                    replyCount = data['replycounts']
                    obj = {
                        'title':title,
                        'userName':userName,
                        'id':id,
                        'topictype':topictype,
                        'publishDate':publishDate,
                        'replyCount':replyCount,
                    }
                    parse(obj)
                except:
                    print('详情页错误')
                    with open('详情错误.txt','a') as f:
                        f.write(str(data)+'\n')
                    continue
        except:
            print('列表页错误')
            with open('列表页.txt','a') as f:
                f.write(start_url+'\n')
            continue

if __name__ == '__main__':
    with open('post.csv','w') as f:
        f.write('id,url,用户名,标题,是否精华,点击数,回复数,内容,发布时间\n')
    start()