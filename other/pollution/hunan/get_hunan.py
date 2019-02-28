#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
import json
import db

headers = {
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Length': "239",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Cookie': "JSESSIONID=78D417370C78C54428505771310DD0BE; insert_cookie_cnemc=94955953",
    'Host': "123.127.175.61:6375",
    'Origin': "http://123.127.175.61:6375",
    'Pragma': "no-cache",
    'Referer': "http://123.127.175.61:6375/eap/hb/cxfx/jcsjcx/jcjgxxcx/jcjgcxdt.jsp?id=00835BB9C77C40B09AA9495FC400A673",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest",
    'cache-control': "no-cache",
    'Postman-Token': "12d38d74-0e05-4699-985b-20183e19b215"
    }

def deal(json_obj,EntTypeName):
    #企业名称、污染源类型（废水、废气）、监测方式、监测点名称、采样日期、发布日期、监测项目、监测频次、实测浓度、折算浓度、排放标准、限制、是否超标、超标倍数、超标原因
    for data in json_obj['list']:
        try:
            title = data['qymc']
            # EntTypeName = EntTypeName
            jianceFangshi = data['jcfs']
            jiancedianName = data['jcdmc']
            caiyangTime = data['cyrq']
            publishDate = data['fbrq']
            jianceProject = data['jcxmmc']
            jiancePinci = data['pcz']+data['pcdw']
            shiceNongdu = data['scnd']
            zhesuanNongdu = data['zsnd']
            paifangBiaozhun = data['bzmc']
            xianzhi = data['xzsx']
            shifouChaobiao = data['sfcb']
            chaobiaoBeishu = data['cbbs']
            chaobiaoYuanyin = data['cbyy']

            print(title, EntTypeName, jianceFangshi, jiancedianName, caiyangTime, publishDate, jianceProject, jiancePinci,shiceNongdu,zhesuanNongdu,paifangBiaozhun,xianzhi,shifouChaobiao,chaobiaoBeishu,chaobiaoYuanyin)

            sql = "insert into hunan(title, EntTypeName, jianceFangshi, jiancedianName, caiyangTime, publishDate, jianceProject, jiancePinci,shiceNongdu,zhesuanNongdu,paifangBiaozhun,xianzhi,shifouChaobiao,chaobiaoBeishu,chaobiaoYuanyin)" \
                  " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                  % (title, EntTypeName, jianceFangshi, jiancedianName, caiyangTime, publishDate, jianceProject, jiancePinci,shiceNongdu,zhesuanNongdu,paifangBiaozhun,xianzhi,shifouChaobiao,chaobiaoBeishu,chaobiaoYuanyin)
            dbclient.save(sql)
        except:
            continue



def start(item):
    select_list = ['A','B']
    date_list = [{'year':'2014','startDate':'2014-01-01','endDate':'2014-12-31'},{'year':'2015','startDate':'2015-01-01','endDate':'2015-12-31'},{'year':'2016','startDate':'2016-01-01','endDate':'2016-12-31'},{'year':'2017','startDate':'2017-01-01','endDate':'2017-12-31'},{'year':'2018','startDate':'2018-01-01','endDate':'2018-12-31'},{'year':'2019','startDate':'2019-01-01','endDate':'2019-12-31'}]

    id = item['id']
    title = item['title']

    for date in date_list:
        try:
            print('当前日期：'+str(date))
            year = date['year']
            startDate = date['startDate']
            endDate = date['endDate']
            for select in select_list:
                try:
                    print('当前选择:'+select)
                    if select == 'A':
                        EntTypeName = '废气'
                    else:
                        EntTypeName = '废水'
                    url = 'http://123.127.175.61:6375/eap/jcjgcxAction/listnew.action'
                    body = 'jcsj=gdsj&jcsjnf={year}&jcsjgdsj=qn&whereBean.jcrqks={startDate}&whereBean.jcrqjs={endDate}&whereBean.jclb=0&whereBean.qybh={id}&whereBean.sjlb={select}&whereBean.jcfs=A&jumpPage={pageToken}&pageNo={pageToken}&interval=10&total=&totalPage=0'

                    #获取第一页
                    data = body.format(year=year,startDate=startDate,endDate=endDate,id=id,select=select,pageToken=1)
                    try:
                        response = requests.post(url,headers=headers,data=data,timeout=10)
                    except:
                        continue
                    # print(response.text)
                    json_obj = json.loads(response.text)

                    if len(json_obj['list']) == 0:
                        print('无数据')
                        continue

                    #处理第一页
                    deal(json_obj,EntTypeName)

                    #获取总数
                    totalPageNo = json_obj['totalPageNo']
                    print('总页数：'+str(totalPageNo))

                    #处理剩余页数
                    for i in range(2,totalPageNo+1):
                        try:
                            print('当前页数：'+str(i))
                            data = body.format(year=year, startDate=startDate, endDate=endDate, id=id, select=select, pageToken=i)
                            response = requests.post(url, headers=headers, data=data,timeout=10)
                            # print(response.text)
                            json_obj = json.loads(response.text)
                            deal(json_obj,EntTypeName)
                        except:
                            continue
                except:
                    continue
        except:
            continue


if __name__ == '__main__':
    dbclient = db.MysqlClient()
    item_list = []
    with open('hunan_id.txt') as f:
        results = f.readlines()
        for res in results:
            id = res.split(',')[0]
            title = res.split(',')[1]
            obj = {
                'id':id,
                'title':title,
            }
            item_list.append(obj)

    for item in item_list:
        print(item)
        try:
            start(item)
        except:
            continue