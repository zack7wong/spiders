#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import json
import time

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Cookie': 'bdshare_firstime=1544597238995; _ga=GA1.2.1468470422.1544597242; _RSG=ofqh4E8mU94PI135JaMm68; _RDG=282d1e7556706a205711ccbaf3dcebdabe; _RGUID=425ec083-84af-4a72-81b0-5a44c50c1499; GUID=09031124311689892108; _abtest_userid=50e47641-24a2-4c05-9b58-91a8cf0b24e1; ASP.NET_SessionSvc=MTAuMjguMTEyLjIxfDkwOTB8amlucWlhb3xkZWZhdWx0fDE1NDM4MjU2NDA0MjE; _gid=GA1.2.1986043836.1545832588; MKT_Pagesource=PC; appFloatCnt=4; _RF1=121.35.103.149; manualclose=1; gad_city=31f35a60e938dff697ddea628b5bea7c; _bfa=1.1544597237868.2arur4.1.1545832586324.1545898761489.6.15.228029; _bfs=1.1; MKT_OrderClick=ASID=&CT=1545898764089&CURL=http%3A%2F%2Fyou.ctrip.com%2Ftravels%2FShanghai2%2Ft2-p1.html&VAL={"pc_vid":"1544597237868.2arur4"}; _jzqco=%7C%7C%7C%7C1545832588563%7C1.1932890010.1544597241403.1545832708031.1545898764122.1545832708031.1545898764122.undefined.0.0.15.15; __zpspc=9.5.1545898764.1545898764.1%234%7C%7C%7C%7C%7C%23; _gat=1; _bfi=p1%3D290570%26p2%3D290602%26v1%3D15%26v2%3D14',
    'Host':"you.ctrip.com",
    'Pragma': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "3930ce9e-90ff-4400-b96d-82a8e209f7e2"
}
for i in range(1551,2117):
    start_url = 'http://you.ctrip.com/travels/Shanghai2/t2-p{pageToken}.html'
    print(start_url.format(pageToken=i))
    response = requests.get(start_url.format(pageToken=i),headers=headers)
    html = HTML(response.text)
    urls = html.xpath('//div[@class="journalslist cf"]/a/@href')
    print(urls)
    host = 'http://you.ctrip.com'
    for url in urls:
        link = host+url
        print(link)

        detail_response = requests.get(link,headers=headers)
        detail_html = HTML(detail_response.text)

        name = detail_html.xpath('string(//div[@class="ctd_head_right cf"]/p[@class="nickname"]|//div[@class="ctd_head_right"]/a[@class="user_img"]/@title)')
        userLink = detail_html.xpath('string(//div[@class="ctd_head_right cf"]/p[@class="nickname"]/a/@href|//div[@class="ctd_head_right"]/a[@class="user_img"]/@href)')
        publishDate = detail_html.xpath('string(//div[@class="ctd_content"]/h3|//div[@class="time"])')
        publishDate = publishDate.strip()
        Day = detail_html.xpath('string(//div[@class="ctd_content_controls cf"]//span[1])')
        thistime = detail_html.xpath('string(//div[@class="ctd_content_controls cf"]//span[2])')
        money = detail_html.xpath('string(//div[@class="ctd_content_controls cf"]//span[3])')
        peoply = detail_html.xpath('string(//div[@class="ctd_content_controls cf"]//span[4])')
        luxian = detail_html.xpath('//div[@class="author_poi"]/dl/dd/a/@title')

        if len(luxian)>0:
            print(name)
            print(publishDate)
            print(Day)
            print(thistime)
            print(money)
            print(peoply)
            print(luxian)

            userInfoUrl = 'http://you.ctrip.com'+userLink
            userResponse = requests.get(userInfoUrl)
            user_html = HTML(userResponse.text)
            userAddress = user_html.xpath('string(//div[@class="item gray"]/span[2])')
            print(userAddress)
            item_list = []
            for myaddress in luxian:
                try:
                    geoUrl = 'http://api.map.baidu.com/geocoder?address={address}&output=json&key=37492c0ee6f924cb5e934fa08c6b1676&city=上海市'
                    response1 = requests.get(geoUrl.format(address=myaddress))
                    # print(response1.text)
                    json_obj1 = json.loads(response1.text)
                    # print(response1.text)
                    geo = json_obj1['result']['location']

                    districtUrl = 'http://api.map.baidu.com/geocoder?output=json&location={lat},%20{lng}&key=37492c0ee6f924cb5e934fa08c6b1676'
                    lng = geo['lng']
                    lat = geo['lat']
                    response2 = requests.get(districtUrl.format(lat=lat,lng=lng))
                    json_obj2 = json.loads(response2.text)
                    district = json_obj2['result']['addressComponent']['district']
                    print(myaddress)
                    print(district)

                    obj = {
                        'address':myaddress,
                        'geo':geo,
                        'district':district,
                    }
                    item_list.append(obj)
                except:
                    continue
            save_res = name + ','+publishDate+','+Day+','+thistime+','+money+','+peoply+','+str(luxian).replace(',','，')+','+str(item_list).replace(',','，')+','+userAddress+'\n'
            with open('results.csv','a') as f:
                f.write(save_res)
