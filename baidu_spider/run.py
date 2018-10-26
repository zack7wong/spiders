#!/usr/bin/env python
# -*- coding:utf-8 -*-

from baidu_spider import download, config
from urllib.parse import quote
from lxml.etree import HTML
from lxml import etree
import re
import os
import json

class BaiduSpider(object):
    def __init__(self):
        self.urls = []

    def get_urls(self):
        with open('keyword.txt') as f:
            results = f.readlines()
            for res in results:
                try:
                    keyword = res.replace('\n', '')
                    url = config.START_URL.format(kw=quote(keyword))
                    url_obj = {
                        'url': url,
                        'keyword': keyword,
                    }
                    self.urls.append(url_obj)
                except:
                    print('该行文本格式有误')
                    print(res)
                    with open('failed_urls.txt','a') as ff:
                        ff.write(res)

    def parse_html(self,url_boj,response):
        #处理编码问题
        # charset = 'utf-8'
        # try:
        #     try:
        #         search_res = re.search('meta.*?charset="(.*?)"', response.text)
        #         charset = search_res.group(1)
        #     except:
        #         search_res = re.search('meta.*?charset=(.*?)"', response.text)
        #         charset = search_res.group(1)
        # except:
        #     pass

        html_text = response
        results = re.findall('<script.*?data-repeatable>({"data".*?)</script>',html_text)
        item_list = []
        for res in results:
            json_obj = json.loads(res)

            #搜索列表位置  order
            order = json_obj['order']

            #搜索智能聚合  contentStyle
            if 'showLeftText' in json_obj['data']:
                contentStyle = json_obj['data']['showLeftText']
            elif 'extend_data' in json_obj['data']:
                if 'showLeftText' in json_obj['data']['extend_data']:
                    contentStyle = json_obj['data']['extend_data']['showLeftText']
            else:
                contentStyle = 'top1'

            #音频，视频，优质科普文章  contentType
            if 'title' in json_obj['data']:
                contentType = json_obj['data']['title']
                if '_' in contentType:
                    contentType = contentType.split('_')[1]
                if '-' in contentType:
                    contentType = contentType.split('-')[1]
                if 'hasVoice' in json_obj['data']:
                    contentType = '音频'

            #医生详情
            #1.top1样式
            if 'info' in json_obj['data']:
                query = json_obj['data']['unhighTitle']
                name = json_obj['data']['info']['author']['name']
                hospital = json_obj['data']['info']['content'][1]
                jobTitle = json_obj['data']['info']['content'][0]
                origin = json_obj['data']['showurl_area']['logo_name']
                obj = {
                    'keyword': url_boj['keyword'],
                    'order': order,
                    'query': query,
                    'contentType': contentType,
                    'contentStyle': contentStyle,
                    'name': name,
                    'hospital': hospital,
                    'jobTitle': jobTitle,
                    'origin': origin,
                }
                item_list.append(obj)
                print(obj)
            #2.优质文章类型
            elif 'list' in json_obj['data']:
                for item in json_obj['data']['list']:
                    query = item['title'].split('<em>', '').split('</em>', '')
                    obj = {
                        'keyword': url_boj['keyword'],
                        'order': order,
                        'query': query,
                        'contentType': contentType,
                        'contentStyle': contentStyle,
                        'name': name,
                        'hospital': hospital,
                        'jobTitle': jobTitle,
                        'origin': origin,
                    }
                    item_list.append(obj)
                    print(obj)

            # html = HTML(html_text)
            # results = html.xpath('//div[@id="results"]/div[@class="c-result result c-clk-recommend"]')
            # results = html.xpath('//div[@id="results"]/div[@class="c-result result"]')
            # print(results)
            #
            # for res in results:
            #     detail_html_text = etree.tostring(res)
            #     detail_html = HTML(detail_html_text.decode())
            #     detail = detail_html.xpath('string(//div[@class="c-result-content"])')
            #     print(detail)

        # except:
        #     with open('failed_urls.txt', 'a') as f:
        #         f.write(str(url_boj))



if __name__ == '__main__':
    spider = BaiduSpider()
    spider.get_urls()
    download = download.Download()
    for url_boj in spider.urls:
        print(url_boj)
        # response = download.driver_get_html(url_boj['url'])
        response = download.get_html(url_boj['url'])
        if response is None:
            print('该URL请求失败')
            print(url_boj['url'])
            with open('failed_urls.txt', 'a') as f:
                f.write(str(url_boj))
        else:
            spider.parse_html(url_boj, response)
            break