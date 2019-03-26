#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import time
import re

def start():
    url = 'http://wx.jd120.com/HqReg-Register.action?code=023Xrq670fPK7F1153970JXj670Xrq6d&state=gh'
    response = requests.get(url)
    # print(response.text)
    html = HTML(response.text)
    urls = html.xpath('//div[@id="appointRegTabContent"]/div/ul/li/a/@href')
    titles = html.xpath('//div[@id="appointRegTabContent"]/div/ul/li/a/text()')
    # print(len(urls))
    # print(len(titles))

    item_list = []
    for url,title in zip(urls,titles):
        link = 'http://wx.jd120.com/'+url
        catName = title.strip()
        # print(link, title)
        obj = {
            'url':link,
            'catName':catName,
        }
        item_list.append(obj)




    # date_list = []
    # for i in range(10):
    #     addTime = i * 3600 * 24
    #     userTime = time.strftime('%Y-%m-%d', time.localtime(time.time() + addTime))
    #     date_list.append(userTime)
    # print(date_list)
    # for date in date_list:
    #     with open(date + '.csv', 'w', encoding='gbk') as f:
    #         pass
    #     print(date)


    allObj_list = []
    for item in item_list:
        url = item['url']
        catName = item['catName']
        print(url,catName)

        try:
            response = requests.get(url,timeout=15)
        except:
            print('请求失败')
            continue
        html = HTML(response.text)
        # print(response.text)
        td_list = html.xpath('//table[@class="table appoint-table"]//tr//td')
        for td in td_list:
            hrefValue_list = td.xpath('.//a/@href')
            # print(hrefValue_list)
            if len(hrefValue_list) >=1:
                num = 1
                for hrefValue in hrefValue_list:
                    # print(hrefValue)
                    searchRes = re.search('/HqReg-select_time.action\?workSessionId=.*?&dateId=(.*?)&.*?doctorId=(.*?)$', hrefValue)
                    if searchRes:
                        if searchRes.group(2) != '':
                            dateName = searchRes.group(1)
                            doctorName = td.xpath('string(.//a['+str(num)+']/span/text())').replace('\n','').replace('\t','').replace('\r','').strip()
                            print(dateName,doctorName)
                            obj = {
                                'dateName':dateName,
                                'doctorName':doctorName,
                                'catName':catName,
                            }
                            allObj_list.append(obj)
                    num+=1

    saveFileDate_list = []
    for obj in allObj_list:
        if obj['dateName'] not in saveFileDate_list:
            with open(obj['dateName'] + '.csv', 'w', encoding='gbk') as f:
                save_res = obj['catName']+','+obj['doctorName']+'\n'
                f.write(save_res)
            saveFileDate_list.append(obj['dateName'])
        else:
            with open(obj['dateName'] + '.csv', 'a', encoding='gbk') as f:
                save_res = obj['catName']+','+obj['doctorName']+'\n'
                f.write(save_res)




if __name__ == '__main__':
    start()