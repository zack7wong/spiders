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
        spider.get_driver()
        spider.driver.get('http://www.baidu.com')
        spider.search(url_obj)