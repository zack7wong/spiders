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
    # 'Cookie': 'bid=jiPiWxCsnbg; ll="118282"; _vwo_uuid_v2=DBCE20527FFC5F06CAEE989D0D0A1CA6E|d3a1206da68d4dffd70ab6cfdb29e357; _ga=GA1.2.2071961702.1531198334; douban-profile-remind=1; douban-fav-remind=1; viewed="6049132"; gr_user_id=c902b75b-be37-423a-8589-cd0a81e33537; __yadk_uid=TNAAa6V3q1b0pjypK2OWoVq0XWqwrxlC; push_noty_num=0; push_doumail_num=0; ct=y; __utmz=30149280.1552644645.51.23.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=30149280; __utmc=223695111; __utma=30149280.2071961702.1531198334.1553423249.1553431696.53; __utmv=30149280.17490; __utma=223695111.2071961702.1531198334.1553423249.1553431704.9; __utmb=223695111.0.10.1553431704; __utmz=223695111.1553431704.9.4.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/misc/sorry; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1553431704%2C%22https%3A%2F%2Fwww.douban.com%2Fmisc%2Fsorry%3Foriginal-url%3Dhttps%253A%252F%252Fmovie.douban.com%252Fsubject%252F1294240%252F%22%5D; _pk_ses.100001.4cf6=*; ps=y; __utmt=1; __utmb=30149280.14.9.1553435821761; dbcl2="174901236:XWSMNyw5H6s"; ck=90dW; _pk_id.100001.4cf6=4d713e5636800d95.1550840314.9.1553435842.1553428897.',
    'Host': "movie.douban.com",
    'Pragma': "no-cache",
    'Referer': "https://movie.douban.com/top250?start=225&filter=",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "49939e16-a5ab-4976-a522-6cf49d3b30e1"
    }

def start():
    url = 'https://book.douban.com/ithil_j/activity/book_annual2018/widget/1'
    response = requests.get(url)
    # print(response.text)
    json_index_obj = json.loads(response.text)
    for data in json_index_obj['res']['subjects']:
        print(data)
        bookName = data['title']
        url = data['url']

        print(url)
        # 书名,作者,isbn,标签,出版时间,出版社,内容简介,作者简介,2018年度榜单

        response = requests.get(url)
        # print(response.text)
        html = HTML(response.text)

        jsonStr = re.search('<script type="application.*?">(.*?)</script>',response.text,re.S).group(1).replace('\n','').strip()

        print(jsonStr)
        json_obj = json.loads(jsonStr)

        authorList = []
        for dire in json_obj['author']:
            authorList.append(dire['name'])
        authors = '|'.join(authorList).replace('\'','"')

        isbn = json_obj['isbn']

        tags_list = html.xpath('//div[@class="blank20"]/div[@class="indent"]/span/a/text()')
        tags = '、'.join(tags_list)

        publishDate = re.search('出版年.*?</span>(.*?)<br/>',response.text).group(1).replace('\n','').replace('\'','"').strip()
        chubanshe = re.search('出版社.*?</span>(.*?)<br/>',response.text).group(1).replace('\n','').replace('\'','"').strip()

        jianjie_list = html.xpath('//div[@id="link-report"]//div[@class="intro"]/p/text()')
        jianjie = ''.join(jianjie_list)

        author_jianjie_list =  html.xpath('//div[@class="indent "]//div[@class="intro"]/p/text()')
        author_jianjie = ''.join(author_jianjie_list)

        nianduBandan = 'https://book.douban.com/annual/2018?source=navigation#1'

        save_res = bookName+','+url+','+authors+','+isbn+','+tags+','+publishDate+','+chubanshe+','+jianjie+','+author_jianjie+','+nianduBandan+'\n'
        print(save_res)

        results = {
            'bookName':bookName,
            'url':url,
            'authors':authors,
            'isbn':isbn,
            'tags':tags,
            'publishDate':publishDate,
            'chubanshe':chubanshe,
            'jianjie':jianjie,
            'author_jianjie':author_jianjie,
            'nianduBandan':nianduBandan,
        }

        dbCli.save(results)



if __name__ == '__main__':
    dbCli = db.MongoClient()
    start()