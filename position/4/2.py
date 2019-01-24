#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 佛山科学技术学院    http://jy.fosu.edu.cn/eweb/jygl/zpfw.so
# 云南师范大学商学院   http://yssxy.bibibi.net/
# 桂林理工大学  http://glut.doerjob.com/   招聘会 招聘信息
# 桂林理工大学博文学院   http://yunjy.bwgl.cn/module/careers
#
# 上海应用技术大学   http://job.sit.edu.cn/
#
# 上海第二工业大学   http://career.sspu.edu.cn/eweb/jygl/index.so?reurl=%2F%2Findex.jsp%3Fnull
# 上海理工大学  http://91.usst.edu.cn/
# 爬招聘信息，宣讲信息

# 宣讲信息：  企业名称 宣讲地点，宣讲时间 场地
# 岗位信息： 企业名称、企业地点、岗位名称、工作类型、岗位职责 薪资水准

import requests
from lxml.etree import HTML
import re
import json

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    # 'Cookie': "JSESSIONID=3CB57BB367471402EA450917C189A6DB.IP8010",
    # 'Host': "jy.fosu.edu.cn",
    'Pragma': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
}


id_list = []
def start():
    start_url = 'http://yunjy.bwgl.cn/module/getcareers?start={pageToken}&count=16&k=&address=&professionals=&career_type=&type=inner&day='
    for i in range(0, 2):
        url = start_url.format(pageToken=i * 15)
        response = requests.get(url)
        json_obj = json.loads(response.text)
        for data in json_obj['data']:
            comName = data['company_name']
            school_name = '桂林理工大学'
            meet_day = data['meet_day']
            address = data['address']

            save_res = comName + '||' + school_name + '||' + meet_day + '||' + address + '\n'
            save_res = save_res.replace(',', '，').replace('||', ',')
            print(save_res)
            with open('宣讲会.csv', 'a', encoding='gbk', errors='ignore') as f:
                f.write(save_res)

if __name__ == '__main__':
    with open('宣讲会.csv','w',encoding='gbk') as f:
        f.write('企业名称,宣讲地点,宣讲时间,宣讲场地\n')
    start()