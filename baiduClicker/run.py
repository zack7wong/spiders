#!/usr/bin/env python
# -*- coding:utf-8 -*-

import chrome
import download
import json
import re
import os


if __name__ == '__main__':
    spider = chrome.Chrome()
    spider.get_urlobj()
    for url_obj in spider.urls:
        print(url_obj)
        for i in range(2):
            print('当前页为：'+str(i+1))
            spider.get_driver()
            keyword = url_obj['keyword']
            pageToken = str(i*10)
            start_url = 'https://www.baidu.com/s?wd={keyword}&pn={pageToken}'.format(keyword=keyword,pageToken=pageToken)
            print(start_url)
            try:
                spider.driver.get(start_url)
                spider.search(url_obj)
            except:
                continue