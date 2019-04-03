#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests

import json
import re
from lxml.etree import HTML

headers = {
    'Connection': "keep-alive",
    'Pragma': "no-cache",
    'cache-control': "no-cache,no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cookie': "__gads=ID=8cbf091c8cdd44b1:T=1553857917:S=ALNI_MZFtDoSlRERR4ubfb_j_KOHIBamAQ; fp=e6209930b3b687d95aea7e5e6b3829d2; utag_main=v_id:0169c9263c180016e15c1d8af4a103078003a07000bd0$_sn:3$_ss:1$_st:1554202230736$vapi_domain:ieee.org$ses_id:1554200430736%3Bexp-session$_pn:1%3Bexp-session; AMCV_8E929CC25A1FB2B30A495C97%40AdobeOrg=1687686476%7CMCIDTS%7C17985%7CMCMID%7C66207938561781243761819043460489904872%7CMCAAMLH-1554805234%7C11%7CMCAAMB-1554805234%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1554207634s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.0.0; JSESSIONID=pPzhVXCTflbn8x4nJOEpo38C43qx5oFQctlyqi9FCZbFh8-DQqFj!-297104286; ipCheck=121.35.100.41; TS01d430e1=012f3506232d792ba044ae6856d85f49631d8b541865c710ac3c9f9998ce32010bf94bcbb5aa0f6dbb258ba9d63d16663f3692baacec63dbbb3929e67ab4dfe7d4471b538f9a18f3c60339cb2ee017272734848933; TS011813a0_26=014082121d4a522ccad18799094b9b62bb91ba7d74cc4c570776807f9349e54d22d29545d8c3a2d50d4d89c9d5bf03ed8c664a6ca3dc9b442e102a8b71890f5d5affba855e; WLSESSION=220357260.20480.0000; TS011813a0=012f350623960f943f7cecaf131755c20bc959dadc65c710ac3c9f9998ce32010bf94bcbb54ee1140511dc854f5a7f36282ed317906ccece8350951ecdb14dbc03133eaeb83ca5aaff1e24afb1883ad3fb6420999b; JSESSIONID=65niptKN2Pe0ifPErb9ly_Xkh2hj2Y_4zlBl17mkf2UY_2hSk7At!-1588170400; WLSESSION=220357260.20480.0000; TS011813a0=012f3506237027602bfb63c52f9674d1527a9c82297b64ca2e8900f959fa3273f480302380f5ef0904d81c795a038f2612d0fb7194b6de0b20fb36243f733fb1c4883f3ca4c22b648a1da5e0b178da0a83e8e8a076; TS01d430e1=012f3506232d792ba044ae6856d85f49631d8b541865c710ac3c9f9998ce32010bf94bcbb5aa0f6dbb258ba9d63d16663f3692baacec63dbbb3929e67ab4dfe7d4471b538f9a18f3c60339cb2ee017272734848933; TS011813a0_26=014082121d4a522ccad18799094b9b62bb91ba7d74cc4c570776807f9349e54d22d29545d8c3a2d50d4d89c9d5bf03ed8c664a6ca3dc9b442e102a8b71890f5d5affba855e",
    'Postman-Token': "e89bb6dc-ee1c-48df-b4b8-7e9a7c14eb63,c8bca514-17e0-446a-b87a-f9b24200779b",
    'Host': "ieeexplore.ieee.org"
    }

def deal(html):
    urls = html.xpath('//ul[@class="results"]/li//h3/a/@href')
    for url in urls:
        # print(url)
        link = 'https://ieeexplore.ieee.org' + url
        print(link)

        postId = re.search('https://ieeexplore.ieee.org/document/(\d+)/', link).group(1)

        # author，keyword
        # 期刊名字，文章标题，刊数，关键词，频次

        response = requests.get(link, headers=headers)
        # print(response.text)
        searchRes = re.search('metadata=(.*?)</script>', response.text, re.S)
        jsonStr = searchRes.group(1).strip()[:-1]
        print(jsonStr)
        json_obj = json.loads(jsonStr)

        # 作者
        author_list = []
        if 'authors' in json_obj:
            for data in json_obj['authors']:
                author_list.append(data['name'])
        authorStr = '，'.join(author_list)

        # 关键词
        ieee_keyword_list = []
        if 'keywords' in json_obj:
            for data in json_obj['keywords']:
                if data['type'] == 'IEEE Keywords':
                    ieee_keyword_list = data['kwd']
        ieee_keywordStr = '，'.join(ieee_keyword_list)

        author_keyword_list = []
        if 'keywords' in json_obj:
            for data in json_obj['keywords']:
                if data['type'] == 'Author Keywords' or data['type'] == 'Author Keywords ':
                    author_keyword_list = data['kwd']
        author_keywordStr = '，'.join(author_keyword_list)

        title = json_obj['title']
        abstract = json_obj['abstract']

        qikan = json_obj['publicationTitle']
        # ( Volume: 34 , Issue: 3 , March 2019 )
        kanshu = 'Volume:' + json_obj['volume'] + '，Issue:' + json_obj['issue'] + '，' + json_obj['publicationDate']

        save_res = id + '||' + postId + '||' + qikan + '||' + kanshu + '||' + title + '||' + ieee_keywordStr + '||' + author_keywordStr + '||' + authorStr + '||' + abstract + '||' + link
        save_res = save_res.replace(',', '，').replace('\n', '').replace('||', ',') + '\n'
        print(save_res)
        with open('结果.csv', 'a', encoding='gbk', errors='ignore') as f:
            f.write(save_res)

def start(id):
    start_url = 'https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber={id}&filter=issueId%20EQ%20%22{id}%22&pageNumber={pageToken}'
    url = start_url.format(id=id,pageToken=1)
    print(url)
    response = requests.get(url, headers=headers)
    html = HTML(response.text)

    #获取总数
    totalNum = len(html.xpath('//div[@class="pagination"]/a')) - 2
    if totalNum >=2:
        print('总页数：'+str(totalNum))

    #处理第一页
    deal(html)

    #获取其他页数
    for i in range(2,totalNum+1):
        print('当前页：'+str(i))
        print(start_url.format(id=id, pageToken=i))
        response = requests.get(start_url.format(id=id, pageToken=i), headers=headers)
        html = HTML(response.text)
        deal(html)



if __name__ == '__main__':
    with open('结果.csv', 'w', encoding='gbk') as f:
        f.write('期刊id,文章id,期刊名,刊数,标题,ieee keywords,author keywords,作者,摘要,链接\n')
    id = input('请输入链接id：')
    # id = '8636215'
    start(id)

