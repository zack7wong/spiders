#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
from urllib.parse import quote
import time
import json
from lxml.etree import HTML

headers = {
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Length': "44",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cookie': "SINAGLOBAL=2741068042226.078.1532572562158; SSOLoginState=1552876828; _s_tentry=sifa.sina.com.cn; login_sid_t=8a5691110b2d786a383900d4fc945dee; cross_origin_proto=SSL; Apache=8242397215703.754.1553004223751; ULV=1553004223777:17:3:1:8242397215703.754.1553004223751:1551923415364; STAR-G0=40b2205a62fcefff599abe680d00fe5a; UOR=www.google.ie,www.weibo.com,login.sina.com.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFX9gU.0AvvHpkroN8y6_.s5JpX5K2hUgL.Fo-ESoB0SoMXeh.2dJLoI7L.9JLXSh2Reh2t; ALF=1584540456; SCF=AlH-htFhOOtuSJnrHnxgPfbVUuhc309qQH8-v0vpUXbA3mir2zmc0UMn6aAUmuaihtWOzQW_espY8bcbTw0dmQo.; SUB=_2A25xlIf6DeThGeNM7VYS9inIyzWIHXVS4_4yrDV8PUNbmtBeLRWkkW9NTh6TnG-yJViB0BEKlgG9J0yaNCqVvoc4; SUHB=0YhBu1xa8rX40t; un=dfit41801@163.com; webim_unReadCount=%7B%22time%22%3A1553054190940%2C%22dm_pub_total%22%3A0%2C%22chat_group_pc%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D",
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

    for year in year_list:
        for month in month_list:
            if month < 10:
                monthStr = '0'+str(month)
            else:
                monthStr = month
            save_res = str(year)+str(monthStr)
            date_list.append(save_res)

    return date_list


def start():
    with open('微博数据.csv', 'w', encoding='gbk') as f:
        f.write('时间,榜单类型,姓名,总分数,阅读人数,阅读人数得分,阅读人数排名,互动数,互动数得分,互动数排名,社会影响力,社会影响力得分,社会影响力排名,爱慕值,爱慕值得分,爱慕值排名,正能量,正能量得分,正能量排名\n')

    date_list = get_date()
    print(date_list)
    url = "http://chart.weibo.com/aj/ranklist"
    rank_type_list = ['5','3','6']
    for rank_type in rank_type_list:
        for date in date_list:
            payload = "time_type={date}&rank_type={rank_type}&version=v1&_t=0"
            data = payload.format(date=date,rank_type=rank_type)
            # data = 'date=2019%2f1%2f1&type=realTimeHotSearchList'
            print(data)

            response = requests.request("POST", url, data=data, headers=headers,verify=False)

            print(response.text)
            json_obj = json.loads(response.text)

            html = HTML(json_obj['data'])

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

                yuedurenshu = div.xpath('string(.//ul/li[1]//div[@class="propor sr_fl"]/span[@class="pro_num"]/text())')
                yuedurenshudefen = div.xpath('string(.//ul/li[1]//div[@class="civi score sr_fl"]/span/i[@class="ci_num"]/text())')
                yuedurenshupaiming = div.xpath('string(.//ul/li[1]//div[@class="civi sr_fl"]/span/i[@class="ci_num"]/text())')

                hudongshu = div.xpath('string(.//ul/li[2]//div[@class="propor sr_fl"]/span[@class="pro_num"]/text())')
                hudongshudefen = div.xpath('string(.//ul/li[2]//div[@class="civi score sr_fl"]/span/i[@class="ci_num"]/text())')
                hudongshupaiming = div.xpath('string(.//ul/li[2]//div[@class="civi sr_fl"]/span/i[@class="ci_num"]/text())')

                shehui = div.xpath('string(.//ul/li[3]//div[@class="propor sr_fl"]/span[@class="pro_num"]/text())')
                shehuidefen = div.xpath('string(.//ul/li[3]//div[@class="civi score sr_fl"]/span/i[@class="ci_num"]/text())')
                shehuipaiming = div.xpath('string(.//ul/li[3]//div[@class="civi sr_fl"]/span/i[@class="ci_num"]/text())')

                aiamu = div.xpath('string(.//ul/li[4]//div[@class="propor sr_fl"]/span[@class="pro_num"]/text())')
                aiamudefen = div.xpath('string(.//ul/li[4]//div[@class="civi score sr_fl"]/span/i[@class="ci_num"]/text())')
                aiamupaiming = div.xpath('string(.//ul/li[4]//div[@class="civi sr_fl"]/span/i[@class="ci_num"]/text())')

                zhengnengliang = div.xpath('string(.//ul/li[5]//div[@class="propor sr_fl"]/span[@class="pro_num"]/text())')
                zhengnengliangdefen = div.xpath('string(.//ul/li[5]//div[@class="civi score sr_fl"]/span/i[@class="ci_num"]/text())')
                zhengnengliangpaiming = div.xpath('string(.//ul/li[5]//div[@class="civi sr_fl"]/span/i[@class="ci_num"]/text())')

                save_res = date+','+bangdanType+','+name+','+zongfenshu+','+yuedurenshu+','+yuedurenshudefen+','+yuedurenshupaiming+','+hudongshu+','+hudongshudefen+','+hudongshupaiming+','+shehui+','+shehuidefen+','+shehuipaiming+','+aiamu+','+aiamudefen+','+aiamupaiming+','+zhengnengliang+','+zhengnengliangdefen+','+zhengnengliangpaiming+'\n'
                with open('微博数据.csv','a', encoding='gbk',errors='ignore') as f:
                    f.write(save_res)




if __name__ == '__main__':
    start()