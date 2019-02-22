#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import db
import math

def get_comment(sightId,commentCount):
    totalNum = math.ceil(int(commentCount)/10)
    print(totalNum)
    #翻页
    for i in range(1,int(totalNum)+1):
        print('当前页：'+str(i))
        start_url = 'https://touch.piao.qunar.com/touch/queryCommentsAndTravelTips.json?type=mp&pageSize=10&fromType=SIGHT&pageNum={pageToken}&sightId={sightId}&tagType=0'
        url = start_url.format(pageToken=i,sightId=sightId)
        print(url)
        try:
            response = requests.get(url)
            # print(response.text)

            json_obj = json.loads(response.text)
            #字段处理
            for data in json_obj['data']['commentList']:
                print(data)
                commentId = data['commentId']
                author = data['author']
                content = data['content']
                date = data['date']
                sightName = data['sightName']

                #存数据
                sql = "insert into qunarComment(sightId,commentId,author,content,date,sightName) values ('%s','%s','%s','%s','%s','%s')" % (sightId, commentId, author, content, date, sightName)+ "ON DUPLICATE KEY UPDATE content='%s'"%(content)
                mysqlCli.save(sql)
        except:
            print('未知错误')
            continue


def get_sight():
    #翻页
    for i in range(1,8):
        print('当前列表页：'+str(i))
        start_url = 'http://touch.piao.qunar.com/touch/list.json?region=西宁&isForeign=false&page={pageToken}&pageSize=10&keyword=景点门票'
        url = start_url.format(pageToken=i)
        print(url)
        response = requests.get(url)
        # print(response.text)
        json_obj = json.loads(response.text)
        #字段处理
        for data in json_obj['data']['sightList']:
            sightId = data['id']
            name = data['name']

            sightSimpleDesc = data['sightSimpleDesc'] if 'sightSimpleDesc' in data else '' #字段不存在特殊处理
            url = 'http:'+ data['url']
            commentCount = data['commentCount']
            addressDetail = data['addressDetail']

            obj = {
                'sightId': sightId,
                'name': name,
                # 'level':data['level'],
                # 'address':data['address'],
                'sightSimpleDesc': sightSimpleDesc,
                'url': url,
                'commentCount': commentCount,
                'addressDetail': addressDetail,
            }
            print(json.dumps(obj))
            #存数据
            sql = "insert into qunarSight(sightId,name,sightSimpleDesc,url,commentCount,addressDetail) values ('%s','%s','%s','%s','%s','%s')"%(sightId,name,sightSimpleDesc,url,commentCount,addressDetail)\
                  + "ON DUPLICATE KEY UPDATE sightSimpleDesc='%s'"%(sightSimpleDesc)
            # print(sql)
            mysqlCli.save(sql)

            #获取评论
            get_comment(sightId,commentCount)


def start():
    get_sight()


if __name__ == '__main__':
    #实例化数据库对象
    mysqlCli = db.MysqlClient()
    start()
