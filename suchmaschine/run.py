#!/usr/bin/env python
# -*- coding:utf-8 -*-

import getKeyword
import download
import baidu
import so
import sogou
import time
import config

def sort_res():
    result = sorted(config.RESULTS, key=lambda x: (x['pageNum'], x['rank']))
    return result


def save_res(results):
    for res in results:
        if res['type'] == 'web_sogou':
            type = '搜狗'
        elif res['type'] == 'm_sogou':
            type = '搜狗移动'
        elif res['type'] == 'web_baidu':
            type = '百度'
        elif res['type'] == 'm_baidu':
            type = '百度移动'
        elif res['type'] == 'web_so':
            type = '360'
        elif res['type'] == 'm_so':
            type = '360移动'

        write_res = myAlign('关键词：%s' % res['keyword']) + myAlign('来源：%s' % type) + myAlign('排名：第%s页第%s个' % (res['pageNum'], res['rank'])) + '\n'
        print(write_res)
        write(write_res)

def myAlign(string):
    slen = len(string)
    res = string
    if isinstance(string, str):
        placeholder = u'　'
    else:
        placeholder = u' '
    while slen < 30:
        res += placeholder
        slen += 1
    return res

def write(results):
    with open('results.txt', 'a') as f:
        f.write(results)


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
            # baidu.save_res()

            so.web_search(kw_list, url_obj)
            so.m_search(kw_list, url_obj)
            # so.save_res()

            sogou.web_search(kw_list, url_obj)
            sogou.m_search(kw_list, url_obj)
            # sogou.save_res()

            results = sort_res()
            save_res(results)
            print('已结束...60秒后关闭...')
            time.sleep(60)
        else:
            print('url访问失败：'+url)