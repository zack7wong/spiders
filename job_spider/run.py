#!/usr/bin/env python
# -*- coding:utf-8 -*-

from job_spider import job
from job_spider import download
# import job
# import download
import json
import re
import os
import time



if __name__ == '__main__':
    spider = job.Job()
    download = download.Download()
    url_list = spider.get_url()
    for url_obj in url_list:
        print(url_obj['url'])
        print(json.dumps(url_obj['body']))
        response = download.get_html(url_obj['url'], method='post', body=json.dumps(url_obj['body']))
        if response is not None:
            print(response.text)
            spider.parse_html(response.text, url_obj)