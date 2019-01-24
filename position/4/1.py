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
    start_url = 'http://yunjy.bwgl.cn/module/getjobs?start={pageToken}&count=16&k=&company_name=&city_name=&about_major=&degree_require=&type_id=-1&is_practice=0'
    for i in range(0,101):
        try:
            url = start_url.format(pageToken=i*15)
            print(url)
            response = requests.get(url,headers=headers)
            # print(response.text)
            json_obj = json.loads(response.text)
            for data in json_obj['data']:
                try:
                    id = data['publish_id']
                    detail_url = 'http://yunjy.bwgl.cn/detail/job?id='+str(id)
                    detail_response = requests.get(detail_url,headers=headers)
                    # print(detail_response.text)
                    comAddress = re.search('<img src=.*?center=(.*?)&',detail_response.text,re.S)
                    if comAddress:
                        comAddress = comAddress.group(1)
                    else:
                        comAddress = ''

                    url2 = 'http://yunjy.bwgl.cn/detail/getjobdetail?publish_id='+str(id)
                    res2 = requests.get(url2,headers=headers)
                    jsonObj2 = json.loads(res2.text)

                    # print(jsonObj2['data']['content'])
                    html2 = HTML(jsonObj2['data']['job_descript'])
                    zhizeList = html2.xpath('//p//text()')
                    zhize = ''.join(zhizeList).replace('\n', '').replace('\r', '').replace('\t', ' ').strip()

                    comName = data['company_name']
                    positionName = data['job_name']
                    jobType = '全职'
                    price = data['salary']

                    save_res = comName + '||' + comAddress + '||' + positionName + '||' + jobType + '||' + zhize + '||' + price + '\n'
                    save_res = save_res.replace(',', '，').replace('||', ',')
                    print(save_res)
                    with open('岗位信息.csv', 'a', encoding='gbk', errors='ignore') as f:
                        f.write(save_res)
                except:
                    continue
        except:
            continue

if __name__ == '__main__':
    with open('岗位信息.csv','w',encoding='gbk') as f:
        f.write('企业名称,企业地点,岗位名称,工作类型,岗位职责,薪资水准\n')
    start()