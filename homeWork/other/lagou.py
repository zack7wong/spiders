#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
from lxml.etree import HTML


url = 'https://www.lagou.com/zhaopin/Python/{page}/?filterOption={page}'
headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Cookie': "JSESSIONID=ABAAABAAADEAAFI58BAFBA9B2E2B6FFA4D55AC7A79C5982; _ga=GA1.2.927698931.1545645652; _gid=GA1.2.1086691864.1545645652; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1545645653; user_trace_token=20181224180052-cc4206c8-0762-11e9-a3dc-525400f775ce; LGUID=20181224180052-cc420aa3-0762-11e9-a3dc-525400f775ce; TG-TRACK-CODE=index_navigation; _gat=1; LGSID=20181225120225-e365ac6d-07f9-11e9-ab9e-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FPython%2F4%2F%3FfilterOption%3D4; SEARCH_ID=378335c8992e428a9d24de168b6ad497; X_HTTP_TOKEN=39cd8a3f027d41414ee8ff00ccba9129; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22167e388900f18b-0398d80a420de1-10376654-2073600-167e3889010e7%22%2C%22%24device_id%22%3A%22167e388900f18b-0398d80a420de1-10376654-2073600-167e3889010e7%22%7D; sajssdk_2015_cross_new_user=1; LG_LOGIN_USER_ID=3a79651c1a6a9f2946f250974b0b7989b98e992c24792cb9; _putrc=B390D5BFB2B429DC; login=true; unick=%E9%BB%84%E8%BE%89%E7%85%8C; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=145; gate_login_token=cb011395618c43501c17125be97fb47c00920769750c1221; index_location_city=%E6%B7%B1%E5%9C%B3; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1545710658; LGRID=20181225120417-264205ec-07fa-11e9-aa33-525400f775ce",
    'Host': "www.lagou.com",
    'Pragma': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
}



import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url,headers=headers) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        xuhao = 1
        for i in range(1, 20):
            start_url = url.format(page=i)

            print(start_url)
            html_text = await fetch(session,start_url)
            html = HTML(html_text)
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

loop = asyncio.get_event_loop()
loop.run_until_complete(main())