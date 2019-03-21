#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
from urllib.parse import quote
import time
import json
from lxml.etree import HTML


import asyncio
import hashlib
import time
import json
import copy
from idataapi_transform import ProcessFactory, GetterConfig, WriterConfig


headers = {
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Length': "44",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cookie': "SINAGLOBAL=2741068042226.078.1532572562158; SSOLoginState=1552876828; _s_tentry=sifa.sina.com.cn; login_sid_t=8a5691110b2d786a383900d4fc945dee; cross_origin_proto=SSL; Apache=8242397215703.754.1553004223751; ULV=1553004223777:17:3:1:8242397215703.754.1553004223751:1551923415364; STAR-G0=40b2205a62fcefff599abe680d00fe5a; UOR=www.google.ie,www.weibo.com,login.sina.com.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFX9gU.0AvvHpkroN8y6_.s5JpX5K2hUgL.Fo-ESoB0SoMXeh.2dJLoI7L.9JLXSh2Reh2t; ALF=1584540456; SCF=AlH-htFhOOtuSJnrHnxgPfbVUuhc309qQH8-v0vpUXbA3mir2zmc0UMn6aAUmuaihtWOzQW_espY8bcbTw0dmQo.; SUB=_2A25xlIf6DeThGeNM7VYS9inIyzWIHXVS4_4yrDV8PUNbmtBeLRWkkW9NTh6TnG-yJViB0BEKlgG9J0yaNCqVvoc4; SUHB=0YhBu1xa8rX40t; un=dfit41801@163.com; webim_unReadCount=%7B%22time%22%3A1553054190940%2C%22dm_pub_total%22%3A0%2C%22chat_group_pc%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D; rank_type=6; WBStorage=201903201822|undefined",
    'Host': "chart.weibo.com",
    'Origin': "http://chart.weibo.com",
    'Pragma': "no-cache",
    'Referer': "http://chart.weibo.com/",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest",
    'cache-control': "no-cache",
}


#获取每一天的日期！！！!!!
def get_date():
    date_list = []
    year_list = [2015,2016,2017,2018,2019]
    month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    fun = lambda year, month: list(range(1, 1 + time.localtime(time.mktime((year, month + 1, 1, 0, 0, 0, 0, 0, 0)) - 86400).tm_mday))

    for year in year_list:
        for month in month_list:
            if month < 10:
                monthStr = '0'+str(month)
            else:
                monthStr = month
            date = str(year)+str(monthStr)
            day_list = fun(year, month)

            if day_list[0] < 10:
                mydaystart = '0'+str(day_list[0])
            else:
                mydaystart = str(day_list[0])

            if day_list[0] < 10:
                mydayend = '0'+str(day_list[-1])
            else:
                mydayend = str(day_list[-1])


            period = str(year)+str(monthStr)+str(mydaystart) +'-'+str(year)+str(monthStr)+str(mydayend)
            obj = {
                'date':date,
                'period':period,
            }
            date_list.append(obj)

    return date_list


async def start():
    writeList = ['时间','榜单类型','姓名','总分数','阅读人数','阅读人数得分','阅读人数排名','互动数','互动数得分','互动数排名','社会影响力','社会影响力得分','社会影响力排名','爱慕值','爱慕值得分','爱慕值排名','正能量','正能量得分','正能量排名','搜索量','搜索量得分','搜索量排名','提及量','提及量得分','提及量排名','阅读数','阅读数得分','阅读数排名']
    # with open('微博数据.csv', 'w', encoding='gbk') as f:
    #     f.write('时间,榜单类型,姓名,总分数,阅读人数,阅读人数得分,阅读人数排名,互动数,互动数得分,互动数排名,社会影响力,社会影响力得分,社会影响力排名,爱慕值,爱慕值得分,爱慕值排名,正能量,正能量得分,正能量排名,搜索量,搜索量得分,搜索量排名,提及量,提及量得分,提及量排名,阅读数,阅读数得分,阅读数排名\n')

    date_list = get_date()
    print(date_list)
    url = "http://chart.weibo.com/aj/ranklist"
    rank_type_list = ['5','3','6']
    item_list = []
    for rank_type in rank_type_list:
        for dateObj in date_list:
            date = dateObj['date']
            period = dateObj['period']
            for pageToken in range(1,5):
                # payload = "time_type={date}&rank_type={rank_type}&version=v1&_t=0"
                payload = "datatype=&page={pageToken}&pagesize=25&rank_type={rank_type}&time_type={date}&period={period}&version=v1&_t=0"
                data = payload.format(pageToken=pageToken,date=date,rank_type=rank_type,period=period)
                # data = 'date=2019%2f1%2f1&type=realTimeHotSearchList'
                print(data)
                try:
                    response = requests.request("POST", url, data=data, headers=headers,verify=False)
                    print(response.text)
                    json_obj = json.loads(response.text)
                    html = HTML(json_obj['data'])
                except:
                    print('errors..'+date+','+str(pageToken)+','+rank_type+'\n')
                    with open('errors.txt','a') as f:
                        f.write('errors..'+date+','+str(pageToken)+','+rank_type+'\n')
                    continue




                div_list = html.xpath('//div[@class="sr_ranking_type clearfix"]')
                for div in div_list:
                    if rank_type == '5':
                        bangdanType = '内地榜'
                    elif rank_type == '3':
                        bangdanType = '港澳台榜'
                    else:
                        bangdanType = '新星榜'
                    name = div.xpath('string(.//div[@class="sr_name S_func1"]/a/text())').strip()
                    zongfenshu = div.xpath('string(.//div[@class="sr_text W_f16"]/span/b/text())')


                    len_li = div.xpath('.//ul/li')

                    item = {}
                    item['时间'] = date
                    item['榜单类型'] = bangdanType
                    item['姓名'] = name
                    item['总分数'] = zongfenshu

                    for liNum in range(1,len(len_li)+1):
                        spanName = div.xpath('string(.//ul/li['+str(liNum)+']//div[@class="propor sr_fl"]/span[@class="pro_txt"]/text())').replace('：','').strip()
                        if spanName == '互动量':
                            spanName = '互动数'

                        spanNameValue = div.xpath('string(.//ul/li['+str(liNum)+']//div[@class="propor sr_fl"]/span[@class="pro_num"]/text())')
                        spanNamedefen = div.xpath('string(.//ul/li['+str(liNum)+']//div[@class="civi score sr_fl"]/span/i[@class="ci_num"]/text())')
                        spanNamepaiming = div.xpath('string(.//ul/li['+str(liNum)+']//div[@class="civi sr_fl"]/span/i[@class="ci_num"]/text())')



                        # print(spanName)
                        spanNamedefenName = spanName +'得分'
                        spanNamepaimingName = spanName +'排名'
                        item[spanName] = spanNameValue
                        item[spanNamedefenName] = spanNamedefen
                        item[spanNamepaimingName] = spanNamepaiming
                        # print(item)

                    for key in writeList:
                        if key not in item.keys():
                            item[key] = ''
                    item_list.append(item)
                    print(item)

                    # yuedurenshu = div.xpath('string(.//ul/li[1]//div[@class="propor sr_fl"]/span[@class="pro_num"]/text())')
                    #
                    # hudongshu = div.xpath('string(.//ul/li[2]//div[@class="propor sr_fl"]/span[@class="pro_num"]/text())')
                    # hudongshudefen = div.xpath('string(.//ul/li[2]//div[@class="civi score sr_fl"]/span/i[@class="ci_num"]/text())')
                    # hudongshupaiming = div.xpath('string(.//ul/li[2]//div[@class="civi sr_fl"]/span/i[@class="ci_num"]/text())')
                    #
                    # shehui = div.xpath('string(.//ul/li[3]//div[@class="propor sr_fl"]/span[@class="pro_num"]/text())')
                    # shehuidefen = div.xpath('string(.//ul/li[3]//div[@class="civi score sr_fl"]/span/i[@class="ci_num"]/text())')
                    # shehuipaiming = div.xpath('string(.//ul/li[3]//div[@class="civi sr_fl"]/span/i[@class="ci_num"]/text())')
                    #
                    # aiamu = div.xpath('string(.//ul/li[4]//div[@class="propor sr_fl"]/span[@class="pro_num"]/text())')
                    # aiamudefen = div.xpath('string(.//ul/li[4]//div[@class="civi score sr_fl"]/span/i[@class="ci_num"]/text())')
                    # aiamupaiming = div.xpath('string(.//ul/li[4]//div[@class="civi sr_fl"]/span/i[@class="ci_num"]/text())')
                    #
                    # zhengnengliang = div.xpath('string(.//ul/li[5]//div[@class="propor sr_fl"]/span[@class="pro_num"]/text())')
                    # zhengnengliangdefen = div.xpath('string(.//ul/li[5]//div[@class="civi score sr_fl"]/span/i[@class="ci_num"]/text())')
                    # zhengnengliangpaiming = div.xpath('string(.//ul/li[5]//div[@class="civi sr_fl"]/span/i[@class="ci_num"]/text())')
                    #
                    # save_res = date+','+bangdanType+','+name+','+zongfenshu+','+yuedurenshu+','+yuedurenshudefen+','+yuedurenshupaiming+','+hudongshu+','+hudongshudefen+','+hudongshupaiming+','+shehui+','+shehuidefen+','+shehuipaiming+','+aiamu+','+aiamudefen+','+aiamupaiming+','+zhengnengliang+','+zhengnengliangdefen+','+zhengnengliangpaiming+'\n'
                    # print(save_res)
                    # with open('微博数据.csv','a', encoding='gbk',errors='ignore') as f:
                    #     f.write(save_res)
                time.sleep(5)

    mongo_config = WriterConfig.WXLSXConfig('结果.xlsx',headers=writeList)
    with ProcessFactory.create_writer(mongo_config) as mongo_writer:
        mongo_writer.write(item_list)




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())