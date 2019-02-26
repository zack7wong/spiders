#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import requests
from lxml.etree import HTML
import db

# def get_date():
#     month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
#     month_list = [1, 2]
#     fun = lambda year, month: list(range(1, 1+time.localtime(time.mktime((year,month+1,1,0,0,0,0,0,0)) - 86400).tm_mday))
#
#     for month in month_list:
#         day_list = fun(2019, month)
#         for day in day_list:
#             save_res = '2019-'+str(month)+'-'+str(day)+'\n'
#             print(save_res)
#             with open('date.txt','a') as f:
#                 f.write(save_res)
#
# get_date()

headers = {
    'Connection': "keep-alive",
    'Pragma': "no-cache",
    'Cache-Control': "no-cache",
    'Origin': "http://wryfb.fjemc.org.cn",
    'Upgrade-Insecure-Requests': "1",
    'Content-Type': "application/x-www-form-urlencoded",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Referer': "http://wryfb.fjemc.org.cn/page7.aspx?id=7WQYA9KY-Q905-59AG-7NMW-7SAXZILEE3WL&lawcode=75739058-1",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'cache-control': "no-cache",
}

def start():
    date_list = []
    with open('date.txt') as f:
        results = f.readlines()
        for res in results:
            date_list.append(res.strip())
    # print(date_list)

    item_list = []
    with open('fujian_id3.txt') as f:
        results = f.readlines()
        for res in results:
            url = res.split(',')[0]
            title = res.split(',')[1].strip()
            obj = {
                'url':url,
                'title':title,
            }
            item_list.append(obj)

    print(len(item_list))
    print(item_list[:10])

    for item in item_list:
        print(item)
        try:
            for date in date_list:
                print('当前日期:'+date)
                start_url = item['url']
                title = item['title']
                body = '__VIEWSTATE=%2FwEPDwUJNDk2MTM2Mzc5ZGTd37nDAAZ8HMoQ9C6MjYnecXynQQ%3D%3D&__EVENTVALIDATION=%2FwEWAwKKm%2FSpBwKnpoOOCwKY7%2B%2FtCc29g5gXa%2BvZaoWCWvhGPER39rFI&right%24l_date={date}&right%24Button1=%CB%D1%CB%F7'
                data = body.format(date=date)
                try:
                    response = requests.post(start_url, data=data, headers=headers,timeout=10)
                except:
                    continue
                # print(response.text)

                html =HTML(response.text)
                tr_list = html.xpath('//form[@id="aspnetForm"]//div[@class="table3"]//tr')
                if len(tr_list) == 1:
                    print('无数据')
                for item in tr_list[1:]:
                    try:
                        td_list = item.xpath('./td')
                        if len(td_list) == 8:
                            jiancedianName = item.xpath('string(./td[1])')
                            jianceTime = item.xpath('string(./td[2])')
                            jianceProject = item.xpath('string(./td[3])')
                            jianceValue = item.xpath('string(./td[4])')
                            biaozhunValue = item.xpath('string(./td[5])')
                            shifoudabiao = item.xpath('string(./td[6])')
                            chaobiaobenshu = item.xpath('string(./td[7])')
                            shifoutingchan = item.xpath('string(./td[8])')
                        elif len(td_list) == 6:
                            jianceProject = item.xpath('string(./td[1])')
                            jianceValue = item.xpath('string(./td[2])')
                            biaozhunValue = item.xpath('string(./td[3])')
                            shifoudabiao = item.xpath('string(./td[4])')
                            chaobiaobenshu = item.xpath('string(./td[5])')
                            shifoutingchan = item.xpath('string(./td[6])')

                        # 企业名称、污染源类型（废水、废气）、监测点名称、监测时间、监测项目、监测值、标准值、是否达标、超标倍数、是否停产
                        print(title,jiancedianName,jianceTime,jianceProject,jianceValue,biaozhunValue,shifoudabiao,chaobiaobenshu,shifoutingchan)

                        sql = "insert into fujian(title,jiancedianName,jianceTime,jianceProject,jianceValue,biaozhunValue,shifoudabiao,chaobiaobenshu,shifoutingchan)" \
                              " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                              % (title,jiancedianName,jianceTime,jianceProject,jianceValue,biaozhunValue,shifoudabiao,chaobiaobenshu,shifoutingchan)
                        dbclient.save(sql)
                    except:
                        continue
        except:
            continue


if __name__ == '__main__':
    dbclient = db.MysqlClient()
    start()
