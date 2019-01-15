#!/usr/bin/env python
# -*- coding:utf-8 -*-

import download
import json
import config
import math
import time
import dateutil.parser
from urllib.parse import quote
from lxml.etree import HTML
from lxml import etree
import time

#微博关键字搜索爬虫：某一时间段内某关键字的所有微博的 发博用户名，微博内容，微博内容的评论内容，转发量，评论量，点赞量，发博时间，评论内容的评论时间，当前时间。

# 例如：13年-14年关键字 速腾断轴 的所有微博和微博评论的以上字段。

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
            commentTotalPage = res.split(',')[4].strip()
            obj ={
                'keyword':keyword,
                'startDate':startDate,
                'endDate':endDate,
                'totalPage':totalPage,
                'commentTotalPage':commentTotalPage,
            }
            item_list.append(obj)
    return item_list

def getTimeStamp(dateStr):
    dateTime = dateutil.parser.parse(dateStr)
    time_tuple = (dateTime.year, dateTime.month, dateTime.day, dateTime.hour, dateTime.minute, dateTime.second, 0, 0, 0)
    timestamp = int(time.mktime(time_tuple))
    return timestamp

def get_comment(id,item):
    commentTotalPage = int(item['commentTotalPage'])
    comment_url = 'https://m.weibo.cn/comments/hotflow?id={id}&mid={id}&max_id={max_id}&max_id_type=0'
    max_id = 0
    for i in range(1,commentTotalPage+1):
        start_url = comment_url.format(id=id,max_id=max_id)
        response = down.get_html(start_url)
        if response:
            json_obj = json.loads(response.text)
            if json_obj['ok'] == 0:
                print('评论为空')
                return
            for data in json_obj['data']['data']:
                commentId = data['id']
                comment_content = data['text']
                publishDate = getTimeStamp(data['created_at'])
                comment_publishDateStr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(publishDate))


                if commentId in commentId_list:
                    continue
                else:
                    commentId_list.append(commentId)
                save_res = id+'||'+commentId+'||'+comment_content+'||'+comment_publishDateStr
                save_res = save_res.replace(',', '，').replace(' ', '').replace('\n', ' ').replace('\r', ' ').replace('||', ',').strip()+'\n'
                print(save_res)
                with open('comment.csv','a') as f:
                    f.write(save_res)
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
        id = html.xpath('string(//div[@class="card-wrap"]/@mid)')
        if id == '':
            print('搜索无结果')
            return


        if id in postId_list:
            continue
        else:
            postId_list.append(id)

        url = 'https://m.weibo.cn/status/'+id
        userName = html.xpath('string(//a[@class="name"])')
        content = html.xpath('//p[@class="txt"]//text()')
        content = ''.join(content).strip()
        publishDateStr = html.xpath('string(//p[@class="from"]/a)').strip()
        reposts_count = html.xpath('string(//div[@class="card-act"]/ul/li[2]/a/text())').replace('转发','')
        comments_count = html.xpath('string(//div[@class="card-act"]/ul/li[3]/a/text())').replace('评论', '')
        attitudes_count = html.xpath('string(//div[@class="card-act"]/ul/li[4]/a/em/text())')
        crawl_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())


        save_res = keyword+'||'+startDate+'||'+endDate+'||'+id +'||'+url+'||'+userName+'||'+content+'||'+publishDateStr+'||'+reposts_count+'||'+comments_count+'||'+attitudes_count+'||'+crawl_time
        save_res = save_res.replace(',','，').replace(' ','').replace('\n',' ').replace('\r',' ').replace('||',',').strip()+'\n'
        print(save_res)
        with open('post.csv','a',encoding='utf8',errors='ignore') as f:
            f.write(save_res)

        #处理评论
        get_comment(id,item)

def main(item):
    keyword = quote(item['keyword'])
    startDate = item['startDate']
    endDate = item['endDate']
    pageNum = int(item['totalPage'])
    URL = 'https://s.weibo.com/weibo/%25E7%258E%258B%25E6%2580%259D%25E8%2581%25AA?q={keyword}&typeall=1&suball=1&timescope=custom:{startDate}:{endDate}&Refer=g&page={pageToken}'

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

if __name__ == '__main__':
    down = download.Download()
    item_list = read()
    for obj in item_list:
        print('当前关键词：'+obj['keyword'])
        main(obj)