#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
from lxml.etree import HTML
import re

headers = {
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    # 'Cookie': 'bid=jiPiWxCsnbg; ll="118282"; _vwo_uuid_v2=DBCE20527FFC5F06CAEE989D0D0A1CA6E|d3a1206da68d4dffd70ab6cfdb29e357; _ga=GA1.2.2071961702.1531198334; __utmv=30149280.17490; douban-profile-remind=1; douban-fav-remind=1; viewed="6049132"; gr_user_id=c902b75b-be37-423a-8589-cd0a81e33537; __utmc=30149280; __utmc=223695111; __yadk_uid=TNAAa6V3q1b0pjypK2OWoVq0XWqwrxlC; ap_v=0,6.0; dbcl2="174901236:i85XnMZMukY"; ck=ss1x; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1550920499%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport%2Flogin%3Fredir%3Dhttps%253A%252F%252Fmovie.douban.com%252Fexplore%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.2071961702.1531198334.1550916112.1550920499.44; __utmb=30149280.0.10.1550920499; __utmz=30149280.1550920499.44.19.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; __utma=223695111.2071961702.1531198334.1550916112.1550920499.4; __utmb=223695111.0.10.1550920499; __utmz=223695111.1550920499.4.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; push_noty_num=0; push_doumail_num=0; _pk_id.100001.4cf6=4d713e5636800d95.1550840314.4.1550920558.1550918679.',
    # 'Cookie': 'bid=jiPiWxCsnbg; __yadk_uid=BXgC7quIT8CrXFcLVOeqON8WyDywpCPQ; ll="118282"; _vwo_uuid_v2=DBCE20527FFC5F06CAEE989D0D0A1CA6E|d3a1206da68d4dffd70ab6cfdb29e357; _ga=GA1.2.2071961702.1531198334; douban-profile-remind=1; douban-fav-remind=1; viewed="6049132"; gr_user_id=c902b75b-be37-423a-8589-cd0a81e33537; __utmc=30149280; ap_v=0,6.0; __utma=30149280.2071961702.1531198334.1550916112.1550920499.44; __utmz=30149280.1550920499.44.19.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; push_noty_num=0; push_doumail_num=0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1550920858%2C%22https%3A%2F%2Fmovie.douban.com%2Fexplore%22%5D; _pk_ses.100001.8cb4=*; __utmt=1; dbcl2="192293664:3s//jYMlAXk"; ck=oYQY; _pk_id.100001.8cb4=034c79f38f87e772.1531198331.36.1550920901.1550817893.; __utmv=30149280.19229; __utmb=30149280.6.9.1550920901763',
    'Host': "movie.douban.com",
    'Pragma': "no-cache",
    'Referer': "https://movie.douban.com/explore",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    # 'X-Requested-With': "XMLHttpRequest",
    'cache-control': "no-cache",
    'Postman-Token': "7f371300-aa70-47f2-95fd-5c98ec1f8400"
    }

def oneInfo(name,url):
    response = requests.get(url,headers=headers)
    html = HTML(response.text)
    rateList = html.xpath('//div[@id="recent_movies"]//div[@class="bd"]/ul/li/div[@class="info"]/em/text()')
    rateList = rateList[:5]
    print(rateList)

    cha = 5-len(rateList)
    for i in range(cha):
        rateList.append('0')

    rate_res = '||'.join(rateList)
    returnRes = name+'||'+rate_res
    print(returnRes)
    return returnRes


def parse(response,title,rate):
    html =HTML(response.text)

    jsonText = re.search('application/ld\+json">(.*?)</script>',response.text,re.S).group(1).strip()
    json_obj = json.loads(jsonText)
    print(json.dumps(json_obj))

    #获取基础信息
    try:
        director = json_obj['director'][0]['name'].split(' ')[0]
        director_url = 'https://movie.douban.com'+json_obj['director'][0]['url']
        directorInfo = oneInfo(director,director_url)
    except:
        director = ''
        directorInfo = '0||0||0||0||0||0'

    try:
        bianju1 = json_obj['author'][0]['name'].split(' ')[0]
        bianju1_url = 'https://movie.douban.com'+json_obj['author'][0]['url']
        bianju1Info = oneInfo(bianju1, bianju1_url)
    except:
        bianju1 = ''
        bianju1Info = '0||0||0||0||0||0'

    try:
        bianju2 = json_obj['author'][1]['name'].split(' ')[0]
        bianju2_url = 'https://movie.douban.com'+json_obj['author'][1]['url']
        bianju2Info = oneInfo(bianju2, bianju2_url)
    except:
        bianju2 = ''
        bianju2Info = '0||0||0||0||0||0'

    try:
        yanyuan1 = json_obj['actor'][0]['name'].split(' ')[0]
        yanyuan1_url = 'https://movie.douban.com'+json_obj['actor'][0]['url']
        yanyuan1Info = oneInfo(yanyuan1, yanyuan1_url)
    except:
        yanyuan1 = ''
        yanyuan1Info = '0||0||0||0||0||0'

    try:
        yanyuan2 = json_obj['actor'][1]['name'].split(' ')[0]
        yanyuan2_url = 'https://movie.douban.com'+json_obj['actor'][1]['url']
        yanyuan2Info = oneInfo(yanyuan2, yanyuan2_url)
    except:
        yanyuan2 = ''
        yanyuan2Info = '0||0||0||0||0||0'

    try:
        yanyuan3 = json_obj['actor'][2]['name'].split(' ')[0]
        yanyuan3_url = 'https://movie.douban.com'+json_obj['actor'][2]['url']
        yanyuan3Info = oneInfo(yanyuan3, yanyuan3_url)
    except:
        yanyuan3 = ''
        yanyuan3Info = '0||0||0||0||0||0'

    print(director,bianju1,bianju2,yanyuan1,yanyuan2,yanyuan3)



    genreList = json_obj['genre']
    type = '/'.join(genreList)
    country = re.search('制片国家/地区:</span>(.*?)<br/>',response.text).group(1).strip()
    language = re.search('语言:</span>(.*?)<br/>',response.text).group(1).strip()
    movieTime = re.search('片长:</span>.*?<span.*?>.*?(\d+)分钟.*?</span>',response.text).group(1).strip()
    datePublished = json_obj['datePublished']
    ratingCount = json_obj['aggregateRating']['ratingCount']
    wantViewCount = html.xpath('string(//div[@class="subject-others-interests-ft"]/a[2])').replace('人想看','')

    #获取各个导演，编剧的信息


    save_res = title+'||'+directorInfo+'||'+bianju1Info+'||'+bianju2Info+'||'+yanyuan1Info+'||'+yanyuan2Info+'||'+yanyuan3Info+'||'+type+'||'+country+'||'+language+'||'+datePublished+'||'+movieTime+'||'+ratingCount+'||'+wantViewCount+'||'+rate
    save_res = save_res.replace('\n','').replace(',','，').replace('||',',')+'\n'
    print(save_res)
    with open('结果.csv','a',encoding='gbk',errors='ignore') as f:
        f.write(save_res)

def start():
    for i in range(0,15):#10
        print('当前页：'+str(i))
        url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start='+str(i*20)
        response = requests.get(url,headers=headers)
        print(response.text)
        json_obj = json.loads(response.text)
        for data in json_obj['subjects']:
            deatil_url = data['url']
            title = data['title']
            rate = data['rate']
            response = requests.get(deatil_url,headers=headers)
            # print(response.text)
            try:
                parse(response,title,rate)
            except:
                continue

if __name__ == '__main__':
    start()