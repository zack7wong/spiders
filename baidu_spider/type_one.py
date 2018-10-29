#!/usr/bin/env python
# -*- coding:utf-8 -*-
from baidu_spider import download, config
from urllib.parse import quote
from lxml.etree import HTML
from lxml import etree
import re
import json

class TypeOneSpider(object):
    def __init__(self):
        self.urls = []
        #初始化文件
        with open('results1.csv','a') as f:
            write_res = '问题标题,链接,top1,智能聚合,权威样式' + '\n'
            f.write(write_res)

    def get_urls(self):
        with open('title_url.txt') as f:
            results = f.readlines()
            for res in results:
                try:
                    title = res.split(',')[0]
                    exist_url = res.split(',')[1].strip()
                    url = config.START_URL.format(kw=quote(title))
                    url_obj = {
                        'title': title,
                        'exist_url': exist_url,
                        'url': url
                    }
                    self.urls.append(url_obj)
                except:
                    print('该行文本格式有误')
                    print(res)
                    with open('failed_urls.txt','a') as ff:
                        ff.write(res)

    def parse_html(self, url_boj, response):
        #top1，智能聚合, 权威样式
        #判断存不存在
        search_res = re.search(url_boj['exist_url'].replace('https://','').replace('http://',''), response)
        if search_res:
            #判断是否聚合
            find_results = re.findall('<script.*?data-repeatable>({"data".*?)</script>', response)
            flag = True
            for res in find_results:
                json_search = re.search(url_boj['exist_url'].replace('https://','').replace('http://',''), res)
                #是聚合，判断是不是top1
                if json_search:
                    flag = False
                    json_obj = json.loads(res)
                    if 'info' in json_obj['data'] or ('tabList' in json_obj['data'] and 'imageCount' not in json_obj['data']):
                        #是top1
                        with open('results1.csv', 'a') as f:
                            write_res = url_boj['title'] + ',' + url_boj['exist_url'] + ',' + '1' + ',' + '否' + ',' + '否' + '\n'
                            print(write_res)
                            f.write(write_res)
                            return None
                    else:
                        with open('results1.csv', 'a') as f:
                            write_res = url_boj['title'] + ',' + url_boj['exist_url'] + ',' + '否' + ',' + str(json['data']['order']) + ',' + '否' + '\n'
                            print(write_res)
                            f.write(write_res)
                            return None
            # 判断权威样式
            if flag:
                #非聚合，判断是不是top1
                html = HTML(response)
                results = html.xpath('//div[@id="results"]/div[@class="c-result result"]')
                for res in results:
                    detail_html_text = etree.tostring(res)
                    detail_search_res = re.search(url_boj['exist_url'].replace('https://','').replace('http://',''), detail_html_text.decode())
                    if detail_search_res:
                        order_res = re.search('order="(\d+)"', detail_html_text.decode())
                        if order_res:
                            if order_res.group(1) == '1':
                                exist_img = re.search('<img src=.*?', detail_html_text.decode())
                                if exist_img:
                                    #判断图片大小
                                    img_size = re.search('<img src=.*?w=(\d+)|<img src=.*?w%3D(\d+)', detail_html_text.decode())
                                    if img_size and int(img_size.group(1)) > 120:
                                        with open('results1.csv', 'a') as f:
                                            write_res = url_boj['title'] + ',' + url_boj['exist_url'] + ',' + '1' + ',' + '否' + ',' + '否' + '\n'
                                            print(write_res)
                                            f.write(write_res)
                                            return None
                                    else:
                                        with open('results1.csv', 'a') as f:
                                            write_res = url_boj['title'] + ',' + url_boj['exist_url'] + ',' + '否' + ',' + '否' + ',' + order_res.group(1) + '\n'
                                            print(write_res)
                                            f.write(write_res)
                                            return None
                                # 无图，全否
                                else:
                                    with open('results1.csv', 'a') as f:
                                        write_res = url_boj['title'] + ',' + url_boj[
                                            'exist_url'] + ',' + '否' + ',' + '否' + ',' + '否' + '\n'
                                        print(write_res)
                                        f.write(write_res)
                                        return None
                            #order不等于1，非top1
                            else:
                                exist_img = re.search('<img src=.*?', detail_html_text.decode())
                                # 有图，权威
                                if exist_img:
                                    with open('results1.csv', 'a') as f:
                                        write_res = url_boj['title'] + ',' + url_boj['exist_url'] + ',' + '否' + ',' + '否' + ',' + order_res.group(1) + '\n'
                                        print(write_res)
                                        f.write(write_res)
                                        return None
                                # 无图，全否
                                else:
                                    with open('results1.csv', 'a') as f:
                                        write_res = url_boj['title'] + ',' + url_boj['exist_url'] + ',' + '否' + ',' + '否' + ',' + '否' + '\n'
                                        print(write_res)
                                        f.write(write_res)
                                        return None
        else:
            #不存在
            with open('results1.csv', 'a') as f:
                write_res = url_boj['title']+','+url_boj['exist_url']+','+'否'+','+'否'+','+'否'+'\n'
                print(write_res)
                f.write(write_res)