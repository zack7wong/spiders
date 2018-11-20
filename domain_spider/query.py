#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     query
   Description :
   Author :        hayden_huang
   Date：          2018/11/13 17:05
-------------------------------------------------
"""

import config
import download
import re
from lxml.etree import HTML

class Query(object):
    def __init__(self):
        self.urls = []
        self.download = download.Download()
        #初始化两个文件
        with open('registed.csv', 'w') as f:
            write_res = 'domain'+'\n'
            f.write(write_res)
        with open('unregister.csv', 'w') as f:
            write_res = 'domain,google_pr,sogou_pr,sogou_link'+'\n'
            f.write(write_res)
        with open('failed_domain.csv', 'w') as f:
            write_res = 'failed'+'\n'
            f.write(write_res)

    def get_url(self):
        with open('domain.txt') as f:
            results = f.readlines()
            for res in results:
                try:
                    url = res.strip()
                    url_obj = {
                        'url': url,
                    }
                    self.urls.append(url_obj)
                except:
                    print('该行文本格式有误')
                    print(res)
                    with open('failed_domain.txt','a') as ff:
                        ff.write(res)

    def query_domain(self,domain_obj):
        really_domain = re.match('([a-zA-Z1-9]+.).*?$',domain_obj['url']).group(1)
        really_domain = domain_obj['url'].replace(really_domain,'')
        start_url = config.QUERY_DOMAIN_URL.format(domain=really_domain)
        response = self.download.get_html(start_url)
        if response:
            search_res = re.search('<original>(.*?)</original>',response.text)
            if search_res:
                if 'Domain name is available' in search_res.group(1):
                    # 未注册
                    print('未注册')
                    self.query_pr(domain_obj)
                elif 'In use' in search_res.group(1) or 'Invalid Domain Name' in search_res.group(1) or 'Domain name is not available' in search_res.group(1):
                    # 已注册
                    print('已注册')
                    self.write_registed(domain_obj)
                else:
                    self.write_failed(domain_obj)
            else:
                self.write_failed(domain_obj)
        else:
            self.write_failed(domain_obj)

    def query_pr(self,domain_obj):
        start_url = config.QUERY_PR_URL.format(domain=domain_obj['url'])
        response = self.download.get_html(start_url)
        if response:
            html = HTML(response.text)
            sogou_link = '-1'
            google_pr = html.xpath('string(//div[@class="pr-content"]/a[1]/img/@alt)')
            if google_pr == '':
                google_pr = '-1'
            sogou_pr = html.xpath('string(//div[@class="pr-content"]/a[2]/img/@alt)')
            if sogou_pr == '':
                sogou_pr = '-1'

            sogou_url = config.SOGOU_URL.format(domain=domain_obj['url'])
            sogou_reponse = self.download.get_html(sogou_url,proxy=True)
            if sogou_reponse:
                sogou_html = HTML(sogou_reponse.text)
                sogou_search = sogou_html.xpath('string(//div[@class="search-info"])')
                sogou_search = re.search('搜狗已为您找到约(\d+)条相关结果',sogou_search)
                if sogou_search:
                    sogou_link = sogou_search.group(1)

            print('谷歌pr：'+google_pr+'  搜狗pr：'+sogou_pr+'  搜狗外链数：'+sogou_link)
            self.write_unregisted(domain_obj,google_pr,sogou_pr,sogou_link)

        else:
            self.write_unregisted(domain_obj, '-1', '-1', '-1')



    def write_failed(self,domain_obj):
        with open('failed_domain.csv', 'a') as f:
            f.write(str(domain_obj['url'])+'\n')

    def write_registed(self,domain_obj):
        with open('registed.csv', 'a') as f:
            write_res = domain_obj['url']+'\n'
            f.write(write_res)

    def write_unregisted(self,domain_obj,google_pr,sogou_pr,sogou_link):
        with open('unregister.csv', 'a') as f:
            write_res = domain_obj['url']+','+google_pr+','+sogou_pr+','+sogou_link+'\n'
            f.write(write_res)