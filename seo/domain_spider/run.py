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
    for domain in query.urls:
        print('正在查询： '+domain['url'])
        query.query_domain(domain)
