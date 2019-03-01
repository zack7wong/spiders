#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
from lxml.etree import HTML
import re
from urllib.parse import quote
import db

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    # 'Content-Length': "11020",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cookie': "ASP.NET_SessionId=aqmre555s400d2rjr2jwyb45; ASPSESSIONIDQQSCDSAD=CNGALCLBDCABNHGOBIAJADKP; UM_distinctid=1692895207442e-0a6ea7e37cf166-36627102-1fa400-169289520752d0; ASPSESSIONIDQQSDATCD=MHBFIKEDAOKLPNNGJBAPFKLP; security_session_verify=dfdee412f18a0e29a462fff1d7927d5c; ASPSESSIONIDAAATAQAB=BNLCEAMDCDININEHGEIDJAEM; CNZZDATA1273855805=1411670600-1551164027-%7C1551422062",
    'Host': "www.aepb.gov.cn:8080",
    'Origin': "http://www.aepb.gov.cn:8080",
    'Pragma': "no-cache",
    # 'Referer': "http://www.aepb.gov.cn:8080/WRYJG/STZXGK/STAuto_Data.aspx?NewsID=762773720000&zdlx=fq",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "25cb69a7-fd8a-4ce4-9ba6-73333b4d787f"
    }

def get_canInfo(item,EntType):
    url = 'http://www.aepb.gov.cn:8080/WRYJG/STZXGK/STAuto_Data.aspx?NewsID={id}&zdlx={EntType}'.format(id=item['id'],EntType=EntType)
    response = requests.get(url,timeout=40)
    # print(response.text)
    html = HTML(response.text)
    jianceCodeList = html.xpath('//select[@id="DropPk"]/option/@value')
    jianceCodeNameList = html.xpath('//select[@id="DropPk"]/option/text()')

    jianceCodeObjList = []
    for jianceCode,jianceCodeName in zip(jianceCodeList,jianceCodeNameList):
        obj = {
            'jianceCode':jianceCode,
            'jianceCodeName':jianceCodeName,
        }
        jianceCodeObjList.append(obj)


    __VIEWSTATE = re.search('id="__VIEWSTATE" value="(.*?)"',response.text).group(1)
    __VIEWSTATE = quote(__VIEWSTATE).replace('/','%2F')
    # totalPage = int(re.search('当前第1/(\d+)页',response.text).group(1))
    print(jianceCodeList)
    # print(__VIEWSTATE)
    return jianceCodeObjList,__VIEWSTATE

def deal(html,item,EntType,jianceCodeName):
    if EntType == 'fs':
        EntTypeName = '废水'
        trNum = 2
    else:
        EntTypeName = '废气'
        trNum = 3
    title = item['title']
    jiancedianName = jianceCodeName

    tr_list = html.xpath('//table[@class="app_table"]//tr')

    #获取名称
    tdNameList = []
    for td in tr_list[0][2:]:
        tdName = td.xpath('string(./text())')
        tdNameList.append(tdName)
        # print(tdName)


    for td in tr_list[trNum:]:
        try:
            jianceTime = td.xpath('string(./td[1]/text())').strip()
            pailiang = td.xpath('string(./td[2]/text())').strip()
            # print(jianceTime)

            for i in range(len(tdNameList)):
                try:
                    if EntType == 'fs':
                        shiceValue = td.xpath('string(./td[' + str((i + 1) * trNum + 1) + ']/text())').strip()
                        zhesuanNongdu = '0'
                        paifangliang = td.xpath('string(./td[' + str((i + 1) * trNum + 2) + ']/text())').strip()
                    else:
                        shiceValue = td.xpath('string(./td[' + str((i + 1) * trNum ) + ']/text())').strip()
                        zhesuanNongdu = td.xpath('string(./td[' + str((i + 1) * trNum + 1) + ']/text())').strip()
                        paifangliang = td.xpath('string(./td[' + str((i + 1) * trNum + 2) + ']/text())').strip()

                    jianceType = tdNameList[i]
                    thisObj = {
                        'title':title,
                        'EntTypeName':EntTypeName,
                        'jianceTime':jianceTime,
                        'jiancedianName':jiancedianName,
                        'pailiang':pailiang,
                        'jianceType':tdNameList[i],
                        'shiceValue':shiceValue,
                        'zhesuanNongdu':zhesuanNongdu,
                        'paifangliang':paifangliang,
                    }
                    print(thisObj)

                    # print(title,EntTypeName,jianceTime,jiancedianName,pailiang,jianceType,shiceValue,zhesuanNongdu,paifangliang)

                    sql = "insert into anhui(title,EntTypeName,jianceTime,jiancedianName,pailiang,jianceType,shiceValue,zhesuanNongdu,paifangliang)" \
                    " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                    % (title,EntTypeName,jianceTime,jiancedianName,pailiang,jianceType,shiceValue,zhesuanNongdu,paifangliang) + "ON DUPLICATE KEY UPDATE title='%s'" % (title)
                    dbclient.save(sql)
                except:
                    continue
        except:
            continue


def start(item):
    EntTypeName_list = ['fs','fq']
    dateList = [{'startDate':'2014-01-01+00%3A00%3A00','endDate':'2014-12-31+23%3A55%3A50'},{'startDate':'2015-01-01+00%3A00%3A00','endDate':'2015-12-31+23%3A55%3A50'},{'startDate':'2016-01-01+00%3A00%3A00','endDate':'2016-12-31+23%3A55%3A50'},{'startDate':'2017-01-01+00%3A00%3A00','endDate':'2017-12-31+23%3A55%3A50'},{'startDate':'2018-01-01+00%3A00%3A00','endDate':'2018-12-31+23%3A55%3A50'},{'startDate':'2019-01-01+00%3A00%3A00','endDate':'2019-02-26+23%3A55%3A50'}]

    for EntType in EntTypeName_list:
        try:
            print('当前废水废气类型：'+str(EntType))
            jianceCodeList, __VIEWSTATE = get_canInfo(item,EntType)

            for jianceCodeObj in jianceCodeList:
                try:
                    jianceCode = jianceCodeObj['jianceCode']
                    jianceCodeName = jianceCodeObj['jianceCodeName']
                    print('当前检测口类型：'+str(jianceCodeName))

                    for dateObj in dateList:
                        try:
                            print('当前日期：'+str(dateObj))
                            startDate = dateObj['startDate']
                            endDate = dateObj['endDate']

                            #获取第一页
                            start_url = 'http://www.aepb.gov.cn:8080/WRYJG/STZXGK/STAuto_Data.aspx?NewsID={id}&zdlx={EntType}'.format(id=item['id'],EntType=EntType)
                            body = '__EVENTTARGET=DropPk&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE={__VIEWSTATE}&txtkssj={startDate}&txtjssj={endDate}&DropPk={jianceCode}&AspNetPager1_input={pageToken}&AspNetPager1=go'
                            data = body.format(__VIEWSTATE=__VIEWSTATE,startDate=startDate,endDate=endDate,jianceCode=jianceCode,pageToken=1)
                            response = requests.post(start_url,data=data,headers=headers,timeout=40)
                            # print(response.text)

                            #获取总条数
                            totalPage = int(re.search('当前第1/(\d+)页',response.text).group(1))
                            totalNum = int(re.search('当前第1/(\d+)页 共(\d+)条记录',response.text).group(2))
                            print('总数：'+str(totalNum))
                            print('总页数：'+str(totalPage))
                            if totalNum == 0:
                                print('无数据')
                                continue

                            #处理第一页
                            print('当前页：1')
                            html = HTML(response.text)
                            deal(html,item,EntType,jianceCodeName)

                            #处理剩余页数
                            for i in range(2,totalPage+1):
                                try:
                                    print('当前页：'+str(i))
                                    body = '__EVENTTARGET=DropPk&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE={__VIEWSTATE}&txtkssj={startDate}&txtjssj={endDate}&DropPk={jianceCode}&AspNetPager1_input={pageToken}&AspNetPager1=go'
                                    data = body.format(__VIEWSTATE=__VIEWSTATE, startDate=startDate, endDate=endDate,jianceCode=jianceCode, pageToken=i)
                                    response = requests.post(start_url, data=data, headers=headers,timeout=40)
                                    html = HTML(response.text)
                                    deal(html,item,EntType,jianceCodeName)
                                except:
                                    continue
                        except:
                            continue
                except:
                    continue
        except:
            continue


if __name__ == '__main__':
    dbclient = db.MysqlClient()
    item_list = []
    with open('anhui_id.txt') as f:
        results = f.readlines()
        for res in results:
            id = res.split(',')[0]
            title = res.split(',')[1].strip()
            obj ={
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