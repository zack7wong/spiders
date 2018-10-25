#!/usr/bin/env python
# -*- coding:utf-8 -*-

from news_spider import download, config
import re
import os


class BaiduSpider(object):
    def __init__(self):
        self.urls = []

    def get_urls(self):
        with open('urls.txt') as f:
            results = f.readlines()
            for res in results:
                try:
                    url = res.split('|')[0]
                    domain = res.split('|')[1]
                    title = res.split('|')[2]
                    keyword = res.split('|')[3]
                    description = res.split('|')[4].strip()
                    url_obj = {
                        'url': url,
                        'domain': domain,
                        'title': title,
                        'keyword': keyword,
                        'description': description,
                    }
                    self.urls.append(url_obj)
                except:
                    print('该行文本格式有误')
                    print(res)
                    with open('failed_urls.txt','a') as ff:
                        ff.write(res)

    def parse_html(self,url_boj,response):
        #处理编码问题
        charset = 'utf-8'
        try:
            try:
                search_res = re.search('meta.*?charset="(.*?)"', response.text)
                charset = search_res.group(1)
            except:
                search_res = re.search('meta.*?charset=(.*?)"', response.text)
                charset = search_res.group(1)
        except:
            pass
        try:
            response.encoding = charset
            html = response.text

            #保存文件
            pwd = os.getcwd()
            file_path = pwd + '/' + url_boj['domain']
            file_name = 'index.html'
            file_path_name = file_path + '/' + file_name
            with open(file_path_name, 'w', encoding=charset) as f:
                f.write()
        except:
            with open('failed_urls.txt', 'a') as ff:
                write_res = url_boj['url'] + '|' + url_boj['domain'] + '|' + url_boj['title'] + '|' + url_boj['keyword'] + '|' + url_boj['description']  + '\n'
                ff.write(write_res)



if __name__ == '__main__':
    spider = BaiduSpider()
    spider.get_urls()
    download = download.Download()
    for url_boj in spider.urls:
        response = download.get_html(url_boj['url'])
        if response is None:
            print('该URL请求失败')
            print(url_boj['url'])
            with open('failed_urls.txt', 'a') as ff:
                write_res = url_boj['url'] + '|' + url_boj['domain'] + '|' + url_boj['title'] + '|' + url_boj['keyword'] + '|' + url_boj['description'] + '\n'
                ff.write(write_res)
        else:
            spider.parse_html(url_boj,response)