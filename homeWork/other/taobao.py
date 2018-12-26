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
    'cookie': "t=4e6b02988addbe072074e68bacc7c129; UM_distinctid=167105f181010-02879acec4c972-1e3c6655-1fa400-167105f1811161; tracknick=%5Cu75BE%5Cu98CEhhh; lgc=%5Cu75BE%5Cu98CEhhh; tg=0; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; cna=r1KFFAVLRlICAXkjZRXMAU9r; cookie2=2390873e3ca89de45591ee788deb49aa; v=0; _tb_token_=e1b55395b7e3a; _m_h5_tk=8471eae64ae9e40816ebff57516c8c0d_1545816425772; _m_h5_tk_enc=1d4a2f50b79d7516fba60c2cb5bd6400; unb=824298478; sg=h85; _l_g_=Ug%3D%3D; skt=b620e2ec5ed77934; publishItemObj=Ng%3D%3D; cookie1=UomILnOytUHyfsupy2G%2BiVMwLxL3EPZHqY6MjNWGB0U%3D; csg=e6466e8e; uc3=vt3=F8dByRMHicPxg%2B6xht4%3D&id2=W8twqJogLFsy&nk2=3yvIIgWQXQ%3D%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; existShop=MTU0NTgwODUyMQ%3D%3D; _cc_=Vq8l%2BKCLiw%3D%3D; dnk=%5Cu75BE%5Cu98CEhhh; _nk_=%5Cu75BE%5Cu98CEhhh; cookie17=W8twqJogLFsy; enc=MYV0QS412YFEj0TzgwnvBFYxay6R8ZnXI%2BYqYimjxOPDzmQSK2UVOgF%2FLzF1D5z3EsxdYret%2FScq6KUbuKfm4w%3D%3D; JSESSIONID=E251C304F7E429C7DFA7E36DE30BCCC0; uc1=cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&cookie21=UtASsssme%2BBq&cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=false&pas=0&cookie14=UoTYM86HlCvGqA%3D%3D&tag=8&lng=zh_CN; mt=ci=3_1; l=aBqx1UMiyJ8AK0QKLMaJwX5ue707gv5PsOUL1MakBiThNP3j8ziREj-o-Vw6j_qC51cy_K-5F; isg=BFBQDh9wOPAsY-MP0E76-IdiIZhisTUep05ockohHat-hfAv8iuj8sg3WQ3AVew7",
    'pragma': "no-cache",
    'referer': "https://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA&type=p&tmhkh5=&spm=a21wu.10013406.a2227oh.d100&from=sea_1_searchbutton&catId=100",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'Postman-Token': "aec1f324-02ce-4443-bc50-6728bc47e93e"
    }


for i in range(0,21):
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
        with open('结果.csv','a',encoding='utf8') as ff:
            ff.write(end)
        start_count+=1