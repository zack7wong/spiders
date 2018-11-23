#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     sogou
   Description :
   Author :        hayden_huang
   Date：          2018/11/22 16:48
-------------------------------------------------
"""


import re
import download
import config
from lxml.etree import HTML
from lxml import etree
import time

class Sogou():
    def __init__(self):
        self.down = download.Download()
        self.result = []

    def web_search(self,kw_list,url_obj):
        headers = {
            'Cookie':'SUV=1522740796080229; SMYUV=1522740796081448; SUID=12C710B7572B8B0A5AC449150002FF06; CXID=96B7F31133531AC7F5BFB5EBA3EFDB1D; pgv_pvi=606208; sw_uuid=8342716051; ssuid=6295371917; dt_ssuid=8529746536; start_time=1540134704266; pex=C864C03270DED3DD8A06887A372DA219231FFAC25A9D64AE09E82AED12E416AC; ad=$yllllllll2bf01JlllllVs$5y6lllllWv2XEZllll9lllllRqxlw@@@@@@@@@@@; ABTEST=0|1542102394|v17; browerV=3; osV=2; SNUID=3ACC84D1A7A2D39B4C44E561A8E15247; IPLOC=CN4403; usid=A-H-ZKVNxDTnQ3IX; gpsloc=%E5%B9%BF%E4%B8%9C%E7%9C%81%09%E6%B7%B1%E5%9C%B3%E5%B8%82; wuid=AAE8ZE3xIwAAAAqRGxZtzgoA1wA=; FREQUENCY=1542876882470_8; sct=83; sst0=613; ld=gZllllllll2bfILnlllllVsLNetlllllWv260ZlllxklllllVklll5@@@@@@@@@@; LSTMV=711%2C336; LCLKINT=3469'
        }
        for kw in kw_list:
            flag = False
            print('当前关键词：'+kw+'  搜索模式：搜狗')
            for i in range(1,11):
                pageToken = str(i)
                print('当前页数：'+str(i))
                url = 'https://www.sogou.com/web?query={kw}&page={pageToken}&ie=utf8'.format(kw=kw,pageToken=pageToken)
                response = self.down.get_html(url,headers=headers)
                #先判断在不在当前页面
                search_res = re.search(url_obj['url']+'|'+url_obj['domain'], response.text)
                if search_res:
                    print('已找到')
                    html = HTML(response.text)
                    results = html.xpath('//div[@class="results"]/div')
                    rank_list = []
                    for i in range(len(results)):
                        rank_list.append(i + 1)
                    for res,rank in zip(results,rank_list):
                        detail_html_text = etree.tostring(res)
                        detail_search_res = re.search(url_obj['url']+'|'+url_obj['domain'], detail_html_text.decode())
                        if detail_search_res:
                            rank = str(rank)
                            print('当前页排名：'+rank)
                            obj = {
                                'keyword':kw,
                                'pageNum':pageToken,
                                'rank':rank,
                                'type':'web_sogou'
                            }
                            config.RESULTS.append(obj)
                            flag = True
                            break
                else:
                    print('第'+str(i)+'页未找到')
                time.sleep(1)
                if flag:
                    break

    def m_search(self,kw_list,url_obj):
        for kw in kw_list:
            flag = False
            print('当前关键词：'+kw+'  搜索模式：搜狗移动')
            for i in range(1,11):
                pageToken = str(i)
                print('当前页数：'+str(i))
                if i == 1:
                    url = 'https://m.sogou.com/web/searchList.jsp?keyword={kw}&wm=3206'.format(kw=kw)
                else:
                    url = 'https://m.sogou.com/web/search/ajax_query.jsp?type=1&keyword={kw}&p={pageToken}'.format(kw=kw,pageToken=pageToken)
                response = self.down.get_html(url)
                #先判断在不在当前页面
                search_res = re.search(url_obj['url']+'|'+url_obj['domain'], response.text)
                if search_res:
                    print('已找到')
                    html = HTML(response.text)
                    results = html.xpath('//div[@class="vrResult"]|//div[@class="result"]')
                    rank_list = []
                    for i in range(len(results)):
                        rank_list.append(i + 1)
                    for res,rank in zip(results,rank_list):
                        detail_html_text = etree.tostring(res)
                        detail_search_res = re.search(url_obj['url']+'|'+url_obj['domain'], detail_html_text.decode())
                        if detail_search_res:
                            rank = str(rank)
                            print('当前页排名：'+rank)
                            obj = {
                                'keyword':kw,
                                'pageNum':pageToken,
                                'rank':rank,
                                'type':'m_sogou'
                            }
                            config.RESULTS.append(obj)
                            flag = True
                            break
                else:
                    print('第'+str(i)+'页未找到')

                if flag:
                    break

    def save_res(self):
        for res in self.result:
            if res['type'] == 'web_sogou':
                type = '搜狗'
            elif res['type'] == 'm_sogou':
                type = '搜狗移动'

            write_res = '关键词：' + res['keyword'] + '             来源：'+ type + '              排名：第' + res['pageNum'] + '页第' + res['rank'] + '个' + '\n'
            print(write_res)
            self.write_res(write_res)

    def write_res(self,results):
        with open('results.txt','a') as f:
            f.write(results)

