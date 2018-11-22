#!/usr/bin/env python
# -*- coding:utf-8 -*-

import getKeyword
import download
import baidu
import so
import sogou
import time

if __name__ == '__main__':
    keyword_obj = getKeyword.getKeyword()
    urls_list = keyword_obj.get_url()
    down = download.Download()
    baidu = baidu.Baidu()
    so = so.So()
    sogou = sogou.Sogou()
    for url_obj in urls_list:
        url = url_obj['url']
        print('当前网站：'+url)
        print('当前域名：'+url_obj['domain'])
        print('正在获取关键词。。')
        response = down.get_html(url)
        if response:
            kw_list = keyword_obj.get_keyword(response)
            # kw_list = ['无锡阿里巴巴外贸']
            print(kw_list)

            baidu.web_search(kw_list,url_obj)
            baidu.m_search(kw_list,url_obj)
            baidu.save_res()

            so.web_search(kw_list, url_obj)
            so.m_search(kw_list, url_obj)
            so.save_res()

            sogou.web_search(kw_list, url_obj)
            sogou.m_search(kw_list, url_obj)
            sogou.save_res()

            print('已结束...60秒后关闭...')
            time.sleep(60)
        else:
            print('url访问失败：'+url)