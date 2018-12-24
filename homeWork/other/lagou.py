#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
from lxml.etree import HTML


url = 'http://www.lagou.com/zhaopin/Python/{page}/?filterOption={page}'
headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    # 'Cookie': "JSESSIONID=ABAAABAAADEAAFI58BAFBA9B2E2B6FFA4D55AC7A79C5982; _ga=GA1.2.927698931.1545645652; _gid=GA1.2.1086691864.1545645652; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1545645653; user_trace_token=20181224180052-cc4206c8-0762-11e9-a3dc-525400f775ce; LGSID=20181224180052-cc4208c3-0762-11e9-a3dc-525400f775ce; PRE_UTM=; PRE_HOST=www.google.com; PRE_SITE=https%3A%2F%2Fwww.google.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGUID=20181224180052-cc420aa3-0762-11e9-a3dc-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_navigation; SEARCH_ID=7cdb1227b81942ec9222f40483b96ada; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1545645688; LGRID=20181224180139-e8363deb-0762-11e9-a3dc-525400f775ce",
    'Host': "www.lagou.com",
    'Pragma': "no-cache",
    'Referer': "https://www.lagou.com/",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
}

xuhao = 1
for i in range(1,5):
    while True:
        start_url = url.format(page=i)
        response = requests.get(start_url,verify=False)
        response.encoding = 'utf8'
        html = HTML(response.text)
        titles = html.xpath('//ul[@class="item_con_list"]/li//h3/text()')
        addresss = html.xpath('//ul[@class="item_con_list"]/li//span[@class="add"]/em/text()')
        xinzis = html.xpath('//ul[@class="item_con_list"]/li//span[@class="money"]/text()')
        jingyans = html.xpath('//ul[@class="item_con_list"]/li//div[@class="p_bot"]/div[@class="li_b_l"]/text()[3]')
        xuelis = html.xpath('//ul[@class="item_con_list"]/li//div[@class="p_bot"]/div[@class="li_b_l"]/text()[3]')
        compames = html.xpath('//ul[@class="item_con_list"]/li//div[@class="company_name"]/a/text()')
        hangyes = html.xpath('//ul[@class="item_con_list"]/li//div[@class="industry"]/text()')
        rongzis = html.xpath('//ul[@class="item_con_list"]/li//div[@class="industry"]/text()')
        guimos = html.xpath('//ul[@class="item_con_list"]/li//div[@class="industry"]/text()')
        for title,address,xinzi,jingyan,xueli,compame,hangye,rongzi,guimo in zip(titles,addresss,xinzis,jingyans,xuelis,compames,hangyes,rongzis,guimos):
            jingyan = jingyan.split('/')[0].strip()
            xueli = xueli.split('/')[1].strip()
            hangye = hangye.split('/')[0].strip().replace(',','，')
            rongzi = rongzi.split('/')[1].strip()
            guimo = guimo.split('/')[2].strip()

            res = str(xuhao)+','+title+','+address+','+xinzi+','+jingyan+','+xueli+','+compame+','+hangye+','+rongzi+','+guimo+'\n'
            print(res)
            with open('results.csv','a') as f:
                f.write(res)
            xuhao+=1
        if len(titles)>0:
            break

