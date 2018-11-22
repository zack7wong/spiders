#!/usr/bin/env python
# -*- coding:utf-8 -*-


import download
from lxml.etree import HTML
import re
import time

class getKeyword(object):
    def __init__(self):
        self.down = download.Download()
        self.kw_list = []

    def get_url(self):
        urls_list = []
        url_obj = {
            'url': 'http://www.aliwuxi.com',
            'domain': 'aliwuxi.com',
        }
        urls_list.append(url_obj)
        # try:
        #     with open('urls.txt') as f:
        #         results = f.readlines()
        #         for res in results:
        #             try:
        #                 url = res.strip()
        #                 domain = re.match('(http://[a-zA-Z1-9]+.).*?$', url).group(1)
        #                 domain = url.replace(domain, '')
        #                 url_obj = {
        #                     'url': url,
        #                     'domain': domain,
        #                 }
        #                 urls_list.append(url_obj)
        #             except:
        #                 print('该行文本格式有误')
        #                 print(res)
        #                 with open('failed_urls.txt', 'a') as ff:
        #                     ff.write(res)
        # except:
        #     print('当前目录没有url.txt文本')
        #     time.sleep(60)
        return urls_list

    def get_keyword(self,response):
        html = HTML(response.text)
        url_list = html.xpath('//a/@href')
        self.parse_keyword(response)
        exits_url = []
        for url in url_list:
            if re.match('^/.*?aspx$',url):
                two_url = 'http://www.aliwuxi.com' + url
            elif re.match('http://.*?aspx$',url):
                two_url = url
            else:
                continue

            if two_url in exits_url:
                continue
            else:
                exits_url.append(two_url)
            print(two_url)
            two_response = self.down.get_html(two_url)
            self.parse_keyword(two_response)
        self.kw_list = list(filter(None, self.kw_list))
        self.kw_list = list(set(self.kw_list))
        return self.kw_list

    def parse_keyword(self,response):
        html = HTML(response.text)
        domain_kw = html.xpath('string(//meta[@name="keywords"]/@content)').split(',')
        if len(domain_kw) < 1:
            return None
        self.kw_list = self.kw_list + domain_kw