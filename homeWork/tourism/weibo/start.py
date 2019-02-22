#!/usr/bin/env python
# -*- coding:utf-8 -*-

import download
import json
import config
import db
import math
import time
import dateutil.parser
from urllib.parse import quote
from lxml.etree import HTML
from lxml import etree
import time

postId_list = []
commentId_list = []

def read():

    #配置url请求的一些参数
    item_list = []
    #typeall=1   xsort=hot  scope=ori  atten=1   vip=1  category=4   viewpoint=1
    res = '大理旅游,2019-01-01,2019-01-16,50,10,typeall=1'
    keyword = res.split(',')[0]
    startDate = res.split(',')[1]
    endDate = res.split(',')[2]
    totalPage = res.split(',')[3]
    commentTotalPage = res.split(',')[4]
    queryType = res.split(',')[5].strip()
    #返回json对象
    obj ={
        'keyword':keyword,
        'startDate':startDate,
        'endDate':endDate,
        'totalPage':totalPage,
        'commentTotalPage':commentTotalPage,
        'queryType':queryType,
    }
    item_list.append(obj)
    return item_list

def getTimeStamp(dateStr):
    #处理时间问题
    dateTime = dateutil.parser.parse(dateStr)
    time_tuple = (dateTime.year, dateTime.month, dateTime.day, dateTime.hour, dateTime.minute, dateTime.second, 0, 0, 0)
    timestamp = int(time.mktime(time_tuple))
    return timestamp

def get_comment(id,item):
    #获取评论
    commentTotalPage = int(item['commentTotalPage'])
    comment_url = 'https://m.weibo.cn/comments/hotflow?id={id}&mid={id}&max_id={max_id}&max_id_type=0'
    max_id = 0
    #翻页
    for i in range(1,commentTotalPage+1):
        time.sleep(2)
        print('暂停2秒')
        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            'cache-control': "no-cache",
        }
        start_url = comment_url.format(id=id,max_id=max_id)
        print(start_url)
        try:
            response = down.get_html(start_url,headers=headers)
            if response:
                json_obj = json.loads(response.text)
                if json_obj['ok'] == 0:
                    print('评论为空')
                    return
                #处理字段
                for data in json_obj['data']['data']:
                    commentId = data['id']
                    comment_content = data['text']
                    publishDate = getTimeStamp(data['created_at'])
                    comment_publishDateStr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(publishDate))


                    if commentId in commentId_list:
                        continue
                    else:
                        commentId_list.append(commentId)

                    #存数据库
                    sql = "insert into weiboComment(commentId,content,commentTime) values ('%s','%s','%s')" % (
                        commentId, comment_content, comment_publishDateStr,) \
                          + "ON DUPLICATE KEY UPDATE content='%s'" % (comment_content)
                    print(sql)
                    mysqlCli.save(sql)

                    # save_res = id+'\t||\t'+commentId+'||'+comment_content+'||'+comment_publishDateStr
                    # save_res = save_res.replace(',', '，').replace(' ', '').replace('\n', ' ').replace('\r', ' ').replace('||', ',').strip()+'\n'
                    # print(save_res)
                    # with open('comment.csv','a',encoding='gbk',errors='ignore') as f:
                    #     f.write(save_res)
            else:
                with open('评论出错url.txt', 'a') as f:
                    f.write(str(start_url))
                continue
        except:
            with open('评论出错url.txt', 'a') as f:
                f.write(str(start_url))
            continue

def parse(item,response):
    keyword = item['keyword']
    startDate = item['startDate']
    endDate = item['endDate']

    allhtml = HTML(response.text)
    #xpath获取数据
    allitem_list = allhtml.xpath('//div[@id="pl_feedlist_index"]//div[@class="card-wrap"]')

    #处理字段
    for etreeItem in allitem_list:
        itemStr = etree.tostring(etreeItem)
        html = HTML(itemStr)
        id = html.xpath('string(//div[@class="card-wrap"]/@mid)')
        if id == '':
            print('搜索无结果')
            return True


        if id in postId_list:
            continue
        else:
            postId_list.append(id)

        #xpath获取各个数据
        url = 'https://m.weibo.cn/status/'+id
        userName = html.xpath('string(//a[@class="name"])')
        content = html.xpath('//p[@class="txt"]//text()')
        content = ''.join(content).strip()
        publishDateStr = html.xpath('string(//p[@class="from"]/a)').strip()
        reposts_count = html.xpath('string(//div[@class="card-act"]/ul/li[2]/a/text())').replace('转发','')
        comments_count = html.xpath('string(//div[@class="card-act"]/ul/li[3]/a/text())').replace('评论', '')
        attitudes_count = html.xpath('string(//div[@class="card-act"]/ul/li[4]/a/em/text())')
        crawl_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())

        #存数据库
        sql = "insert into weiboSight(keyword,startDate,endDate,postId,url,userName,content,publishDateStr,reposts_count,comments_count,attitudes_count,crawl_time) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
            keyword, startDate, endDate, id, url, userName, content, publishDateStr, reposts_count, comments_count,
            attitudes_count, crawl_time) \
              + "ON DUPLICATE KEY UPDATE reposts_count='%s'" % (reposts_count)
        print(sql)
        mysqlCli.save(sql)

        # save_res = keyword+'||'+startDate+'||'+endDate+'||\t'+id +'||'+url+'||'+userName+'||'+content+'||'+publishDateStr+'||'+reposts_count+'||'+comments_count+'||'+attitudes_count+'||'+crawl_time
        # save_res = save_res.replace(',','，').replace(' ','').replace('\n',' ').replace('\r',' ').replace('||',',').strip()+'\n'
        # print(save_res)
        # with open('post.csv','a',encoding='gbk',errors='ignore') as f:
        #     f.write(save_res)

        #处理评论
        get_comment(id,item)

def main(item):
    #设置参数
    keyword = quote(item['keyword'])
    startDate = item['startDate']
    endDate = item['endDate']
    pageNum = int(item['totalPage'])
    queryType = item['queryType']
    URL = 'https://s.weibo.com/weibo/%25E7%258E%258B%25E6%2580%259D%25E8%2581%25AA?q={keyword}&{queryType}&suball=1&timescope=custom:{startDate}:{endDate}&Refer=g&page={pageToken}'

    #翻页
    for i in range(1,pageNum+1):
        print('当前页数：'+str(i))
        #拼接url
        start_url = URL.format(keyword=keyword,queryType=queryType,pageToken=i,startDate=startDate,endDate=endDate)
        print(start_url)
        response = down.get_html(start_url)
        if response:
            # print(response.text):
            parse(item,response)
        else:
            print('网络请求失败')
            continue


if __name__ == '__main__':
    #实例化数据库，下载器对象
    mysqlCli = db.MysqlClient()
    down = download.Download()
    #获取配置参数
    item_list = read()
    # with open('post.csv', 'w', encoding='gbk', errors='ignore') as f:
    #     f.write('关键词,开始时间,结束时间,id,链接,用户名,内容,发布时间,转发数,评论数,点赞数,爬取时间\n')
    # with open('comment.csv', 'w', encoding='gbk', errors='ignore') as f:
    #     f.write('id,评论id,评论内容,评论时间\n')
    for obj in item_list:
        print('当前关键词：'+obj['keyword'])
        main(obj)