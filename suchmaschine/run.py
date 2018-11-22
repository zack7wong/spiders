#!/usr/bin/env python
# -*- coding:utf-8 -*-

import getKeyword
import download
import baidu
import time

if __name__ == '__main__':
    keyword_obj = getKeyword.getKeyword()
    urls_list = keyword_obj.get_url()
    down = download.Download()
    baidu = baidu.Baidu()
    for url_obj in urls_list:
        url = url_obj['url']
        print('当前网站：'+url)
        print('正在获取关键词。。')
        response = down.get_html(url)
        if response:
            kw_list = keyword_obj.get_keyword(response)
            print(kw_list)
            baidu.web_search(kw_list,url_obj)
            baidu.m_search(kw_list,url_obj)
            baidu.save_res()
            print('已结束')
            time.sleep(60)
        else:
            print('url访问失败：'+url)