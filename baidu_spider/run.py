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

            # contentType 音频，视频，优质科普文章，专家回答, 专家语音解答
            if 'title' in json_obj['data']:
                contentType = json_obj['data']['title']
            elif 'extend_data' in json_obj['data']:
                contentType = json_obj['data']['extend_data']['title']
            elif 'extendData' in json_obj['data']:
                contentType = json_obj['data']['extendData']['title']
            else:
                contentType = '结构卡'

            if '_' in contentType:
                contentType = contentType.split('_')[1]
                contentType = re.sub('(\(.*?\))', '', contentType)
            if '-' in contentType:
                contentType = contentType.split('-')[0].strip()
            if 'hasVoice' in json_obj['data']:
                contentType = '音频'
            if 'video' in json_obj['data']:
                contentType = '视频'

            #contentStyle 搜索智能聚合
            if 'showLeftText' in json_obj['data']:
                contentStyle = json_obj['data']['showLeftText']
            elif 'extend_data' in json_obj['data'] and 'showLeftText' in json_obj['data']['extend_data']:
                contentStyle = json_obj['data']['extend_data']['showLeftText']
            elif 'extendData' in json_obj['data'] and 'showLeftText' in json_obj['data']['extendData']:
                contentStyle = json_obj['data']['extendData']['showLeftText']
            else:
                contentStyle = 'top1'


            #医生详情
            #1.top1样式1
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
            #1.top1样式2 结构卡 （头疼怎么办）
            elif 'tabList' in json_obj['data']:
                query = json_obj['data']['sgTitle']
                name = json_obj['data']['tabList'][0]['doctor']['name']
                hospital = json_obj['data']['tabList'][0]['doctor']['hospital']
                jobTitle = json_obj['data']['tabList'][0]['doctor']['level']
                origin = ''
                contentStyle = 'top1'
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
            #2.优质科普文章类型,  专家回答类型
            elif 'list' in json_obj['data'] or 'extend_data' in json_obj['data']:
                if 'list' in json_obj['data']:
                    data = json_obj['data']['list']
                elif 'extend_data' in json_obj['data']:
                    data = json_obj['data']['extend_data']['list']

                for item in data:
                    query = item['title'].replace('<em>', '').replace('</em>', '').replace('？', '').replace('。', '')
                    name = item['doctorName'] if 'doctorName' in item else item['doctorInfo'].split(' ')[0]
                    hospital = item['hospital'] if 'hospital' in item else item['doctorInfo'].split(' ')[1]
                    jobTitle = item['doctorTitle'] if 'doctorTitle' in item else ''

                    if 'list' in json_obj['data']:
                        origin = item['source']
                    elif 'extend_data' in json_obj['data']:
                        origin = item['miptitle']
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
            #3.视频类
            elif 'videoList' in json_obj['data']:
                for item in json_obj['data']['videoList']:
                    query = item['title'].replace('<em>', '').replace('</em>', '').replace('？', '').replace('。', '')
                    name = item['doctor_name'] if 'doctor_name' in item else ''
                    hospital = item['hospital'] if 'hospital' in item else ''
                    jobTitle = item['doctor_level'] if 'doctor_level' in item else ''
                    origin = item['source'] if 'source' in item else ''
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
                    if name == None:
                        continue
                    item_list.append(obj)
                    print(obj)
            #4.音频类
            elif 'extendData' in json_obj['data']:
                for item in json_obj['data']['extendData']['list']:
                    query = item['title'].replace('<em>', '').replace('</em>', '').replace('？', '').replace('。', '')
                    name = item['doctorName'] if 'doctorName' in item else ''
                    hospital = item['hospital'] if 'hospital' in item else ''
                    jobTitle = item['doctorTitle'] if 'doctorTitle' in item else ''
                    origin = item['miptitle'] if 'miptitle' in item else ''
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
                    if name == None:
                        continue
                    item_list.append(obj)
                    print(obj)


        self.write(item_list)

    def write(self,item_list):
        for item in item_list:
            with open('results.csv','a') as f:
                write_res = item['keyword'] + ',' + item['order'] + ',' + item['query'] + ',' + item['contentType'] + ',' + item['contentStyle'] + ',' + item['name'] + ',' + item['hospital'] + ',' + item['jobTitle'] + ',' + item['origin'] + '\n'
                f.write(write_res)
        if len(item_list) == 0:
            with open('failed_urls.txt', 'a') as f:
                f.write(str(url_boj) + '\n')


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
                f.write(str(url_boj) + '\n')
        else:
            spider.parse_html(url_boj, response)