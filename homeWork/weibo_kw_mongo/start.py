#!/usr/bin/env python
# -*- coding:utf-8 -*-

import download
import json
import config
import math
import time
import db
import dateutil.parser
from urllib.parse import quote
from lxml.etree import HTML
from lxml import etree
import time
import re


postId_list = []
commentId_list = []

def read():
    item_list = []
    with open('keyword.txt') as f:
        results = f.readlines()
        for res in results:
            keyword = res.split(',')[0]
            startDate = res.split(',')[1]
            endDate = res.split(',')[2]
            totalPage = res.split(',')[3]
            commentTotalPage = res.split(',')[4]
            wenzhangPage = res.split(',')[5].strip()
            obj ={
                'keyword':keyword,
                'startDate':startDate,
                'endDate':endDate,
                'totalPage':totalPage,
                'commentTotalPage':commentTotalPage,
                'wenzhangPage':wenzhangPage,
            }
            item_list.append(obj)
    return item_list

def getTimeStamp(dateStr):
    dateTime = dateutil.parser.parse(dateStr)
    time_tuple = (dateTime.year, dateTime.month, dateTime.day, dateTime.hour, dateTime.minute, dateTime.second, 0, 0, 0)
    timestamp = int(time.mktime(time_tuple))
    return timestamp

def get_comment(postId,item):
    commentTotalPage = int(item['commentTotalPage'])
    comment_url = 'https://m.weibo.cn/comments/hotflow?id={id}&mid={id}&max_id={max_id}&max_id_type=0'
    max_id = 0
    for i in range(1,commentTotalPage+1):
        start_url = comment_url.format(id=postId,max_id=max_id)
        response = down.get_html(start_url)
        if response:
            json_obj = json.loads(response.text)
            if json_obj['ok'] == 0:
                print('评论为空')
                return
            for data in json_obj['data']['data']:
                print(json.dumps(data))
                userId = str(data['user']['id'])
                userName = str(data['user']['screen_name'])
                urank = str(data['user']['urank'])
                commentId = data['id']
                comment_content = data['text']
                publishDate = getTimeStamp(data['created_at'])
                comment_publishDateStr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(publishDate))


                if commentId in commentId_list:
                    continue
                else:
                    commentId_list.append(commentId)
                save_res = postId+'||'+commentId+'||'+comment_content+'||'+comment_publishDateStr
                save_res = save_res.replace(',', '，').replace(' ', '').replace('\n', ' ').replace('\r', ' ').replace('||', ',').strip()+'\n'
                print(save_res)
                # with open('comment.csv','a') as f:
                #     f.write(save_res)
                obj = {
                    'postId':postId,
                    'userId':userId,
                    'userName':userName,
                    'urank':urank,
                    'commentId':commentId,
                    'comment_content':comment_content,
                    'comment_publishDateStr':comment_publishDateStr,
                }
                mongoClient.save_comment(obj)
        else:
            print('评论请求失败')
            continue

def parse(item,response):
    keyword = item['keyword']
    startDate = item['startDate']
    endDate = item['endDate']

    allhtml = HTML(response.text)
    allitem_list = allhtml.xpath('//div[@id="pl_feedlist_index"]//div[@class="card-wrap"]')
    for etreeItem in allitem_list:
        itemStr = etree.tostring(etreeItem)
        html = HTML(itemStr)
        postId = html.xpath('string(//div[@class="card-wrap"]/@mid)')
        if postId == '':
            print('搜索无结果')
            return

        if postId in postId_list:
            continue
        else:
            postId_list.append(postId)

        url = 'https://m.weibo.cn/status/'+postId
        userName = html.xpath('string(//a[@class="name"])')
        content = html.xpath('//p[@class="txt"]//text()')
        content = ''.join(content).strip()
        publishDateStr = html.xpath('string(//p[@class="from"]/a)').strip()
        reposts_count = html.xpath('string(//div[@class="card-act"]/ul/li[2]/a/text())').replace('转发','')
        comments_count = html.xpath('string(//div[@class="card-act"]/ul/li[3]/a/text())').replace('评论', '')
        attitudes_count = html.xpath('string(//div[@class="card-act"]/ul/li[4]/a/em/text())')
        crawl_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())


        save_res = keyword+'||'+startDate+'||'+endDate+'||'+postId +'||'+url+'||'+userName+'||'+content+'||'+publishDateStr+'||'+reposts_count+'||'+comments_count+'||'+attitudes_count+'||'+crawl_time
        save_res = save_res.replace(',','，').replace(' ','').replace('\n',' ').replace('\r',' ').replace('||',',').strip()+'\n'
        print(save_res)
        # with open('post.csv','a',encoding='utf8',errors='ignore') as f:
        #     f.write(save_res)
        obj = {
            'keyword':keyword,
            'startDate':startDate,
            'endDate':endDate,
            'postId':postId,
            'url':url,
            'userName':userName,
            'content':content,
            'publishDateStr':publishDateStr,
            'reposts_count':reposts_count,
            'comments_count':comments_count,
            'attitudes_count':attitudes_count,
            'crawl_time':crawl_time,
        }
        mongoClient.save_post(obj)

        #处理评论
        get_comment(postId,item)

def parse_wenzhang(item,response):
    keyword = item['keyword']
    startDate = item['startDate']
    endDate = item['endDate']

    headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cache-Control': "no-cache",
        'Connection': "keep-alive",
        'Cookie': "SINAGLOBAL=2741068042226.078.1532572562158; Ugrow-G0=7e0e6b57abe2c2f76f677abd9a9ed65d; login_sid_t=0508861b225cb94d51cb2702234fb284; cross_origin_proto=SSL; YF-V5-G0=5468b83cd1a503b6427769425908497c; _s_tentry=login.sina.com.cn; Apache=6704202225558.143.1546953901646; ULV=1546953901664:14:1:1:6704202225558.143.1546953901646:1545634557172; SSOLoginState=1547092029; YF-Page-G0=59104684d5296c124160a1b451efa4ac; wvr=6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFX9gU.0AvvHpkroN8y6_.s5JpX5KMhUgL.Fo-ESoB0SoMXeh.2dJLoI7L.9JLXSh2Reh2t; ALF=1579085368; SCF=AlH-htFhOOtuSJnrHnxgPfbVUuhc309qQH8-v0vpUXbAuvDR4CBHQPwI_Yx8qvscnx7JEegFJ1iw0ZsybYeIx2Y.; SUB=_2A25xOcrqDeThGeNM7VYS9inIyzWIHXVSTrsirDV8PUNbmtBeLUTAkW9NTh6TnH-z1Pwg9kfNZYt3VQcuUbILLmAi; SUHB=0U1Z5MKLEFBg2v; wb_view_log_5264367409=1920*10801; UOR=www.google.ie,www.weibo.com,www.google.com; WBStorage=d2ec5569c294a2d0|undefined",
        'Host': "weibo.com",
        'Pragma': "no-cache",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        'cache-control': "no-cache",
    }

    allhtml = HTML(response.text)
    allurl_list = allhtml.xpath('//div[@id="pl_feedlist_index"]/div[@class="card-wrap"]//h3/a/@href')
    # print(allurl_list)
    for url in allurl_list:
        if re.search('https://weibo.com/ttarticle/',url):
            response = down.get_html(url,headers=headers)

            # print(response.text)
            if response:
                html = HTML(response.text)
                title = html.xpath('string(//div[@class="title"])')
                wenzhangId = re.search('id=(\d+)',url).group(1)
                userName = html.xpath('string(//em[@class="W_autocut"])')
                content = html.xpath('string(//div[@class="WB_editor_iframe"])').strip()
                publishDateStr = html.xpath('string(//span[@class="time"])').replace('发布于','').strip()
                reposts_count = html.xpath('string(//ul[@class="WB_row_line WB_row_r3 clearfix S_line2"]/li[1]//span[@class="line S_line1"])').replace('转发','').strip()
                comments_count = html.xpath('string(//ul[@class="WB_row_line WB_row_r3 clearfix S_line2"]/li[2]//span[@class="line S_line1"])').replace('评论','').strip()
                attitudes_count = html.xpath('string(//ul[@class="WB_row_line WB_row_r3 clearfix S_line2"]/li[3]//span[@class="line S_line1"])')
                crawl_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                obj = {
                    'keyword': keyword,
                    'startDate': startDate,
                    'endDate': endDate,
                    'title': title,
                    'wenzhangId': wenzhangId,
                    'url': url,
                    'userName': userName,
                    'content': content,
                    'publishDateStr': publishDateStr,
                    'reposts_count': reposts_count,
                    'comments_count': comments_count,
                    'attitudes_count': attitudes_count,
                    'crawl_time': crawl_time,
                }
                print(obj)
                mongoClient.save_wenzhang(obj)


def main(item):
    keyword = quote(item['keyword'])
    startDate = item['startDate']
    endDate = item['endDate']
    pageNum = int(item['totalPage'])
    wenzhangPageNum = int(item['wenzhangPage'])
    URL = 'https://s.weibo.com/weibo/%25E7%258E%258B%25E6%2580%259D%25E8%2581%25AA?q={keyword}&typeall=1&suball=1&timescope=custom:{startDate}:{endDate}&Refer=g&page={pageToken}'

    #获取微博和评论
    for i in range(1,pageNum+1):
        start_url = URL.format(keyword=keyword,pageToken=i,startDate=startDate,endDate=endDate)
        print(start_url)
        response = down.get_html(start_url)
        if response:
            # print(response.text):
            parse(item,response)
        else:
            print('网络请求失败')
            continue

    #获取文章
    wenzhang_url = 'https://s.weibo.com/article?q={keyword}&Refer=weibo_article&page={pageToken}'
    for i in range(1,wenzhangPageNum+1):
        start_url = wenzhang_url.format(keyword=keyword,pageToken=i)
        print(start_url)
        response = down.get_html(start_url)
        if response:
            # print(response.text)
            parse_wenzhang(item,response)
        else:
            print('网络请求失败')
            continue


if __name__ == '__main__':
    down = download.Download()
    mongoClient = db.MongoClient()
    item_list = read()
    for obj in item_list:
        print('当前关键词：'+obj['keyword'])
        main(obj)