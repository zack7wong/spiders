#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
from lxml.etree import HTML


import re
import json
import urllib

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Cookie': "uniqid=5ca20c1dc3ab0; search_notice=1; user_uniqid=5ABFDD6945D15210; FIRSTVISITED=1554123809.343; from_data=YTo2OntzOjQ6Imhvc3QiO3M6MTA6IjY5OXBpYy5jb20iO3M6Mzoic2VtIjtiOjA7czoxMDoic291cmNlZnJvbSI7aTowO3M6NDoid29yZCI7TjtzOjM6ImtpZCI7aTowO3M6ODoic2VtX3R5cGUiO2k6MDt9; session_data=YTo1OntzOjM6InVpZCI7czo4OiIxOTQ0OTc2OCI7czo1OiJ0b2tlbiI7czozMjoiZGZhMGMyOTZiN2FlOGFmM2RhOGU5MTdjZDE3YzY0NjMiO3M6MzoidXV0IjtzOjMyOiJiZjZmOTI3YmQ0Njg5NGI3NjJjMjI4NmE3NTY2ZGJkZSI7czo0OiJkYXRhIjthOjE6e3M6ODoidXNlcm5hbWUiO3M6NDoiSmFtZSI7fXM6NjoiZXh0aW1lIjtpOjE1NTQ3MzEwMjY7fQ%3D%3D; username=Jame; uid=19449768; isdiyici=1; is_qy_vip=1; activeMuchun_2=1; ISREQUEST=1; WEBPARAMS=is_pay=1; video_youhui_v2=423; login_view=1; PHPSESSID=2bed8b8cabb80e4fdec2307bd3953a6d; login_user=1; resource_number_data20190403=997051%2C387417%2C140273%2C85941%2C67059%2C52915%2C44686%2C14453%2C252239%2C3367; s_token=9faa70a29b59782df3d76f3c4034afeb; Hm_lvt_e37e21a48e66c7bbb5d74ea6f717a49c=1554123810,1554291815; Hm_lpvt_e37e21a48e66c7bbb5d74ea6f717a49c=1554291815; Hm_lvt_ddcd8445645e86f06e172516cac60b6a=1554123810,1554291816; Hm_lvt_1154154465e0978ab181e2fd9a9b9057=1554123810,1554291816; active16_2=1; index-collectHInt=1; video_time_2=1554291822; search_mode=video; Hm_lpvt_ddcd8445645e86f06e172516cac60b6a=1554291983; Hm_lpvt_1154154465e0978ab181e2fd9a9b9057=1554291983",
    'Host': "699pic.com",
    'Pragma': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "3e0d834c-61bd-4bab-9d38-b3f37d3e46b8"
    }

def start():

    for i in range(1,401):
        print('当前页：'+str(i))
        url = 'http://699pic.com/video-sousuo-0-0-{pageToken}-0-0-0.html'

        try:
            response = requests.get(url.format(pageToken=i),timeout=10)
        except:
            print('请求列表错误')
            continue
        # print(response.text)

        html = HTML(response.text)
        urls = html.xpath('//div[@class="swipeboxEx"]/div//a[@class="video-name fl"]/@href')
        for url in urls:
            # print(url)

            id = re.search('/video-(\d+).html',url).group(1)
            down_url = 'http://699pic.com/download/video?id='+id


            # print(down_url)
            try:
                response = requests.get(down_url,headers=headers,timeout=10)
            except:
                print('请求详情页出错')
                continue
            json_obj = json.loads(response.text)
            src = json_obj['src']
            # print(src)
            fileName = '摄图网_video_'+id+'.zip'
            print('正在下载。。'+fileName)

            # video_response = requests.get(src,headers=headers)
            # with open(fileName,'wb') as f:
            #     f.write(video_response.content)
            try:
                urllib.request.urlretrieve(src, fileName)
            except:
                print('下载出错')
                continue

if __name__ == '__main__':
    start()