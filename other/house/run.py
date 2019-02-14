#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import re

numberDIC = {'one':'1','two':'2','three':'3','four':'4','five':'5','six':'6','seven':'7','eight':'8','nine':'9','zero':'0','dor':'.',}

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Length': "136",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cookie': "Hm_lvt_8db7cb1b4649ef76847e460b7e13171c=1549873241; UM_distinctid=168dba4db4c43b-01069eeb2606ed-10376654-1fa400-168dba4db4d267; JSESSIONID=E979465F5BC0706F1B759F5767B4B0F4; CNZZDATA1253675216=1932841714-1549868380-%7C1550106978; Hm_lpvt_8db7cb1b4649ef76847e460b7e13171c=1550112030",
    'Host': "hu.tmsf.com",
    'Origin': "http://hu.tmsf.com",
    'Pragma': "no-cache",
    'Referer': "http://hu.tmsf.com/newhouse/property_searchall.htm",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
}

def deal_num(mylist):
    res = ''
    for item in mylist:
        item = item.replace('number','')
        for eachkey in numberDIC.keys():
            if item == eachkey:
                res+=numberDIC[eachkey]
                break
    return res


def parse_detail(url,title,address,response):
    html = HTML(response.text)
    tr_list = html.xpath('//div[@class="onbuildshow_contant colordg ft14"]/table//tr')
    for tr in tr_list:
        loudong = tr.xpath('string(.//td[1]/a/text())')
        if loudong == '':
            continue
        fanghao = tr.xpath('string(.//td[2]/a/div/text())')
        jianzhumianji = deal_num(tr.xpath('.//td[3]/a/div/span/@class'))
        taoneimianji = deal_num(tr.xpath('.//td[4]/a/div/span/@class'))
        defanglv = deal_num(tr.xpath('.//td[5]/a/div/span/@class'))+'%'
        danjia = deal_num(tr.xpath('.//td[6]/a/div/span/@class'))
        zhuangxiujia = deal_num(tr.xpath('.//td[7]/a/div/span/@class'))
        zongjia = deal_num(tr.xpath('.//td[8]/a/div/span/@class'))
        zhuangtai = tr.xpath('string(.//td[9]/a/text())')

        save_res = url+'||'+title+'||'+address+'||'+loudong+'||'+fanghao+'||'+jianzhumianji+'||'+taoneimianji+'||'+defanglv+'||'+danjia+'||'+zhuangxiujia+'||'+zongjia+'||'+zhuangtai
        print(save_res)
        save_res = save_res.replace('\n','').replace(',','，').replace('||',',')+'\n'
        with open('新房.csv','a',encoding='gbk',errors='ignore') as f:
            f.write(save_res)

def start():
    for i in range(1,100):
        print('目录页当前页：'+str(i))
        start_url = 'http://hu.tmsf.com/newhouse/property_searchall.htm'
        body = 'keytype=1&keyword=&sid=330500&districtid=&areaid=&dealprice=&propertystate=&propertytype=&ordertype=&priceorder=&openorder=&page={pageToken}&bbs='
        mydata = body.format(pageToken=i)

        response = requests.post(start_url,headers=headers, data=mydata)
        # print(response.text)

        html = HTML(response.text)
        li_list = html.xpath('//div[@class="searchpageall"]//ul/li')
        for li in li_list:
            url = li.xpath('string(.//h3/a/@href)')
            url = 'http://hu.tmsf.com'+url.replace('info','price')
            title = li.xpath('string(.//h3/a/text())')
            print(title)
            address = li.xpath('string(.//div[@class="build_txt"]/div[2]/p[@class="build_txt03"]/text())').strip()
            print(url)

            #获取详情页第一页
            response = requests.get(url)
            html = HTML(response.text)

            # 获取总页数
            total_page = html.xpath('string(//div[@class="spagenext"]/span[1])')
            total_page = re.search('页数.*?1/(\d+).*?', total_page).group(1)
            print('总页数' + total_page)

            #处理第一页
            parse_detail(url,title,address,response)

            #处理后续页数
            for j in range(2,int(total_page)+1):
                print('每个楼盘当前页：'+str(j))
                each_page_url = url + 'isopen=&presellid=&buildingid=&area=&allprice=&housestate=&housetype=&page={pageToken}&roomid='.format(pageToken=j)
                print(each_page_url)
                each_response = requests.get(each_page_url)
                parse_detail(url, title, address, each_response)


if __name__ == '__main__':
    with open('新房.csv', 'w', encoding='gbk', errors='ignore') as f:
        f.write('链接,楼盘,地址,楼栋,房号,建筑面积,套内建筑面积,得房率,房价,装修价,总价,状态\n')
    start()