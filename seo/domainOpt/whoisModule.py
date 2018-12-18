#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     whoisModule
   Description :
   Author :        hayden_huang
   Date：          2018/12/17 18:43
-------------------------------------------------
"""

import download
import re
import whois
import json

class WhoisClass():
    def __init__(self):
        self.whois_list = [{'function':'builtIn()'},{'function':'panda()'}]
        self.domain_obj = None
        self.down = download.Download()

    def builtIn(self):
        try:
            res = whois.whois(self.domain_obj['url'])
            if res:
                print('已注册')
                return True
            else:
                print('未知错误')
                return False
        except:
            print('未注册')
            return False

    def panda(self):
        url = 'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain={domain}'
        start_url = url.format(domain=self.domain_obj['domain'],timeout=15)
        response = self.down.get_html(start_url)
        if response:
            search_res = re.search('<original>(.*?)</original>', response.text)
            if search_res:
                if 'Domain name is available' in search_res.group(1):
                    # 未注册
                    print('未注册')
                    self.write_unregiste()
                    # self.query_pr(domain_obj)
                elif 'In use' in search_res.group(1) or 'Invalid Domain Name' in search_res.group(1) or 'Domain name is not available' in search_res.group(1):
                    # 已注册
                    print('已注册')
                    self.write_registe()
                    # self.write_registed(domain_obj)
                else:
                    print('未知错误')
                    self.write_error()
            else:
                print('未知错误')
                self.write_error()
        else:
            print('网络请求错误')
            self.write_error()

    def write_unregiste(self):
        with open('未注册.txt','a') as f:
            f.write(self.domain_obj['url']+'\n')

    def write_registe(self):
        with open('已注册.txt','a') as f:
            f.write(self.domain_obj['url']+'\n')

    def write_error(self):
        with open('未知错误.txt', 'a') as f:
            f.write(self.domain_obj['url']+'\n')
