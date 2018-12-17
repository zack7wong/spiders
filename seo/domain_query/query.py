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
import json
from lxml.etree import HTML

class Query(object):
    def __init__(self):
        self.urls = []
        self.download = download.Download()
        #初始化两个文件
        with open('success.csv', 'w') as f:
            write_res = 'domain,Ahrefs_Rank,DR,Backlinks,Referring_domains'+'\n'
            f.write(write_res)
        with open('failed.csv', 'w') as f:
            write_res = 'domain'+'\n'
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
        # really_domain = re.match('([a-zA-Z1-9]+.).*?$',domain_obj['url']).group(1)
        # really_domain = domain_obj['url'].replace(really_domain,'')
        start_url = config.START_URL.format(url=domain_obj['url'])
        print(start_url)
        response = self.download.get_html(start_url)
        if response:
            search_res = re.search('var CSHash = "(.*?)";', response.text)
            if search_res:
                CSHash = search_res.group(1)
                print(CSHash)
                ahrefs = self.get_ahrefs(CSHash)
                dr = self.get_dr(CSHash)
                Backlinks = self.get_Backlinks(CSHash)
                Referring = self.get_Referring(CSHash)
                obj = {
                    'url':domain_obj['url'],
                    'ahrefs':ahrefs,
                    'dr':dr,
                    'Backlinks':Backlinks,
                    'Referring':Referring,
                }
                print(obj)
                self.write_success(obj)
                return None

        print('未知错误...')
        self.write_failed(domain_obj)

    def get_ahrefs(self,CSHash):
        url = 'https://ahrefs.com/site-explorer/ajax/overview/domain-rank-history-table/{CSHash}'.format(CSHash=CSHash)
        headers = config.XMLHttpRequest_HEADERS
        response = self.download.get_html(url,headers=headers)
        json_obj = json.loads(response.text)
        ahrefs = str(json_obj['Today']['value'])
        return ahrefs

    def get_dr(self,CSHash):
        url = 'https://ahrefs.com/site-explorer/ajax/overview/domain-rating/{CSHash}'.format(CSHash=CSHash)
        headers = config.XMLHttpRequest_HEADERS
        response = self.download.get_html(url,headers=headers)
        json_obj = json.loads(response.text)
        dr = str(json_obj['domain_rating'])
        return dr

    def get_Backlinks(self,CSHash):
        url = 'https://ahrefs.com/site-explorer/ajax/overview/backlinks-stats/{CSHash}'.format(CSHash=CSHash)
        headers = config.XMLHttpRequest_HEADERS
        response = self.download.get_html(url,headers=headers)
        json_obj = json.loads(response.text)
        Backlinks = str(json_obj['total_backlinks_formated'])
        return Backlinks

    def get_Referring(self,CSHash):
        url = 'https://ahrefs.com/site-explorer/ajax/overview/referring-domains-stats/{CSHash}'.format(CSHash=CSHash)
        headers = config.XMLHttpRequest_HEADERS
        response = self.download.get_html(url,headers=headers)
        json_obj = json.loads(response.text)
        Referring = str(json_obj['total_referring_domains_formated'])
        return Referring

    def write_failed(self,domain_obj):
        with open('failed.csv', 'a') as f:
            f.write(str(domain_obj['url'])+'\n')

    def write_success(self,results):
        with open('success.csv', 'a') as f:
            write_res = results['url']+','+results['ahrefs']+','+results['dr']+','+results['Backlinks']+','+results['Backlinks']+'\n'
            f.write(write_res)
