#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
from lxml.etree import HTML


import re
import json
import urllib
import os
from urllib.parse import quote,unquote

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Cookie': "FIRSTVISITED=1554096226.748; bt_guid=ec16d34d2baceedf2b394d57e5f1d376; sign=WEIXIN; login_type=WEIXIN; auth_id=9245319%7C%E9%83%AD%E5%9B%BA%E6%B1%9F%7C1555423029%7Cb3b7eaa20481a3a34ccb2290e3452386; sns=%7B%22type%22%3A%22weixin%22%2C%22token%22%3A%7B%22access_token%22%3A%2220_mY_u7iy4dYqmWNa3sVHgLEHEQXTcU0kJ4AWrfKfslpHxbSv3pIBlCdbXcVz3e0Qqhw2AFJunsssT7o3bX8cC2g%22%2C%22expires_in%22%3A7200%2C%22refresh_token%22%3A%2220__fzuqg96EcBnzC4IU3ZBYjEEh43XtiF0b0U-cSaM3GvIgAWR8wfv0T3L3vnF1auoiqBtN8_TPebd-fCEaqTjnw%22%2C%22openid%22%3A%22oMdYSvzyMcFeRmliF_1e3BYJb3UM%22%2C%22scope%22%3A%22snsapi_login%22%2C%22unionid%22%3A%22oZ_uiwfNHrrFS_CIz3DtlYrnBfkY%22%7D%7D; Array=%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FB7MFzDy6jTicXJFWou4ibBMXkq1ICdJsH37EKSj7zG0lhVXEKHlHCw9evQTkibuCzdCHvwY0jY9kTiaqFxya7ADXjQ%2F132; ISREQUEST=1; WEBPARAMS=is_pay=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%229245319%22%2C%22%24device_id%22%3A%22169d75a7c19f5-00e6bebbad417d-12366d56-2073600-169d75a7c1b98%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22169d75a7c19f5-00e6bebbad417d-12366d56-2073600-169d75a7c1b98%22%7D; Hm_lvt_2b0a2664b82723809b19b4de393dde93=1554096226,1554127033,1554294957; Hm_lvt_4df399c02bb6b34a5681f739d57787ee=1554096227,1554127033,1554294958; Hm_lpvt_2b0a2664b82723809b19b4de393dde93=1554294998; Hm_lpvt_4df399c02bb6b34a5681f739d57787ee=1554294998",
    'Host': "proxy-rar.ibaotu.com",
    'Pragma': "no-cache",
    'Referer': "https://ibaotu.com/?m=download&id=17972779",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "41752a7e-aebb-4aab-9be7-cdcd74f651f9"
    }

location_headers = {
    'Host': "ibaotu.com",
    'Connection': "keep-alive",
    'Pragma': "no-cache",
    'Cache-Control': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cookie': "_uab_collina=155409622454376629752093; islogout=1; FIRSTVISITED=1554096226.748; bt_guid=ec16d34d2baceedf2b394d57e5f1d376; sign=WEIXIN; login_type=WEIXIN; auth_id=9245319%7C%E9%83%AD%E5%9B%BA%E6%B1%9F%7C1555423029%7Cb3b7eaa20481a3a34ccb2290e3452386; sns=%7B%22type%22%3A%22weixin%22%2C%22token%22%3A%7B%22access_token%22%3A%2220_mY_u7iy4dYqmWNa3sVHgLEHEQXTcU0kJ4AWrfKfslpHxbSv3pIBlCdbXcVz3e0Qqhw2AFJunsssT7o3bX8cC2g%22%2C%22expires_in%22%3A7200%2C%22refresh_token%22%3A%2220__fzuqg96EcBnzC4IU3ZBYjEEh43XtiF0b0U-cSaM3GvIgAWR8wfv0T3L3vnF1auoiqBtN8_TPebd-fCEaqTjnw%22%2C%22openid%22%3A%22oMdYSvzyMcFeRmliF_1e3BYJb3UM%22%2C%22scope%22%3A%22snsapi_login%22%2C%22unionid%22%3A%22oZ_uiwfNHrrFS_CIz3DtlYrnBfkY%22%7D%7D; Array=%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FB7MFzDy6jTicXJFWou4ibBMXkq1ICdJsH37EKSj7zG0lhVXEKHlHCw9evQTkibuCzdCHvwY0jY9kTiaqFxya7ADXjQ%2F132; ISREQUEST=1; WEBPARAMS=is_pay=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%229245319%22%2C%22%24device_id%22%3A%22169d75a7c19f5-00e6bebbad417d-12366d56-2073600-169d75a7c1b98%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22169d75a7c19f5-00e6bebbad417d-12366d56-2073600-169d75a7c1b98%22%7D; Hm_lvt_2b0a2664b82723809b19b4de393dde93=1554096226,1554127033,1554294957; sign=null; Hm_lvt_4df399c02bb6b34a5681f739d57787ee=1554096227,1554127033,1554294958; Hm_lpvt_2b0a2664b82723809b19b4de393dde93=1554295408; Hm_lpvt_4df399c02bb6b34a5681f739d57787ee=1554295409",
    'cache-control': "no-cache",
    'Postman-Token': "66de2a0a-f2e1-4b69-8426-0261c82e5431"
    }

def start(item):
    pageNum = int(item['pageNum'])
    catName = item['catName']
    url = item['url']

    path = os.path.join(os.getcwd(), catName)
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)

    for i in range(1,pageNum):
        print('当前页：'+str(i))
        if 'pageToken' in url:
            start_url = url.format(pageToken=i)
        else:
            start_url = url

        try:
            response = requests.get(start_url,timeout=10)
        except:
            print('请求列表错误')
            continue
        # print(response.text)

        html = HTML(response.text)
        urls = html.xpath('//div[@class="bt-body search clearfix"]/dl[@class="pic-box"]//a[@class="down-btn gradient-hor-og"]/@href')
        for url in urls:
            # print(url)

            id = re.search('//ibaotu.com/\?m=download&id=(\d+)$', url).group(1)

            link = 'https://ibaotu.com/?m=downloadopen&a=open&id='+id+'&down_type=1&type=1'
            print(link)


            try:
                response = requests.get(link, headers=location_headers, timeout=10, allow_redirects=False)
                # print(response.text)
                if '此图片您已经下载过啦' in response.text:
                    print('此图片您已经下载过啦')
                    continue
                location_url = response.headers['location']
                location_quote = unquote(location_url)
                # print(location_quote)
                fileName = re.search('https://.*?ibaotu.com/.*?&n=(.*?)\.(.*?)$', location_quote).group(1)
                fileName_type = re.search('https://.*?ibaotu.com/.*?&n=(.*?)\.(.*?)$', location_quote).group(2)
                savefileName = fileName + '.' + fileName_type
            except:
                print('请求详情页出错')
                continue


            print('正在下载。。'+savefileName)
            endPath = os.path.join(path,savefileName)
            # video_response = requests.get(src,headers=headers)
            # with open(fileName,'wb') as f:
            #     f.write(video_response.content)
            try:
                urllib.request.urlretrieve(location_url, endPath)
            except:
                print('下载出错')
                continue


if __name__ == '__main__':

    item_list = []
    with open('ibaotu.txt') as f:
        results = f.readlines()
        for res in results:
            catName = res.split(',')[0]
            url = res.split(',')[1]
            pageNum = res.split(',')[2].strip()
            obj = {
                'catName':catName,
                'url':url,
                'pageNum':pageNum,
            }
            item_list.append(obj)
    for item in item_list:
        print(item)
        start(item)