#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     so
   Description :
   Author :        hayden_huang
   Date：          2018/11/22 11:08
-------------------------------------------------
"""


import re
import download
import config
from lxml.etree import HTML
from lxml import etree

class So():
    def __init__(self):
        self.down = download.Download()
        self.result = []

    def web_search(self,kw_list,url_obj):
        for kw in kw_list:
            flag = False
            print('当前关键词：'+kw+'  搜索模式：360')
            for i in range(1,11):
                pageToken = str(i)
                print('当前页数：'+str(i))
                url = 'https://www.so.com/s?q={kw}&pn={pageToken}'.format(kw=kw,pageToken=pageToken)
                response = self.down.get_html(url)
                #先判断在不在当前页面
                search_res = re.search(url_obj['url']+'|'+url_obj['domain'], response.text)
                if search_res:
                    print('已找到')
                    html = HTML(response.text)
                    results = html.xpath('//ul[@class="result"]/li')
                    for res in results:
                        detail_html_text = etree.tostring(res)
                        detail_search_res = re.search(url_obj['url']+'|'+url_obj['domain'], detail_html_text.decode())
                        if detail_search_res:
                            rank = re.search('rel="noopener" data-res=.*?pos.*?:(\d+),.*?', detail_html_text.decode(),re.S).group(1)
                            rank = rank
                            print('当前页排名：'+rank)
                            obj = {
                                'keyword':kw,
                                'pageNum':pageToken,
                                'rank':rank,
                                'type':'web_so'
                            }
                            config.RESULTS.append(obj)
                            flag = True
                            break
                else:
                    print('第'+str(i)+'页未找到')

                if flag:
                    break

    def m_search(self,kw_list,url_obj):
        for kw in kw_list:
            flag = False
            print('当前关键词：'+kw+'  搜索模式：360移动')
            for i in range(1,11):
                pageToken = str(i)
                print('当前页数：'+str(i))
                if pageToken == '1':
                    url = 'https://m.so.com/index.php?q={kw}'.format(kw=kw)
                else:
                    url = 'https://m.so.com/nextpage?q={kw}&pn={pageToken}&ajax=1'.format(kw=kw,pageToken=pageToken)
                response = self.down.get_html(url)
                #先判断在不在当前页面
                search_res = re.search(url_obj['url']+'|'+url_obj['domain'], response.text)
                if search_res:
                    print('已找到')
                    html = HTML(response.text)
                    results = html.xpath('//div[@class=" g-card res-list og "]|//div[@class="tg-wrap"]//div[@class="g-card res-list sumext-tpl-image mso "]')
                    rank_list = []
                    for i in range(len(results)):
                        rank_list.append(i+1)
                    for res,rank in zip(results,rank_list):
                        detail_html_text = etree.tostring(res)
                        detail_search_res = re.search(url_obj['url']+'|'+url_obj['domain'], detail_html_text.decode())
                        if detail_search_res:
                            # rank = re.search('rel="noopener" data-res=.*?"pos":(\d+),.*?', detail_html_text.decode()).group(1)
                            rank = str(rank)
                            print('当前页排名：'+rank)
                            obj = {
                                'keyword':kw,
                                'pageNum':pageToken,
                                'rank':rank,
                                'type':'m_so'
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
            if res['type'] == 'web_so':
                type = '360'
            elif res['type'] == 'm_so':
                type = '360移动'

            write_res = '关键词：' + res['keyword'] + '             来源：'+ type + '              排名：第' + res['pageNum'] + '页第' + res['rank'] + '个' + '\n'
            print(write_res)
            self.write_res(write_res)

    def write_res(self,results):
        with open('results.txt','a') as f:
            f.write(results)

