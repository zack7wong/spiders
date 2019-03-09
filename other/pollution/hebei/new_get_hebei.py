#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
from lxml.etree import HTML
import re
from urllib.parse import quote
import db
import time

get_headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Host': "121.28.49.84:8003",
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
    # 'Content-Length': "173324",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Host': "121.28.49.84:8003",
    'Origin': "http://121.28.49.84:8003",
    'Pragma': "no-cache",
    'Referer': "http://121.28.49.84:8003/",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    'X-MicrosoftAjax': "Delta=true",
    'X-Requested-With': "XMLHttpRequest",
    'cache-control': "no-cache",
}

def get_canInfo():
    url = 'http://121.28.49.84:8003/'
    response = requests.get(url, headers=get_headers, timeout=15)
    # print(response.text)


    __VIEWSTATE = re.search('id="__VIEWSTATE" value="(.*?)"',response.text).group(1)
    __VIEWSTATE = quote(__VIEWSTATE).replace('/','%2F')

    __EVENTVALIDATION = re.search('id="__EVENTVALIDATION" value="(.*?)"',response.text).group(1)
    __EVENTVALIDATION = quote(__EVENTVALIDATION).replace('/','%2F')

    tvsite_ExpandState = re.search('id="tvsite_ExpandState" value="(.*?)"', response.text).group(1)
    tvsite_ExpandState = quote(tvsite_ExpandState).replace('/', '%2F')

    # print(__VIEWSTATE)
    # print(__EVENTVALIDATION)
    # print(tvsite_ExpandState)

    return __VIEWSTATE,__EVENTVALIDATION,tvsite_ExpandState

def deal(response,item,EntType):

    #获取__VIEWSTATE  __EVENTVALIDATION
    __VIEWSTATE = re.search('\|__VIEWSTATE\|(.*?)\|\d+\|hiddenField', response.text).group(1)
    __VIEWSTATE = quote(__VIEWSTATE).replace('/', '%2F')

    __EVENTVALIDATION = re.search('\|__EVENTVALIDATION\|(.*?)\|\d+\|asyncPostBackControlIDs', response.text).group(1)
    __EVENTVALIDATION = quote(__EVENTVALIDATION).replace('/', '%2F')


    if EntType == '1':
        EntTypeName = '废水'
    else:
        EntTypeName = '废气'


    title = item['title']

    # 企业名称、污染源类型（废水、废气）、监测日期、监测项目、排放口及监测点位、监测结果、单位、执行标准名称、标准限值、是否超标、超标倍数、发布时间、污染物排放方式、排放去向
    html = HTML(response.text)
    tr_list = html.xpath('//table[@id="tbdata_auto"]//tr')
    for tr in tr_list[2:]:
        jianceTime = tr.xpath('string(./td[2]/text())').strip()
        jianceProject = tr.xpath('string(./td[3]/text())').strip()
        jiancedianName = tr.xpath('string(./td[4]/text())').strip()
        jianceValue = tr.xpath('string(./td[5]/text())').strip()
        danwei = tr.xpath('string(./td[6]/text())').strip()
        zhixingBiaozhunName = tr.xpath('string(./td[7]/text())').strip()
        biaozhunXianzhi = tr.xpath('string(./td[8]/text())').strip()
        shifouChaobiao = tr.xpath('string(./td[9]/text())').strip()
        chaobiaoBeishu = tr.xpath('string(./td[10]/text())').strip()
        publishDate = tr.xpath('string(./td[11]/text())').strip()
        paifangFangshi = tr.xpath('string(./td[12]/text())').strip()
        paifangQuxiang = tr.xpath('string(./td[13]/text())').strip()

        print(title,EntTypeName,jianceTime,jianceProject,jiancedianName,jianceValue,danwei,zhixingBiaozhunName,biaozhunXianzhi,shifouChaobiao,chaobiaoBeishu,publishDate,paifangFangshi,paifangQuxiang)

        sql = "insert into hebei(title,EntTypeName,jianceTime,jianceProject,jiancedianName,jianceValue,danwei,zhixingBiaozhunName,biaozhunXianzhi,shifouChaobiao,chaobiaoBeishu,publishDate,paifangFangshi,paifangQuxiang)" \
              " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
              % (title,EntTypeName,jianceTime,jianceProject,jiancedianName,jianceValue,danwei,zhixingBiaozhunName,biaozhunXianzhi,shifouChaobiao,chaobiaoBeishu,publishDate,paifangFangshi,paifangQuxiang) + "ON DUPLICATE KEY UPDATE title='%s'" % (title)
        dbclient.save(sql)



    return __VIEWSTATE,__EVENTVALIDATION


def start(item,fileName):
    tvsite_SelectedNode = item['id']
    title = item['title']
    __EVENTARGUMENT = item['__EVENTARGUMENT']

    for cityObj in city_list:
        if cityObj['cityName'] == fileName:
            shiqu__EVENTARGUMENT = cityObj['cityId']

    EntTypeName_list = ['1','2']
    dateList = [{'startDate': '2014-01-01', 'endDate': '2014-01-31'}, {'startDate': '2014-02-01', 'endDate': '2014-02-28'}, {'startDate': '2014-03-01', 'endDate': '2014-03-31'}, {'startDate': '2014-04-01', 'endDate': '2014-04-30'}, {'startDate': '2014-05-01', 'endDate': '2014-05-31'}, {'startDate': '2014-06-01', 'endDate': '2014-06-30'}, {'startDate': '2014-07-01', 'endDate': '2014-07-31'}, {'startDate': '2014-08-01', 'endDate': '2014-08-31'}, {'startDate': '2014-09-01', 'endDate': '2014-09-30'}, {'startDate': '2014-10-01', 'endDate': '2014-10-31'}, {'startDate': '2014-11-01', 'endDate': '2014-11-30'}, {'startDate': '2014-12-01', 'endDate': '2014-12-31'}, {'startDate': '2015-01-01', 'endDate': '2015-01-31'}, {'startDate': '2015-02-01', 'endDate': '2015-02-28'}, {'startDate': '2015-03-01', 'endDate': '2015-03-31'}, {'startDate': '2015-04-01', 'endDate': '2015-04-30'}, {'startDate': '2015-05-01', 'endDate': '2015-05-31'}, {'startDate': '2015-06-01', 'endDate': '2015-06-30'}, {'startDate': '2015-07-01', 'endDate': '2015-07-31'}, {'startDate': '2015-08-01', 'endDate': '2015-08-31'}, {'startDate': '2015-09-01', 'endDate': '2015-09-30'}, {'startDate': '2015-10-01', 'endDate': '2015-10-31'}, {'startDate': '2015-11-01', 'endDate': '2015-11-30'}, {'startDate': '2015-12-01', 'endDate': '2015-12-31'}, {'startDate': '2016-01-01', 'endDate': '2016-01-31'}, {'startDate': '2016-02-01', 'endDate': '2016-02-28'}, {'startDate': '2016-03-01', 'endDate': '2016-03-31'}, {'startDate': '2016-04-01', 'endDate': '2016-04-30'}, {'startDate': '2016-05-01', 'endDate': '2016-05-31'}, {'startDate': '2016-06-01', 'endDate': '2016-06-30'}, {'startDate': '2016-07-01', 'endDate': '2016-07-31'}, {'startDate': '2016-08-01', 'endDate': '2016-08-31'}, {'startDate': '2016-09-01', 'endDate': '2016-09-30'}, {'startDate': '2016-10-01', 'endDate': '2016-10-31'}, {'startDate': '2016-11-01', 'endDate': '2016-11-30'}, {'startDate': '2016-12-01', 'endDate': '2016-12-31'}, {'startDate': '2017-01-01', 'endDate': '2017-01-31'}, {'startDate': '2017-02-01', 'endDate': '2017-02-28'}, {'startDate': '2017-03-01', 'endDate': '2017-03-31'}, {'startDate': '2017-04-01', 'endDate': '2017-04-30'}, {'startDate': '2017-05-01', 'endDate': '2017-05-31'}, {'startDate': '2017-06-01', 'endDate': '2017-06-30'}, {'startDate': '2017-07-01', 'endDate': '2017-07-31'}, {'startDate': '2017-08-01', 'endDate': '2017-08-31'}, {'startDate': '2017-09-01', 'endDate': '2017-09-30'}, {'startDate': '2017-10-01', 'endDate': '2017-10-31'}, {'startDate': '2017-11-01', 'endDate': '2017-11-30'}, {'startDate': '2017-12-01', 'endDate': '2017-12-31'}, {'startDate': '2018-01-01', 'endDate': '2018-01-31'}, {'startDate': '2018-02-01', 'endDate': '2018-02-28'}, {'startDate': '2018-03-01', 'endDate': '2018-03-31'}, {'startDate': '2018-04-01', 'endDate': '2018-04-30'}, {'startDate': '2018-05-01', 'endDate': '2018-05-31'}, {'startDate': '2018-06-01', 'endDate': '2018-06-30'}, {'startDate': '2018-07-01', 'endDate': '2018-07-31'}, {'startDate': '2018-08-01', 'endDate': '2018-08-31'}, {'startDate': '2018-09-01', 'endDate': '2018-09-30'}, {'startDate': '2018-10-01', 'endDate': '2018-10-31'}, {'startDate': '2018-11-01', 'endDate': '2018-11-30'}, {'startDate': '2018-12-01', 'endDate': '2018-12-31'}, {'startDate': '2019-01-01', 'endDate': '2019-01-31'}, {'startDate': '2019-02-01', 'endDate': '2019-02-28'}]

    for EntType in EntTypeName_list:
        try:
            print('当前废水废气类型：'+str(EntType))

            #获取首页参数
            __VIEWSTATE,__EVENTVALIDATION, tvsite_ExpandState = get_canInfo()

            #获取市区参数
            shiqu_body = 'ScriptManager1=UpdatePanel1%7Ctvsite&ddl_year=2018&txt_EnpName=%E8%AF%B7%E8%BE%93%E5%85%A5%E4%BC%81%E4%B8%9A%E5%90%8D%E7%A7%B0&rd_DataType=1&txtStartDate_autoData=2018-10-01&txtEndDate_autoData=2018-10-31&Asp_AutoData_input=2&rd_SiteType=2&txtStartDate_handData=2019-03-01&txtEndDate_handData=2019-03-31&Asp_HandData_input=1&txtStartDate_NoiseData=2019&txtStartDate_otherData=2019-03-01&txtEndDate_otherData=2019-03-31&txt_reason=2019-01-01&txt_reason_end=2019-12-31&txt_monplan=2019&txtyearreport=2019&ddl_city=&txt_monplan_sum=2019&__EVENTTARGET=tvsite&__EVENTARGUMENT={shiqu__EVENTARGUMENT}&__LASTFOCUS=&__VIEWSTATE={__VIEWSTATE}&__EVENTVALIDATION={__EVENTVALIDATION}&tvsite_ExpandState={tvsite_ExpandState}&tvsite_PopulateLog=&__ASYNCPOST=true&'
            shiqu_data = shiqu_body.format(shiqu__EVENTARGUMENT=shiqu__EVENTARGUMENT, tvsite_ExpandState=tvsite_ExpandState, __VIEWSTATE=__VIEWSTATE, __EVENTVALIDATION=__EVENTVALIDATION)
            response = requests.post('http://121.28.49.84:8003/', data=shiqu_data, headers=post_headers, timeout=15)

            __VIEWSTATE = re.search('\|__VIEWSTATE\|(.*?)\|\d+\|hiddenField', response.text).group(1)
            __VIEWSTATE = quote(__VIEWSTATE).replace('/', '%2F')
            __EVENTVALIDATION = re.search('\|__EVENTVALIDATION\|(.*?)\|\d+\|asyncPostBackControlIDs',response.text).group(1)
            __EVENTVALIDATION = quote(__EVENTVALIDATION).replace('/', '%2F')
            tvsite_ExpandState = re.search('\|tvsite_ExpandState\|(.*?)\|\d+\|hiddenField', response.text).group(1)
            tvsite_ExpandState = quote(__VIEWSTATE).replace('/', '%2F')

            #获取列表页参数
            body = 'ScriptManager1=UpdatePanel1%7Ctvsite&__EVENTTARGET=tvsite&__EVENTARGUMENT={__EVENTARGUMENT}&__LASTFOCUS=&tvsite_ExpandState={tvsite_ExpandState}&tvsite_SelectedNode={tvsite_SelectedNode}&tvsite_PopulateLog=&__VIEWSTATE={__VIEWSTATE}&__EVENTVALIDATION={__EVENTVALIDATION}&ddl_year=2018&txt_EnpName=%E8%AF%B7%E8%BE%93%E5%85%A5%E4%BC%81%E4%B8%9A%E5%90%8D%E7%A7%B0&rd_DataType={EntType}&txtStartDate_autoData=2019-03-02&txtEndDate_autoData=2019-03-02&rd_SiteType=1&txtStartDate_handData=2019-03-01&txtEndDate_handData=2019-03-31&txtStartDate_NoiseData=2019&txtStartDate_otherData=2019-03-01&txtEndDate_otherData=2019-03-31&txt_reason=2019-01-01&txt_reason_end=2019-12-31&txt_monplan=2019&txtyearreport=2019&ddl_city=&txt_monplan_sum=2019&__ASYNCPOST=true&'
            data = body.format(__EVENTARGUMENT=__EVENTARGUMENT, tvsite_ExpandState=tvsite_ExpandState, tvsite_SelectedNode=tvsite_SelectedNode, __VIEWSTATE=__VIEWSTATE, __EVENTVALIDATION=__EVENTVALIDATION, EntType=EntType)
            # print(data)
            response = requests.post('http://121.28.49.84:8003/', data=data, headers=post_headers, timeout=15)
            # print(response.text)

            __VIEWSTATE = re.search('\|__VIEWSTATE\|(.*?)\|\d+\|hiddenField', response.text).group(1)
            __VIEWSTATE = quote(__VIEWSTATE).replace('/', '%2F')

            __EVENTVALIDATION = re.search('\|__EVENTVALIDATION\|(.*?)\|\d+\|asyncPostBackControlIDs', response.text).group(1)
            __EVENTVALIDATION = quote(__EVENTVALIDATION).replace('/', '%2F')

            #开始日期循环
            for dateObj in dateList:
                try:
                    print('当前日期：'+str(dateObj))
                    startDate = dateObj['startDate']
                    endDate = dateObj['endDate']

                    #获取第一页
                    start_url = 'http://121.28.49.84:8003/'
                    body = 'ScriptManager1=UpdatePanel2%7Cbtn_query_autodata&ddl_year=2018&txt_EnpName=%E8%AF%B7%E8%BE%93%E5%85%A5%E4%BC%81%E4%B8%9A%E5%90%8D%E7%A7%B0&rd_DataType={EntType}&txtStartDate_autoData={startDate}&txtEndDate_autoData={endDate}&Asp_AutoData_input={pageToken}&rd_SiteType=1&txtStartDate_handData=2019-03-01&txtEndDate_handData=2019-03-31&Asp_HandData_input=1&txtStartDate_NoiseData=2019&txtStartDate_otherData=2019-03-01&txtEndDate_otherData=2019-03-31&txt_reason=2019-01-01&txt_reason_end=2019-12-31&txt_monplan=2019&txtyearreport=2019&ddl_city=&txt_monplan_sum=2019&__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE={__VIEWSTATE}&__EVENTVALIDATION={__EVENTVALIDATION}&tvsite_ExpandState={tvsite_ExpandState}&tvsite_SelectedNode={tvsite_SelectedNode}&tvsite_PopulateLog=&__ASYNCPOST=true&btn_query_autodata=%E6%9F%A5%20%20%20%E8%AF%A2'
                    # body = 'ScriptManager1=UpdatePanel2%7CAsp_AutoData&ddl_year=2018&txt_EnpName=%E8%AF%B7%E8%BE%93%E5%85%A5%E4%BC%81%E4%B8%9A%E5%90%8D%E7%A7%B0&rd_DataType={EntType}&txtStartDate_autoData={startDate}&txtEndDate_autoData={endDate}&Asp_AutoData_input={pageToken}&rd_SiteType=1&txtStartDate_handData=2019-03-01&txtEndDate_handData=2019-03-31&Asp_HandData_input=1&txtStartDate_NoiseData=2019&txtStartDate_otherData=2019-03-01&txtEndDate_otherData=2019-03-31&txt_reason=2019-01-01&txt_reason_end=2019-12-31&txt_monplan=2019&txtyearreport=2019&ddl_city=&txt_monplan_sum=2019&__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE={__VIEWSTATE}&__EVENTVALIDATION={__EVENTVALIDATION}&tvsite_ExpandState={tvsite_ExpandState}&tvsite_SelectedNode={tvsite_SelectedNode}&tvsite_PopulateLog=&__ASYNCPOST=true&Asp_AutoData=go'
                    data = body.format(pageToken=1, EntType=EntType, startDate=startDate, endDate=endDate, __VIEWSTATE=__VIEWSTATE, __EVENTVALIDATION=__EVENTVALIDATION, tvsite_SelectedNode=tvsite_SelectedNode, tvsite_ExpandState=tvsite_ExpandState)
                    # print(data)
                    response = requests.post(start_url, data=data, headers=post_headers, timeout=15)
                    # print(response.text)

                    #无数据
                    if 'tbdata_auto1' in response.text:
                        print('无数据')
                        continue

                    #获取总条数
                    totalPage = re.search("共<font color='red'>(\d+)</font>页",response.text,re.S)
                    if totalPage:
                        totalPage = int(totalPage.group(1))
                        print('总页数：' + str(totalPage))
                    else:
                        print('无数据')
                        continue

                    #处理第一页
                    print('当前页：1')
                    __VIEWSTATE,__EVENTVALIDATION = deal(response,item,EntType)

                    #处理剩余页数
                    for i in range(2,totalPage+1):
                        try:
                            print('当前页：'+str(i))
                            # body = 'ScriptManager1=UpdatePanel2%7Cbtn_query_autodata&ddl_year=2018&txt_EnpName=%E8%AF%B7%E8%BE%93%E5%85%A5%E4%BC%81%E4%B8%9A%E5%90%8D%E7%A7%B0&rd_DataType={EntType}&txtStartDate_autoData={startDate}&txtEndDate_autoData={endDate}&Asp_AutoData_input={pageToken}&rd_SiteType=1&txtStartDate_handData=2019-03-01&txtEndDate_handData=2019-03-31&Asp_HandData_input=1&txtStartDate_NoiseData=2019&txtStartDate_otherData=2019-03-01&txtEndDate_otherData=2019-03-31&txt_reason=2019-01-01&txt_reason_end=2019-12-31&txt_monplan=2019&txtyearreport=2019&ddl_city=&txt_monplan_sum=2019&__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE={__VIEWSTATE}&__EVENTVALIDATION={__EVENTVALIDATION}&tvsite_ExpandState={tvsite_ExpandState}&tvsite_SelectedNode={tvsite_SelectedNode}&tvsite_PopulateLog=&__ASYNCPOST=true&btn_query_autodata=%E6%9F%A5%20%20%20%E8%AF%A2'
                            body = 'ScriptManager1=UpdatePanel2%7CAsp_AutoData&ddl_year=2018&txt_EnpName=%E8%AF%B7%E8%BE%93%E5%85%A5%E4%BC%81%E4%B8%9A%E5%90%8D%E7%A7%B0&rd_DataType={EntType}&txtStartDate_autoData={startDate}&txtEndDate_autoData={endDate}&Asp_AutoData_input={pageToken}&rd_SiteType=1&txtStartDate_handData=2019-03-01&txtEndDate_handData=2019-03-31&Asp_HandData_input=1&txtStartDate_NoiseData=2019&txtStartDate_otherData=2019-03-01&txtEndDate_otherData=2019-03-31&txt_reason=2019-01-01&txt_reason_end=2019-12-31&txt_monplan=2019&txtyearreport=2019&ddl_city=&txt_monplan_sum=2019&__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE={__VIEWSTATE}&__EVENTVALIDATION={__EVENTVALIDATION}&tvsite_ExpandState={tvsite_ExpandState}&tvsite_SelectedNode={tvsite_SelectedNode}&tvsite_PopulateLog=&__ASYNCPOST=true&Asp_AutoData=go'
                            data = body.format(pageToken=i, EntType=EntType, startDate=startDate, endDate=endDate,__VIEWSTATE=__VIEWSTATE, __EVENTVALIDATION=__EVENTVALIDATION,tvsite_SelectedNode=tvsite_SelectedNode, tvsite_ExpandState=tvsite_ExpandState)
                            # print(data)
                            response = requests.post(start_url, data=data, headers=post_headers, timeout=15)
                            # print(response.text)
                            __VIEWSTATE, __EVENTVALIDATION = deal(response, item, EntType)
                        except:
                            continue
                except:
                    continue
        except:
            continue

if __name__ == '__main__':
    city_list = [{'cityId':'s130100','cityName':'石家庄市'},{'cityId':'s130200','cityName':'唐山市'},{'cityId':'s130300','cityName':'秦皇岛市'},{'cityId':'s130400','cityName':'邯郸市'},{'cityId':'s130500','cityName':'邢台市'},{'cityId':'s130600','cityName':'保定市'},{'cityId':'s130700','cityName':'张家口市'},{'cityId':'s130800','cityName':'承德市'},{'cityId':'s130900','cityName':'沧州市'},{'cityId':'s131000','cityName':'廊坊市'},{'cityId':'s131100','cityName':'衡水市'},{'cityId':'s139100','cityName':'定州市'},{'cityId':'s130181','cityName':'辛集市'}]
    dbclient = db.MysqlClient()
    item_list = []
    fileName = '张家口市'
    with open(fileName+'.txt') as f:
        results = f.readlines()
        for res in results:
            title = res.split(',')[0]
            id = res.split(',')[1].strip()
            __EVENTARGUMENT = res.split(',')[2].strip()
            obj ={
                'id':id,
                'title':title,
                '__EVENTARGUMENT':__EVENTARGUMENT,
            }
            item_list.append(obj)
    for item in item_list: ########## 起始位置
        print(item)
        try:
            start(item,fileName)
        except:
            continue