#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML

import time

headers = {
    'Connection': "keep-alive",
    'Pragma': "no-cache",
    'Cache-Control': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    # 'Cookie': 'bid=jiPiWxCsnbg; ll="118282"; _vwo_uuid_v2=DBCE20527FFC5F06CAEE989D0D0A1CA6E|d3a1206da68d4dffd70ab6cfdb29e357; _ga=GA1.2.2071961702.1531198334; douban-profile-remind=1; douban-fav-remind=1; gr_user_id=c902b75b-be37-423a-8589-cd0a81e33537; __yadk_uid=TNAAa6V3q1b0pjypK2OWoVq0XWqwrxlC; push_noty_num=0; push_doumail_num=0; ct=y; __utmz=30149280.1552644645.51.23.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=30149280.17490; __utmz=223695111.1553431704.9.4.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/misc/sorry; ps=y; __utmc=30149280; viewed="30172069_27180479_27194720_27611824_30465792_6049132"; ap_v=0,6.0; __utmc=223695111; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1553685746%2C%22https%3A%2F%2Fwww.douban.com%2Fmisc%2Fsorry%3Foriginal-url%3Dhttps%253A%252F%252Fmovie.douban.com%252Fsubject%252F1294240%252F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.2071961702.1531198334.1553682353.1553685746.57; __utma=223695111.2071961702.1531198334.1553682353.1553685746.11; __utmb=223695111.0.10.1553685746; __utmt=1; __utmb=30149280.2.9.1553686761074; dbcl2="174901236:XWSMNyw5H6s"; ck=90dW; _pk_id.100001.4cf6=4d713e5636800d95.1550840314.11.1553686851.1553682360.',
    'cache-control': "no-cache",
    'Postman-Token': "2af87ec3-6dc6-4a15-b553-255dff11dfb7"
    }

def start():
    for i in range(0,120):
        try:
            print('当前页：'+str(i))
            pageToken = i*20
            url = 'https://movie.douban.com/subject/1292052/comments?start={pageToken}&limit=20&sort=new_score&status=P'
            start_url = url.format(pageToken=pageToken)
            print(start_url)
            response = requests.get(start_url,headers=headers)
            # print(response.text)
            html = HTML(response.text)
            allText = html.xpath('//div[@id="comments"]/div//span[@class="short"]/text()')
            # print(allText)

            for text in allText:
                print(text)
                with open('comment.txt','a') as f:
                    f.write(text+'\n')

            print('暂停5秒')
            time.sleep(5)
        except:
            print('error..')
            continue

if __name__ == '__main__':
    start()