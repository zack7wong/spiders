#!/usr/bin/env python
# -*- coding:utf-8 -*-

import download
import json
import re
import os
import config
import time
import query

if __name__ == '__main__':
    query = query.Query()
    query.get_url()
    while True:
        # try:
            type = input('请输入要查询的域名(如需批量请输入 all)：')
            if type == 'all':
                for domain in query.urls:
                    print('正在查询： '+domain['url'])
                    query.query_domain(domain)
            else:
                domain = {'url':type}
                print('正在查询： ' + domain['url'])
                query.query_domain(domain)
        # except:
        #     print('未知错误')

