#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     baidu
   Description :
   Author :        hayden_huang
   Date：          2018/11/21 12:15
-------------------------------------------------
"""

import re
import download
from lxml.etree import HTML
from lxml import etree
import config

class Baidu():
    def __init__(self):
        self.down = download.Download()
        self.result = []

    def web_search(self,kw_list,url_obj):
        for kw in kw_list:
            flag = False
            print('当前关键词：'+kw+'  搜索模式：百度')
            for i in range(0,10):
                pageToken = str(i*10)
                print('当前页数：'+str(i+1))
                url = 'https://www.baidu.com/s?wd={kw}&pn={pageToken}'.format(kw=kw,pageToken=pageToken)
                response = self.down.get_html(url)
                #先判断在不在当前页面
                search_res = re.search(url_obj['url']+'|'+url_obj['domain'], response.text)
                if search_res:
                    print('已找到')
                    html = HTML(response.text)
                    results = html.xpath('//div[@id="content_left"]/div[@class="result c-container "]')
                    for res in results:
                        detail_html_text = etree.tostring(res)
                        detail_search_res = re.search(url_obj['url']+'|'+url_obj['domain'], detail_html_text.decode().replace('</b>','').replace('<b>',''))
                        if detail_search_res:
                            rank = re.search('<div class="result c-container " id="(\d+)"', detail_html_text.decode(),re.S).group(1)
                            rank = rank[-1]
                            if rank == '0':
                                rank = '10'
                            print('当前页排名：'+rank)
                            obj = {
                                'keyword':kw,
                                'pageNum':str(i+1),
                                'rank':rank,
                                'type':'web_baidu'
                            }
                            config.RESULTS.append(obj)
                            flag = True
                            break
                else:
                    print('第'+str(i+1)+'页未找到')

                if flag:
                    break

    def m_search(self,kw_list,url_obj):
        for kw in kw_list:
            flag = False
            print('当前关键词：' + kw +'  搜索模式：百度移动')
            for i in range(0, 10):
                pageToken = str(i * 10)
                print('当前页数：' + str(i+1))
                url = 'https://m.baidu.com/s?pn={pageToken}&word={kw}'.format(kw=kw, pageToken=pageToken)
                response = self.down.get_html(url)
                # 先判断在不在当前页面
                search_res = re.search(url_obj['url'] + '|' + url_obj['domain'], response.text)
                if search_res:
                    print('已找到')
                    html = HTML(response.text)
                    results = html.xpath('//div[@id="results"]/div[@class="c-result result"]')
                    for res in results:
                        detail_html_text = etree.tostring(res)
                        detail_search_res = re.search(url_obj['url'] + '|' + url_obj['domain'],detail_html_text.decode())
                        if detail_search_res:
                            rank = re.search('order="(\d+)"', detail_html_text.decode(),re.S).group(1)
                            rank = rank[-1]
                            if rank == '0':
                                rank = '10'
                            print('当前页排名：' + rank)
                            obj = {
                                'keyword': kw,
                                'pageNum': str(i + 1),
                                'rank': rank,
                                'type': 'm_baidu'
                            }
                            config.RESULTS.append(obj)
                            flag = True
                            break
                else:
                    print('第' + str(i + 1) + '页未找到')

                if flag:
                    break

    def save_res(self):
        for res in self.result:
            if res['type'] == 'web_baidu':
                type = '百度'
            elif res['type'] == 'm_baidu':
                type = '百度移动'

            write_res = '关键词：' + res['keyword'] + '             来源：'+ type + '              排名：第' + res['pageNum'] + '页第' + res['rank'] + '个' + '\n'
            print(write_res)
            self.write_res(write_res)

    def write_res(self,results):
        with open('results.txt','a') as f:
            f.write(results)

