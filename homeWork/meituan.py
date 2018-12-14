#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import json
import requests


headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Cookie': "_lxsdk_cuid=165d5c284d5c8-0ecc3a2e62a215-34647908-13c680-165d5c284d5c8; ci=30; iuuid=264956EEBB97729C4769D15722680FE5AB6637B3C28F769B658ADD6801BCC444; cityname=%E6%B7%B1%E5%9C%B3; i_extend=H__a100001__b1; webp=1; _ga=GA1.2.1170109347.1540362537; _lxsdk=264956EEBB97729C4769D15722680FE5AB6637B3C28F769B658ADD6801BCC444; uuid=86dd7c3fdd5d413894aa.1544776788.1.0.0; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; _gid=GA1.2.1020230120.1544776802; client-id=68ebe83a-cf01-4f43-be26-473bf13ec096; _lxsdk_s=%7C%7CNaN",
    'Host': "wz.meituan.com",
    'Pragma': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "ffc9fb2a-4a65-4979-a379-866ee314f8be"
    }

for i in range(5):

    url = 'https://wz.meituan.com/meishi/pn{page}/'.format(page=str(i))
    response = requests.get(url,headers=headers)
    search_res = re.search('window._appState = (.*?);</script>',response.text)
    json_obj = json.loads(search_res.group(1))

    for data in json_obj['poiLists']['poiInfos']:
        title = data['title']
        address = data['address']
        avgScore = data['avgScore']
        allCommentNum = data['allCommentNum']
        avgPrice = data['avgPrice']
        res = title+','+address+','+str(avgScore)+','+str(allCommentNum)+','+str(avgPrice)+'\n'
        print(res)
        with open('meituan.csv','a') as f:
            f.write(res)