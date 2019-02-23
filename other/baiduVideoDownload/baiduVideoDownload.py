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
import random


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
}

payload_list = [
    '_client_id=wappc_1550900051497_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=4&sign=886E2EB27A80BB43F84C58AD58C1CA07&stErrorNums=1&stMethod=1&stMode=1&stSize=886&stTime=386&stTimesNum=1&st_type=personalize_page&tid=6044618024&timestamp=1550927304974&user_view_data=%5B%7B%22tid%22%3A%225894836179%22%2C%22duration%22%3A26%7D%5D&yuelaou_locate=110142%2312%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=85823C9E342C0D3B2FF0F5514A787D44&stErrorNums=1&stMethod=1&stMode=1&stSize=804&stTime=487&stTimesNum=1&st_type=personalize_page&tid=6045267465&timestamp=1550927774921&user_view_data=%5B%7B%22tid%22%3A%225965165949%22%2C%22duration%22%3A2%7D%2C%7B%22tid%22%3A%225858909216%22%2C%22duration%22%3A9%7D%2C%7B%22tid%22%3A%226037928279%22%2C%22duration%22%3A2%7D%2C%7B%22tid%22%3A%226027590223%22%2C%22duration%22%3A0%7D%2C%7B%22tid%22%3A%225994089822%22%2C%22duration%22%3A1%7D%2C%7B%22tid%22%3A%226027588593%22%2C%22duration%22%3A0%7D%2C%7B%22tid%22%3A%225967442030%22%2C%22duration%22%3A1%7D%5D&yuelaou_locate=110141%239%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=2&sign=2AC3BFC7434C86F33664BFD5BCCC9979&stErrorNums=1&stMethod=1&stMode=1&stSize=886&stTime=484&stTimesNum=1&st_type=personalize_page&tid=6045267465&timestamp=1550927818617&user_view_data=%5B%7B%22tid%22%3A%226045267465%22%2C%22duration%22%3A0%7D%2C%7B%22tid%22%3A%225818213801%22%2C%22duration%22%3A0%7D%2C%7B%22tid%22%3A%225980826176%22%2C%22duration%22%3A2%7D%5D&yuelaou_locate=110141%239%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=3&sign=C1F4FCA7A5C120F6D39B7C637669CE47&stErrorNums=1&stMethod=1&stMode=1&stSize=886&stTime=103&stTimesNum=1&st_type=personalize_page&tid=6045267465&timestamp=1550927840422&user_view_data=%5B%7B%22tid%22%3A%225992659099%22%2C%22duration%22%3A0%7D%2C%7B%22tid%22%3A%225985772792%22%2C%22duration%22%3A18%7D%5D&yuelaou_locate=110141%239%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=4&sign=B7A045FA744A812416DB8D136303585A&stErrorNums=1&stMethod=1&stMode=1&stSize=805&stTime=164&stTimesNum=1&st_type=personalize_page&tid=6045267465&timestamp=1550927868532&user_view_data=%5B%7B%22tid%22%3A%225980000693%22%2C%22duration%22%3A25%7D%5D&yuelaou_locate=110141%239%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=5&sign=562060B7E12952A8CDD9C2D3E76D81C0&stErrorNums=1&stMethod=1&stMode=1&stSize=886&stTime=257&stTimesNum=1&st_type=personalize_page&tid=6045267465&timestamp=1550927877658&user_view_data=%5B%7B%22tid%22%3A%226017814355%22%2C%22duration%22%3A7%7D%5D&yuelaou_locate=110141%239%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=6&sign=63DB6AA742861618D083BB13FDB08A7B&stErrorNums=1&stMethod=1&stMode=1&stSize=803&stTime=128&stTimesNum=1&st_type=personalize_page&tid=6045267465&timestamp=1550927887660&user_view_data=%5B%7B%22tid%22%3A%225927475149%22%2C%22duration%22%3A8%7D%5D&yuelaou_locate=110141%239%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
]

def start():
    try:
        url = "http://14.215.177.221/c/f/video/getVideoMidPage"
        # payload = "_client_id=wappc_1550900051497_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=2&sign=0B4BCA3C7425E1B756AC4166928D6DBA&stErrorNums=1&stMethod=1&stMode=1&stSize=886&stTime=243&stTimesNum=1&st_type=personalize_page&tid=6044618024&timestamp=1550901221750&user_view_data=%5B%7B%22tid%22%3A%226044618024%22%2C%22duration%22%3A89%7D%2C%7B%22tid%22%3A%225986489933%22%2C%22duration%22%3A45%7D%2C%7B%22tid%22%3A%225987781592%22%2C%22duration%22%3A19%7D%2C%7B%22tid%22%3A%225788304980%22%2C%22duration%22%3A10%7D%2C%7B%22tid%22%3A%225894847432%22%2C%22duration%22%3A25%7D%2C%7B%22tid%22%3A%225911348141%22%2C%22duration%22%3A77%7D%2C%7B%22tid%22%3A%225991767356%22%2C%22duration%22%3A36%7D%2C%7B%22tid%22%3A%225917483889%22%2C%22duration%22%3A69%7D%2C%7B%22tid%22%3A%225981183080%22%2C%22duration%22%3A108%7D%5D&yuelaou_locate=110142%2312%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal"
        # payload = "_client_id=wappc_1550900051497_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=4&sign=886E2EB27A80BB43F84C58AD58C1CA07&stErrorNums=1&stMethod=1&stMode=1&stSize=886&stTime=386&stTimesNum=1&st_type=personalize_page&tid=6044618024&timestamp=1550927304974&user_view_data=%5B%7B%22tid%22%3A%225894836179%22%2C%22duration%22%3A26%7D%5D&yuelaou_locate=110142%2312%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal"
        payload = random.choice(payload_list)
        # print(payload)
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
                    # urllib.request.urlretrieve(videoUrl, fileName)
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


