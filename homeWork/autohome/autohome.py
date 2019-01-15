#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import re

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

def parse(link,response):
    html = HTML(response.text)
    id = re.search('https://club.autohome.com.cn/bbs/thread/(.*?)/',link)
    if id:
        id = id.group(1)
    else:
        id = link

    url = link

    if 'd="seal"' in response.text:
        jinghua = '1'
    else:
        jinghua = '0'
    userName = html.xpath('string(//li[@class="txtcenter fw"]/a/@title)')
    clickCount = html.xpath('string(//font[@id="x-views"])')
    replyCount = html.xpath('string(//font[@id="x-replys"])')
    content = html.xpath('string(//div[@class="conttxt"])')
    publishDate = html.xpath('string(//span[@xname="date"])')

    save_res = id + '||' + url + '||' + userName + '||' + jinghua + '||' + clickCount + '||' + replyCount + '||' + content + '||' + publishDate
    save_res = save_res.replace(',', '，').replace(' ', '').replace('\n', ' ').replace('\r', ' ').replace('||',',').strip() + '\n'
    print(save_res)
    with open('post.csv', 'a', encoding='utf8', errors='ignore') as f:
        f.write(save_res)

def start():
    for i in range(1,1001):
        start_url = 'https://club.autohome.com.cn/bbs/forum-c-2761-{pageToken}.html?qaType=-1#pvareaid=101061'.format(pageToken=i)
        print(start_url)
        response = requests.get(start_url,headers=headers)
        html = HTML(response.text)
        # print(response.text)
        url_list = html.xpath('//div[@id="subcontent"]/dl/dt[1]/a[1]/@href')
        for url in url_list:
            link = 'https://club.autohome.com.cn'+url
            print(link)
            detail_response = requests.get(link,headers=headers)
            # print(detail_response.text)
            parse(link,detail_response)
            break
        break

if __name__ == '__main__':
    with open('post.csv','w') as f:
        f.write('id,url,用户名,是否精华,点击数,回复数,内容,发布时间\n')
    start()