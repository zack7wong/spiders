#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import requests
import re
import db
from lxml.etree import HTML
from urllib.parse import quote

get_headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Cookie': "ASP.NET_SessionId=z54lc0bvs3itgsbvht1lia55",
    'Host': "1.189.191.146:8000",
    'Pragma': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    'cache-control': "no-cache",
}

post_headers = {
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Length': "14656",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Cookie': "ASP.NET_SessionId=z54lc0bvs3itgsbvht1lia55",
    'Host': "1.189.191.146:8000",
    'Origin': "http://1.189.191.146:8000",
    'Pragma': "no-cache",
    'Referer': "http://1.189.191.146:8000",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    'X-MicrosoftAjax': "Delta=true",
    'cache-control': "no-cache",
}

def get_start_VIEWSTATE(url):
    response = requests.get(url,headers=get_headers,timeout=20)
    # print(response.text)
    html = HTML(response.text)
    __VIEWSTATE = re.search('id="__VIEWSTATE" value="(.*?)"',response.text).group(1)
    __VIEWSTATE = quote(__VIEWSTATE).replace('/','%2F')
    # print(__VIEWSTATE)
    # print(__EVENTVALIDATION)
    # print(rd_DataType)

    return __VIEWSTATE

def get_nextId_VIEWSTATE(response):
    html = HTML(response.text)
    nextId = html.xpath('string(//table[@id="ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_gvHistoryData"]//table[@class="PagerStyleInfo5"]//td[last()-1]/@name)').strip()
    nextId = quote(nextId)

    __VIEWSTATE = re.search('\|__VIEWSTATE\|(.*?)\|\d+\|hiddenField', response.text).group(1)
    __VIEWSTATE = quote(__VIEWSTATE).replace('/', '%2F')

    return __VIEWSTATE,nextId

def deal(response,title,EntTypeName):
    # 企业名称、污染源类型（废水、废气）、监测点位、监测方式、监测时间、监测项目、执行标准、检测值、单位、标准限值、是否达标、是否停产、备注
    html = HTML(response.text)
    tr_list = html.xpath('//table[@id="ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_gvHistoryData"]//tr')
    for tr in tr_list[1:-2]:
        try:
            jiancedianName = tr.xpath('string(./td[1]/text())')
            jianceType = tr.xpath('string(./td[2]/text())')
            jianceTime = tr.xpath('string(./td[3]/text())')
            jianceProject = tr.xpath('string(./td[4]/text())')
            zhixingBiaozhun = tr.xpath('string(./td[5]/text())')
            jianceValue = tr.xpath('string(./td[6]/span/text())')
            danwei = tr.xpath('string(./td[7]/text())')
            biaozhunXianzhi = tr.xpath('string(./td[8]/span/text())')
            shifouDabiao = tr.xpath('string(./td[9]/span/text())')
            shifouTingchan = tr.xpath('string(./td[11]/span/text())')
            beizhu = tr.xpath('string(./td[12]/text())')
            obj = {
                'title': title,
                'EntTypeName': EntTypeName,
                'jiancedianName': jiancedianName,
                'jianceType': jianceType,
                'jianceTime': jianceTime,
                'jianceProject': jianceProject,
                'zhixingBiaozhun': zhixingBiaozhun,
                'jianceValue': jianceValue,
                'danwei': danwei,
                'biaozhunXianzhi': biaozhunXianzhi,
                'shifouDabiao': shifouDabiao,
                'shifouTingchan': shifouTingchan,
                'beizhu': beizhu,
            }
            print(obj)
            sql = "insert into heilongjiang(title,EntTypeName,jiancedianName,jianceType,jianceTime,jianceProject,zhixingBiaozhun,jianceValue,danwei,biaozhunXianzhi,shifouDabiao,shifouTingchan,beizhu)" \
                  " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                  % (title,EntTypeName,jiancedianName,jianceType,jianceTime,jianceProject,zhixingBiaozhun,jianceValue,danwei,biaozhunXianzhi,shifouDabiao,shifouTingchan,beizhu) + "ON DUPLICATE KEY UPDATE title='%s'" % (title)
            dbclient.save(sql)
        except:
            continue


def start(item):
    if item['EntTypeName'] == '废水':
        category = '1'
    else:
        category = '2'

    url = item['url']
    title = item['title']
    EntTypeName = item['EntTypeName']
    startDate = item['startDate']
    endDate = item['endDate']
    totalPage = int(item['totalPage'])

    try:
        __VIEWSTATE = get_start_VIEWSTATE(url)
    except:
        return

    #获取第一页数据
    first_body = 'ctl00%24ctl00%24ScriptManager1=ctl00%24ctl00%24ScriptManager1%7Cctl00%24ctl00%24cphMain%24cphMainPage%24UCDataSearch%24btnSearch&ctl00%24ctl00%24cphMain%24cphMainPage%24UCMonitorTrend%24ddlIndicatorCategory={category}&ctl00%24ctl00%24cphMain%24cphMainPage%24UCMonitorTrend%24ddlMonitorSite=-1&ctl00%24ctl00%24cphMain%24cphMainPage%24UCMonitorTrend%24ddlPollutantName=%E7%83%9F%E5%B0%98&ctl00%24ctl00%24cphMain%24cphMainPage%24UCMonitorTrend%24ddlDataType=-1&ctl00%24ctl00%24cphMain%24cphMainPage%24UCMonitorTrend%24txtStartTime=2019-03-01&ctl00%24ctl00%24cphMain%24cphMainPage%24UCMonitorTrend%24txtEndTime=2019-03-03&ctl00%24ctl00%24cphMain%24cphMainPage%24UCDataSearch%24ddlIndicatorCategory={category}&ctl00%24ctl00%24cphMain%24cphMainPage%24UCDataSearch%24ddlMonitorSite=-1&ctl00%24ctl00%24cphMain%24cphMainPage%24UCDataSearch%24ddlPollutantName=-1&ctl00%24ctl00%24cphMain%24cphMainPage%24UCDataSearch%24ddlDataType=-1&ctl00%24ctl00%24cphMain%24cphMainPage%24UCDataSearch%24txtStartTime={startDate}&ctl00%24ctl00%24cphMain%24cphMainPage%24UCDataSearch%24txtEndTime={endDate}&__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE={__VIEWSTATE}&__VIEWSTATEGENERATOR=0C628C24&__ASYNCPOST=true&ctl00%24ctl00%24cphMain%24cphMainPage%24UCDataSearch%24btnSearch=%E6%9F%A5%20%E8%AF%A2'
    first_data = first_body.format(category=category, startDate=startDate, endDate=endDate, __VIEWSTATE=__VIEWSTATE)
    # print(first_data)
    response = requests.post(url,data=first_data,headers=post_headers,timeout=20)
    # print(response.text)

    #获取__VIEWSTATE,nextId
    __VIEWSTATE, nextId = get_nextId_VIEWSTATE(response)
    #处理数据
    deal(response,title,EntTypeName)



    #获取剩余页数
    for i in range(totalPage):
        try:
            print('当前页：'+str(i))
            body = 'ctl00%24ctl00%24ScriptManager1=ctl00%24ctl00%24cphMain%24cphMainPage%24UCDataSearch%24UpdatePanel1%7C{nextId}&ctl00%24ctl00%24cphMain%24cphMainPage%24UCMonitorTrend%24ddlIndicatorCategory={category}&ctl00%24ctl00%24cphMain%24cphMainPage%24UCMonitorTrend%24ddlMonitorSite=-1&ctl00%24ctl00%24cphMain%24cphMainPage%24UCMonitorTrend%24ddlPollutantName=%E7%83%9F%E5%B0%98&ctl00%24ctl00%24cphMain%24cphMainPage%24UCMonitorTrend%24ddlDataType=-1&ctl00%24ctl00%24cphMain%24cphMainPage%24UCMonitorTrend%24txtStartTime=2019-03-01&ctl00%24ctl00%24cphMain%24cphMainPage%24UCMonitorTrend%24txtEndTime=2019-03-02&ctl00%24ctl00%24cphMain%24cphMainPage%24UCDataSearch%24ddlIndicatorCategory={category}&ctl00%24ctl00%24cphMain%24cphMainPage%24UCDataSearch%24ddlMonitorSite=-1&ctl00%24ctl00%24cphMain%24cphMainPage%24UCDataSearch%24ddlPollutantName=-1&ctl00%24ctl00%24cphMain%24cphMainPage%24UCDataSearch%24ddlDataType=-1&ctl00%24ctl00%24cphMain%24cphMainPage%24UCDataSearch%24txtStartTime={startDate}&ctl00%24ctl00%24cphMain%24cphMainPage%24UCDataSearch%24txtEndTime={endDate}&__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE={__VIEWSTATE}&__VIEWSTATEGENERATOR=0C628C24&__ASYNCPOST=true&ctl00%24ctl00%24cphMain%24cphMainPage%24UCDataSearch%24gvHistoryData%24ctl23%24lbnNext.x=5&ctl00%24ctl00%24cphMain%24cphMainPage%24UCDataSearch%24gvHistoryData%24ctl23%24lbnNext.y=2'
            data = body.format(nextId=nextId,category=category, startDate=startDate, endDate=endDate, __VIEWSTATE=__VIEWSTATE)
            response = requests.post(url, data=data, headers=post_headers,timeout=20)
            # print(response.text)
            __VIEWSTATE, nextId = get_nextId_VIEWSTATE(response)
            deal(response,title,EntTypeName)
        except:
            continue


if __name__ == '__main__':
    dbclient = db.MysqlClient()
    item_list = []
    with open('heilongjiang_id.txt') as f:
        results = f.readlines()
        for res in results:
            url = res.split(',')[0]
            title = res.split(',')[1].strip()
            startDate = res.split(',')[2].strip()
            endDate = res.split(',')[3].strip()
            totalPage = res.split(',')[4].strip()
            EntTypeName = res.split(',')[5].strip()
            obj = {
                'url': url,
                'title': title,
                'startDate': startDate,
                'endDate': endDate,
                'totalPage': totalPage,
                'EntTypeName': EntTypeName,
            }
            item_list.append(obj)
    for item in item_list:
        print(item)
        try:
            start(item)
        except:
            continue