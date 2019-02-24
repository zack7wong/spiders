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
    # 'cuid': "B3088C2A62F38E3846E34328BFB847CE|0",
    'client_logid': "1550900043496",
    'Host': "c.tieba.baidu.com",
    'Charset': "UTF-8",
    # 'cuid_galaxy2': "B3088C2A62F38E3846E34328BFB847CE|0",
    'User-Agent': "bdtb for Android 9.9.8.42",
    'Accept-Encoding': "gzip",
    # 'Content-Length': "1094",
    'Connection': "keep-alive",
    'cache-control': "no-cache",
}

# payload_list = [
#     '_client_id=wappc_1550900051497_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=4&sign=886E2EB27A80BB43F84C58AD58C1CA07&stErrorNums=1&stMethod=1&stMode=1&stSize=886&stTime=386&stTimesNum=1&st_type=personalize_page&tid=6044618024&timestamp=1550927304974&user_view_data=%5B%7B%22tid%22%3A%225894836179%22%2C%22duration%22%3A26%7D%5D&yuelaou_locate=110142%2312%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
#     '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=85823C9E342C0D3B2FF0F5514A787D44&stErrorNums=1&stMethod=1&stMode=1&stSize=804&stTime=487&stTimesNum=1&st_type=personalize_page&tid=6045267465&timestamp=1550927774921&user_view_data=%5B%7B%22tid%22%3A%225965165949%22%2C%22duration%22%3A2%7D%2C%7B%22tid%22%3A%225858909216%22%2C%22duration%22%3A9%7D%2C%7B%22tid%22%3A%226037928279%22%2C%22duration%22%3A2%7D%2C%7B%22tid%22%3A%226027590223%22%2C%22duration%22%3A0%7D%2C%7B%22tid%22%3A%225994089822%22%2C%22duration%22%3A1%7D%2C%7B%22tid%22%3A%226027588593%22%2C%22duration%22%3A0%7D%2C%7B%22tid%22%3A%225967442030%22%2C%22duration%22%3A1%7D%5D&yuelaou_locate=110141%239%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
#     '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=2&sign=2AC3BFC7434C86F33664BFD5BCCC9979&stErrorNums=1&stMethod=1&stMode=1&stSize=886&stTime=484&stTimesNum=1&st_type=personalize_page&tid=6045267465&timestamp=1550927818617&user_view_data=%5B%7B%22tid%22%3A%226045267465%22%2C%22duration%22%3A0%7D%2C%7B%22tid%22%3A%225818213801%22%2C%22duration%22%3A0%7D%2C%7B%22tid%22%3A%225980826176%22%2C%22duration%22%3A2%7D%5D&yuelaou_locate=110141%239%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
#     '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=3&sign=C1F4FCA7A5C120F6D39B7C637669CE47&stErrorNums=1&stMethod=1&stMode=1&stSize=886&stTime=103&stTimesNum=1&st_type=personalize_page&tid=6045267465&timestamp=1550927840422&user_view_data=%5B%7B%22tid%22%3A%225992659099%22%2C%22duration%22%3A0%7D%2C%7B%22tid%22%3A%225985772792%22%2C%22duration%22%3A18%7D%5D&yuelaou_locate=110141%239%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
#     '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=4&sign=B7A045FA744A812416DB8D136303585A&stErrorNums=1&stMethod=1&stMode=1&stSize=805&stTime=164&stTimesNum=1&st_type=personalize_page&tid=6045267465&timestamp=1550927868532&user_view_data=%5B%7B%22tid%22%3A%225980000693%22%2C%22duration%22%3A25%7D%5D&yuelaou_locate=110141%239%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
#     '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=5&sign=562060B7E12952A8CDD9C2D3E76D81C0&stErrorNums=1&stMethod=1&stMode=1&stSize=886&stTime=257&stTimesNum=1&st_type=personalize_page&tid=6045267465&timestamp=1550927877658&user_view_data=%5B%7B%22tid%22%3A%226017814355%22%2C%22duration%22%3A7%7D%5D&yuelaou_locate=110141%239%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
#     '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=6&sign=63DB6AA742861618D083BB13FDB08A7B&stErrorNums=1&stMethod=1&stMode=1&stSize=803&stTime=128&stTimesNum=1&st_type=personalize_page&tid=6045267465&timestamp=1550927887660&user_view_data=%5B%7B%22tid%22%3A%225927475149%22%2C%22duration%22%3A8%7D%5D&yuelaou_locate=110141%239%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
# ]

payload_list = [
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=97A15F8127F6023AC3391BA37303A42B&stErrorNums=1&stMethod=1&stMode=1&stSize=783&stTime=303&stTimesNum=1&st_type=personalize_page&tid=6045484355&timestamp=1550997023073&user_view_data=%5B%7B%22tid%22%3A%225774792876%22%2C%22duration%22%3A44%7D%2C%7B%22tid%22%3A%226004868076%22%2C%22duration%22%3A6%7D%5D&yuelaou_locate=110141%234%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=E6D107C3D823E719A12CE88A70089A86&stErrorNums=1&stMethod=1&stMode=1&stSize=805&stTime=334&stTimesNum=1&st_type=personalize_page&tid=6044544877&timestamp=1550997042355&user_view_data=%5B%7B%22tid%22%3A%226045484355%22%2C%22duration%22%3A3%7D%5D&yuelaou_locate=110142%236%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=3846C1F20E28D2992417425867F73D44&stErrorNums=1&stMethod=1&stMode=1&stSize=783&stTime=178&stTimesNum=1&st_type=personalize_page&tid=5992329065&timestamp=1550997285762&user_view_data=%5B%7B%22tid%22%3A%226044544877%22%2C%22duration%22%3A2%7D%5D&yuelaou_locate=110086%232%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=2A04B9CD66CA85236F7D179C8E37B8CB&stErrorNums=1&stMethod=1&stMode=1&stSize=807&stTime=491&stTimesNum=1&st_type=personalize_page&tid=6044744640&timestamp=1550997289166&user_view_data=%5B%5D&yuelaou_locate=110142%234%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=D2D32FD466DEAA5D0C37E2D4B1530364&stErrorNums=1&stMethod=1&stMode=1&stSize=808&stTime=357&stTimesNum=1&st_type=personalize_page&tid=6040258720&timestamp=1550997292387&user_view_data=%5B%7B%22tid%22%3A%226044744640%22%2C%22duration%22%3A1%7D%5D&yuelaou_locate=110086%236%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=162E3C05653BD7D761B160BD2AE99340&stErrorNums=1&stMethod=1&stMode=1&stSize=803&stTime=206&stTimesNum=1&st_type=personalize_page&tid=6046228382&timestamp=1550997295658&user_view_data=%5B%7B%22tid%22%3A%226040258720%22%2C%22duration%22%3A1%7D%5D&yuelaou_locate=110143%238%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=6AA5EB4605CBBB3CBB96A3C0572358E2&stErrorNums=1&stMethod=1&stMode=1&stSize=802&stTime=112&stTimesNum=1&st_type=personalize_page&tid=6045433002&timestamp=1550997336308&user_view_data=%5B%7B%22tid%22%3A%226044629816%22%2C%22duration%22%3A2%7D%5D&yuelaou_locate=110141%2312%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=9F09E2BE28599D1D4A0C7C2F4461B568&stErrorNums=1&stMethod=1&stMode=1&stSize=808&stTime=292&stTimesNum=1&st_type=personalize_page&tid=5992519630&timestamp=1550997339287&user_view_data=%5B%7B%22tid%22%3A%226045433002%22%2C%22duration%22%3A0%7D%5D&yuelaou_locate=110086%2314%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=B5B440E9E1A8DAB3A3C21552847CB98E&stErrorNums=1&stMethod=1&stMode=1&stSize=804&stTime=307&stTimesNum=1&st_type=personalize_page&tid=6044623941&timestamp=1550997344335&user_view_data=%5B%7B%22tid%22%3A%225992519630%22%2C%22duration%22%3A0%7D%5D&yuelaou_locate=110142%2316%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=09E1FC1DB7794D4A5E8D25ABADB44848&stErrorNums=1&stMethod=1&stMode=1&stSize=804&stTime=336&stTimesNum=1&st_type=personalize_page&tid=6045708433&timestamp=1550997347678&user_view_data=%5B%7B%22tid%22%3A%226044623941%22%2C%22duration%22%3A0%7D%5D&yuelaou_locate=110141%2318%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=E9597648D521ECED968D0C99FD8CDC38&stErrorNums=1&stMethod=1&stMode=1&stSize=802&stTime=320&stTimesNum=1&st_type=personalize_page&tid=6002034186&timestamp=1550997351773&user_view_data=%5B%7B%22tid%22%3A%226045708433%22%2C%22duration%22%3A0%7D%5D&yuelaou_locate=110086%2320%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=F6B60129E17603EF7C5E08797A5C3B82&stErrorNums=1&stMethod=1&stMode=1&stSize=803&stTime=274&stTimesNum=1&st_type=personalize_page&tid=6023279358&timestamp=1550997356394&user_view_data=%5B%7B%22tid%22%3A%226002034186%22%2C%22duration%22%3A2%7D%5D&yuelaou_locate=110086%2322%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=E489CC26BBB52FE409F447359F475FA8&stErrorNums=1&stMethod=1&stMode=1&stSize=804&stTime=323&stTimesNum=1&st_type=personalize_page&tid=6004696414&timestamp=1550997359792&user_view_data=%5B%7B%22tid%22%3A%226023279358%22%2C%22duration%22%3A1%7D%5D&yuelaou_locate=110086%2324%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=B7F80DBFBBBDD3DD07B797BA7C5589BE&stErrorNums=1&stMethod=1&stMode=1&stSize=807&stTime=586&stTimesNum=1&st_type=personalize_page&tid=6038591236&timestamp=1550997362811&user_view_data=%5B%5D&yuelaou_locate=110086%2326%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=A678B876797EB8FEDE5F517F80A4B0AE&stErrorNums=1&stMethod=1&stMode=1&stSize=803&stTime=109&stTimesNum=1&st_type=personalize_page&tid=6025031874&timestamp=1550997367069&user_view_data=%5B%7B%22tid%22%3A%226038591236%22%2C%22duration%22%3A0%7D%5D&yuelaou_locate=110086%2328%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=FC1A0CB6E3B3265A5F66BF3B879872C5&stErrorNums=1&stMethod=1&stMode=1&stSize=803&stTime=547&stTimesNum=1&st_type=personalize_page&tid=6032126956&timestamp=1550997370734&user_view_data=%5B%5D&yuelaou_locate=110086%2330%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=0420C6A07E71BA2DF74B5CC9AE8CB867&stErrorNums=1&stMethod=1&stMode=1&stSize=804&stTime=348&stTimesNum=1&st_type=personalize_page&tid=6025432206&timestamp=1550997374935&user_view_data=%5B%5D&yuelaou_locate=110086%2332%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=9BBDA0133099BFE1E7DA78159D95DB11&stErrorNums=1&stMethod=1&stMode=1&stSize=804&stTime=471&stTimesNum=1&st_type=personalize_page&tid=6034087601&timestamp=1550997379623&user_view_data=%5B%5D&yuelaou_locate=110086%2334%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=645B26BE65B5A95D33C90D02D3EF6C28&stErrorNums=1&stMethod=1&stMode=1&stSize=804&stTime=600&stTimesNum=1&st_type=personalize_page&tid=6045720032&timestamp=1550997396943&user_view_data=%5B%7B%22tid%22%3A%226034087601%22%2C%22duration%22%3A1%7D%5D&yuelaou_locate=110141%2346%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=75B81174BA73F04D5DC45455F15CD179&stErrorNums=1&stMethod=2&stMode=1&stSize=673&stTime=207&stTimesNum=1&st_type=personalize_page&tid=6045608244&timestamp=1550997751207&user_view_data=%5B%5D&yuelaou_locate=110144%2348%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=FCFED372A8695A2B3DA5DD45310E58C4&stErrorNums=1&stMethod=1&stMode=1&stSize=804&stTime=171&stTimesNum=1&st_type=personalize_page&tid=6045414620&timestamp=1550997759869&user_view_data=%5B%7B%22tid%22%3A%226045608244%22%2C%22duration%22%3A1%7D%5D&yuelaou_locate=110086%2354%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=7217172F6857CEFD18A7DEC300326F95&stErrorNums=1&stMethod=1&stMode=1&stSize=804&stTime=191&stTimesNum=1&st_type=personalize_page&tid=6041094078&timestamp=1550997763425&user_view_data=%5B%7B%22tid%22%3A%226045414620%22%2C%22duration%22%3A1%7D%5D&yuelaou_locate=110086%2355%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=8E4F8AF7732C5D9711492FC6B60E2540&stErrorNums=1&stMethod=1&stMode=1&stSize=806&stTime=312&stTimesNum=1&st_type=personalize_page&tid=6046270767&timestamp=1550997766543&user_view_data=%5B%7B%22tid%22%3A%226041094078%22%2C%22duration%22%3A0%7D%5D&yuelaou_locate=110143%2357%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=FDFE4448087E76BA82F174B9399FCF4E&stErrorNums=1&stMethod=1&stMode=1&stSize=804&stTime=461&stTimesNum=1&st_type=personalize_page&tid=6046247927&timestamp=1550997770073&user_view_data=%5B%7B%22tid%22%3A%226046270767%22%2C%22duration%22%3A1%7D%5D&yuelaou_locate=110141%2359%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=D84DB847EC3912600F1522B106D93A39&stErrorNums=1&stMethod=1&stMode=1&stSize=803&stTime=170&stTimesNum=1&st_type=personalize_page&tid=6034087291&timestamp=1550997778680&user_view_data=%5B%7B%22tid%22%3A%226046247927%22%2C%22duration%22%3A0%7D%5D&yuelaou_locate=110086%2364%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=01570415190E052965C7384D23F301E1&stErrorNums=1&stMethod=1&stMode=1&stSize=803&stTime=498&stTimesNum=1&st_type=personalize_page&tid=6046221467&timestamp=1550997784388&user_view_data=%5B%7B%22tid%22%3A%226034087291%22%2C%22duration%22%3A0%7D%5D&yuelaou_locate=110143%2368%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=BA87F3D3DF82621375E53B9DEB5BAEF6&stErrorNums=1&stMethod=1&stMode=1&stSize=804&stTime=285&stTimesNum=1&st_type=personalize_page&tid=6039582334&timestamp=1550997794811&user_view_data=%5B%7B%22tid%22%3A%226046221467%22%2C%22duration%22%3A1%7D%5D&yuelaou_locate=110086%2374%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
    '_client_id=wappc_1550927549543_367&_client_type=2&_client_version=9.9.8.42&_phone_imei=863100036804080&call_from=client_index&cuid=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_galaxy2=B3088C2A62F38E3846E34328BFB847CE%7C0&cuid_gid=&from=mini_1092a&model=Redmi+Note+4&net_type=1&pn=1&sign=16F2246DE5923B05D294CB207CC299AD&stErrorNums=1&stMethod=1&stMode=1&stSize=804&stTime=148&stTimesNum=1&st_type=personalize_page&tid=6046042866&timestamp=1550997798412&user_view_data=%5B%5D&yuelaou_locate=110141%2376%23ui_normal%2Cmsd_normal%2Ctw_tag_21%2Cvideo_tag_134%2Clive_normal',
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
        if 'list' in json_obj:
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
                        # print(videoUrl)
                        try:
                            urllib.request.urlretrieve(videoUrl, fileName)
                            print('下载成功')
                            print('暂停3秒')
                            time.sleep(3)
                        except:
                            print('下载失败')
                            print('暂停3秒')
                            time.sleep(3)
                            continue
        else:
            print('视频数据为空')
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


