#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     query
   Description :
   Author :        hayden_huang
   Date：          2018/12/17 18:32
-------------------------------------------------
"""

import config
import download
import re
from lxml.etree import HTML
import whoisModule
import random
import time

class Query():
    def __init__(self):
        self.down = download.Download()
        self.mywhois = whoisModule.WhoisClass()

    def get_random_whois(self):
        res = random.choice(self.mywhois.whois_list)
        # res['function'] = 'oneonefour()'
        return 'self.mywhois.'+res['function']

    def query_regist(self,domain_obj_list,processNum):
        for domain_obj in domain_obj_list:
            try:
                print('正在查询该链接是否注册： ' + domain_obj['url'])
                self.mywhois.domain_obj = domain_obj
                res = self.get_random_whois()
                eval(res)
                time.sleep(2)
            except:
                continue
