#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     baiduVideoDownload
   Description :
   Author :        hayden_huang
   Date：          2019/2/23 15:57
-------------------------------------------------
"""

import requests
import json
import time
import urllib
import os


headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Cookie': "ka=open;",
    'cuid_gid': "",
    'cuid': "B3088C2A62F38E3846E34328BFB847CE|0",
    'client_logid': "1550900043496",
    'Host': "c.tieba.baidu.com",
    'Charset': "UTF-8",
    'cuid_galaxy2': "B3088C2A62F38E3846E34328BFB847CE|0",
    'User-Agent': "bdtb for Android 9.9.8.42",
    'Accept-Encoding': "gzip",
    'Content-Length': "1094",
    'Connection': "keep-alive",
    'cache-control': "no-cache",
    'Postman-Token': "f2a2e48a-f103-4aff-b460-f6e02c9c5dac"
    }

def start():
    try:
        url = "http://14.215.177.221/c/f/video/getVideoMidPage"
        payload = "_client_id=wappc_1550900051497_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=2&sign=0B4BCA3C7425E1B756AC4166928D6DBA&stErrorNums=1&stMethod=1&stMode=1&stSize=886&stTime=243&stTimesNum=1&st_type=personalize_page&tid=6044618024&timestamp=1550901221750&user_view_data=%5B%7B%22tid%22%3A%226044618024%22%2C%22duration%22%3A89%7D%2C%7B%22tid%22%3A%225986489933%22%2C%22duration%22%3A45%7D%2C%7B%22tid%22%3A%225987781592%22%2C%22duration%22%3A19%7D%2C%7B%22tid%22%3A%225788304980%22%2C%22duration%22%3A10%7D%2C%7B%22tid%22%3A%225894847432%22%2C%22duration%22%3A25%7D%2C%7B%22tid%22%3A%225911348141%22%2C%22duration%22%3A77%7D%2C%7B%22tid%22%3A%225991767356%22%2C%22duration%22%3A36%7D%2C%7B%22tid%22%3A%225917483889%22%2C%22duration%22%3A69%7D%2C%7B%22tid%22%3A%225981183080%22%2C%22duration%22%3A108%7D%5D&yuelaou_locate=110142%2312%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal"

        try:
            response = requests.request("POST", url, data=payload, headers=headers)
        except:
            print('获取数据失败')

        # print(response.text)
        json_obj = json.loads(response.text)
        for data in json_obj['list']:
            # print(json.dumps(data))
            title = data['title']
            if 'video_desc' in data['video']:
                if isinstance(data['video']['video_desc'],list) and len(data['video']['video_desc'])>0:
                    videoUrl = data['video']['video_desc'][-1]['video_url']
                    print('正在下载：'+title)
                    fileName = title+'.mp4'
                    fileName = os.path.join('video', fileName)
                    try:
                        urllib.request.urlretrieve(videoUrl, fileName)
                        print('下载成功')
                    except:
                        print('下载失败')
                        continue
    except:
        print('未知错误')

if __name__ == '__main__':

    # flag = 0
    # for root, dirs, files in os.walk(".", topdown=False):
    #     for name in dirs:
    #         if 'vidoe' == name:
    #             flag = 1
    #             break

    path = os.path.join(os.getcwd(),'video')
    # print(path)
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)

    while True:
        print('当前时间：'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        start()


