#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import re
import json

start_count=1
headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "no-cache,no-cache",
        'cookie': "thw=cn; cna=xgrfE6KDbDICAXUc+6O6psAE; v=0; t=d2fe07687234984308182d23f28476ce; cookie2=1c4cfef2e8d2925a45312d4fc5ced6c5; _tb_token_=337e66e353ebe; _mw_us_time_=1545815949838; unb=813112913; sg=430; _l_g_=Ug%3D%3D; skt=ee0266d41db2527b; cookie1=V360CmZnyG7cIb%2BgO%2FKjx1M631Qdt5SN2su%2BXVHO1LM%3D; csg=f674830b; uc3=vt3=F8dByRMHicSkecf0v8s%3D&id2=W8gwa8FRs9tg&nk2=F5RMGoDTrd%2FSIgJu&lg2=WqG3DMC9VAQiUQ%3D%3D; existShop=MTU0NTgxNTk1Nw%3D%3D; tracknick=tb9347787_44; lgc=tb9347787_44; _cc_=VFC%2FuZ9ajQ%3D%3D; dnk=tb9347787_44; _nk_=tb9347787_44; cookie17=W8gwa8FRs9tg; tg=0; uc1=cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&cookie21=UtASsssme%2BBq&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&existShop=false&pas=0&cookie14=UoTYM86GLRiQ%2Fg%3D%3D&tag=8&lng=zh_CN; mt=ci=5_1; l=aBeaOTn0ysWIEtQBBMaO5S-kU95ZZL5PseMY1Ma6fTDg6640T05Nry-o-VwR7_hC5TGy_K-5F; isg=BMHBOXuLeTOIjZUH1Engx9Dv0A0AC1b1EWGprCMW5UgnCuHcajyJsE0A6D7pAs0Y",
    'pragma': "no-cache",
    'referer': "https://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA&type=p&tmhkh5=&spm=a21wu.10013406.a2227oh.d100&from=sea_1_searchbutton&catId=100",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'Postman-Token': "aec1f324-02ce-4443-bc50-6728bc47e93e"
    }



for i in range(0,5):
    url = 'https://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA&type=p&tmhkh5=&spm=a21wu.10013406.a2227oh.d100&from=sea_1_searchbutton&catId=100&p4ppushleft=5%2C48&s={page}'
    start_url = url.format(page=i*50)
    response = requests.get(url=start_url,headers=headers)
    # print(response.text)
    search_res = re.search('g_page_config = (.*?)true}};',response.text)
    # print(search_res.group(1))
    thisres = search_res.group(1)+'true}}'
    json_obj = json.loads(thisres)
    for data in json_obj['mods']['grid']['data']['spus']:
        title = data['title']
        importantKey = data['importantKey'].replace('"','')
        price = data['price']
        month_sales = data['month_sales']
        seller = data['seller']['num']
        end = str(start_count)+','+title+','+importantKey+','+price+','+month_sales+','+seller+'\n'
        print(end)
        with open('结果.csv','a') as ff:
            ff.write(end)
        start_count+=1