#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     read
   Description :
   Author :        hayden_huang
   Date：          2018/12/17 18:15
-------------------------------------------------
"""

import re

class Read():
    def __init__(self):
        pass

    def read_txt(self):
        urls = []
        with open('待检测域名.txt') as f:
            results = f.readlines()
            for res in results:
                try:
                    url = res.strip()
                    domain = re.match('([a-zA-Z1-9]+.).*?$', url).group(1)
                    domain = url.replace(domain, '')
                    url_obj = {
                        'url': url,
                        'domain': domain,

                    }
                    urls.append(url_obj)
                except:
                    print('该行文本格式有误')
                    print(res)
                    with open('格式错误.txt', 'a') as ff:
                        ff.write(res)
        return urls