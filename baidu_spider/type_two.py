#!/usr/bin/env python
# -*- coding:utf-8 -*-

from baidu_spider import download, config
from urllib.parse import quote
from lxml.etree import HTML
from lxml import etree
import re
import json

class TypeTwoSpider(object):
    def __init__(self):
        self.urls = []
        #初始化文件
        write_res = '关键词,搜索列表位置,query抓取,内容形式,内容展示样式,专家姓名,医院,职称,来源平台' + '\n'
        with open('resutls1.csv','a') as f:
            f.write(write_res)

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
        order_list = []
        item_list = []
        for res in results:
            json_obj = json.loads(res)

            #搜索列表位置  order
            order = json_obj['order']
            order_list.append(order)

            # contentType 音频，视频，优质科普文章，专家回答, 专家语音解答, 问答
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
            if 'video' in json_obj['data'] or ('videoList' in json_obj['data'] and len(json_obj['data']['videoList']) > 0) or 'media' in json_obj['data']:
                contentType = '视频'
            if '<em>' in contentType:
                contentType = '问答'

            #contentStyle top1, 搜索智能聚合, 权威样式（特殊处理）
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
                try:
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
                except:
                    pass
            #1.top1样式2 结构卡 （头疼怎么办）
            elif 'tabList' in json_obj['data']:
                if 'imageCount' not in json_obj['data']:
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
                    if 'doctorInfo' in item:
                        name = item['doctorName'] if 'doctorName' in item else item['doctorInfo'].split(' ')[0]
                        hospital = item['hospital'] if 'hospital' in item else item['doctorInfo'].split(' ')[1]
                    else:
                        name = item['doctorName'] if 'doctorName' in item else ''
                        hospital = item['hospital'] if 'hospital' in item else ''

                    jobTitle = item['doctorTitle'] if 'doctorTitle' in item else ''
                    if 'list' in json_obj['data']:
                        origin = item['source'] if 'source' in item else ''
                    elif 'extend_data' in json_obj['data']:
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
                    if name == '':
                        continue
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

        #匹配非js json模式的，权威样式
        html = HTML(html_text)
        # results = html.xpath('//div[@id="results"]/div[@class="c-result result c-clk-recommend"]')
        results = html.xpath('//div[@id="results"]/div[@class="c-result result"]')
        for res in results:
            detail_html_text = etree.tostring(res)
            order_res = re.search('order="(\d+)"', detail_html_text.decode()).group(1)
            if order_res in order_list:
                continue
            detail_html = HTML(detail_html_text.decode())
            order = order_res
            query = detail_html.xpath('string(//span[@class="c-title-text"])').split('_')[0].replace('?', '')
            # contentType = detail_html.xpath('string(//span[@class="c-title-text"])').split('_')[1]
            contentType = '问答'
            contentStyle = '权威样式'
            name = detail_html.xpath('string(//div[@class="c-span11 c-line-clamp1"]//span[1])')
            hospital = detail_html.xpath('string(//div[@class="c-span11 c-line-clamp1"]//span[3])')
            jobTitle = detail_html.xpath('string(//div[@class="c-span11 c-line-clamp1"]//span[2])')
            origin = detail_html.xpath('string(//span[@class="c-color-gray"])')
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
            if name == '':
                continue
            item_list.append(obj)
            print(obj)

        self.write(url_boj, item_list)

    def write(self, url_boj, item_list):
        for item in item_list:
            with open('results.csv','a') as f:
                write_res = item['keyword'] + ',' + item['order'] + ',' + item['query'] + ',' + item['contentType'] + ',' + item['contentStyle'] + ',' + item['name'] + ',' + item['hospital'] + ',' + item['jobTitle'] + ',' + item['origin'] + '\n'
                f.write(write_res)
        if len(item_list) == 0:
            with open('failed_urls.txt', 'a') as f:
                f.write(str(url_boj) + '\n')
