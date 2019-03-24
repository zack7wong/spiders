#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import re
import json
import db

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Cookie': 'bid=jiPiWxCsnbg; ll="118282"; _vwo_uuid_v2=DBCE20527FFC5F06CAEE989D0D0A1CA6E|d3a1206da68d4dffd70ab6cfdb29e357; _ga=GA1.2.2071961702.1531198334; douban-profile-remind=1; douban-fav-remind=1; viewed="6049132"; gr_user_id=c902b75b-be37-423a-8589-cd0a81e33537; __yadk_uid=TNAAa6V3q1b0pjypK2OWoVq0XWqwrxlC; __utmz=223695111.1550920499.4.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; push_noty_num=0; push_doumail_num=0; __utmv=30149280.19229; ct=y; __utmz=30149280.1552644645.51.23.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1553423248%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport%2Flogin%3Fredir%3Dhttps%253A%252F%252Fmovie.douban.com%252Fexplore%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.2071961702.1531198334.1552644645.1553423249.52; __utmb=30149280.0.10.1553423249; __utmc=30149280; __utma=223695111.2071961702.1531198334.1552373181.1553423249.8; __utmb=223695111.0.10.1553423249; __utmc=223695111; dbcl2="174901236:Ud60RwKZOSY"; ck=4JGP; _pk_id.100001.4cf6=4d713e5636800d95.1550840314.8.1553428893.1552373269.',
    'Host': "movie.douban.com",
    'Pragma': "no-cache",
    'Referer': "https://movie.douban.com/top250?start=225&filter=",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "49939e16-a5ab-4976-a522-6cf49d3b30e1"
    }

def start():
    num = 1
    for i in range(0,10):
        print('当前页：'+str(i))
        pageToken = i*25
        start_url = 'https://movie.douban.com/top250?start={pageToken}&filter='.format(pageToken=pageToken)
        print(start_url)
        response = requests.get(start_url,headers=headers)
        # print(response.text)
        html = HTML(response.text)
        urls = html.xpath('//ol[@class="grid_view"]/li//div[@class="hd"]/a/@href')
        for url in urls:
            print(url)
            movieId = re.search('https://movie.douban.com/subject/(\d+)/',url).group(1)
            response = requests.get(url, headers=headers)
            html = HTML(response.text)

            MovieNameStr = html.xpath('string(//h1/span/text())')
            MovieName = MovieNameStr.split(' ')[0].replace('\'','"')
            EnglishName = ' '.join(MovieNameStr.split(' ')[1:]).replace('\'','"')

            pattern_all_zh = r'([\u4e00-\u9fa5])'
            text_cn_split = re.findall(pattern_all_zh, EnglishName, re.S)
            if text_cn_split:
                EnglishName = ''
                MovieName = MovieNameStr.replace('\'','"').strip()

            jsonStr = re.search('<script type="application.*?">(.*?)</script>',response.text,re.S).group(1).replace('\n','').strip()
            # print(response.text)
            print(jsonStr)
            json_obj = json.loads(jsonStr)

            OtherName = ''
            OtherNameStr = re.search('又名:</span>(.*?)<br/>',response.text)
            if OtherNameStr:
                OtherName = OtherNameStr.group(1).strip().replace('\'','"')
            DirectorList = []
            for dire in json_obj['director']:
                DirectorList.append(dire['name'])
            Director = '|'.join(DirectorList).replace('\'','"')

            ActorsList = []
            for dire in json_obj['actor']:
                ActorsList.append(dire['name'])
            Actors = '|'.join(ActorsList).replace('\'','"')

            Year = json_obj['datePublished']
            Country = re.search('制片国家/地区:</span>(.*?)<br/>',response.text).group(1).replace('\n','').replace('\'','"').strip()
            timeLong = re.search('片长:</span> <span property="v:runtime" content="(\d+)"',response.text).group(1).replace('\n','').replace('\'','"').strip()

            Grenre = '|'.join(json_obj['genre'])
            Rating = json_obj['aggregateRating']['ratingValue']
            RatingNum = json_obj['aggregateRating']['ratingCount']
            Description = json_obj['description']

            # print(movieId)
            # print(MovieName)
            # print(EnglishName)
            # print(Director)
            # print(Actors)
            # print(Year)
            # print(Country)
            # print(Grenre)
            # print(Rating)
            # print(RatingNum)
            # print(Description)

            sql = "insert into info(movieId,num,MovieName,EnglishName,OtherName,Director,Actors,Year,Country,Grenre,Rating,RatingNum,Description,timeLong) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " %(movieId,num,MovieName,EnglishName,OtherName,Director,Actors,Year,Country,Grenre,Rating,RatingNum,Description,timeLong)
            num +=1

            print(sql)
            dbCli.save(sql)



if __name__ == '__main__':
    dbCli = db.MysqlClient()
    start()