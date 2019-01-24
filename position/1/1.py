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

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Cookie': "JSESSIONID=3CB57BB367471402EA450917C189A6DB.IP8010",
    'Host': "jy.fosu.edu.cn",
    'Pragma': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "029cfacf-d506-4430-a44d-ba5832ab3ee9"
    }


id_list = []
def start():
    start_url = 'http://jy.fosu.edu.cn/eweb/wfc/app/pager.so?type=goPager&requestPager=pager&pageMethod=next&currentPage={pageToken}'
    for i in range(0,15):
        url = start_url.format(pageToken=i)
        print(url)
        response = requests.get(url,headers=headers)
        html = HTML(response.text)
        url_list = html.xpath('//div[@class="z_newsl"]/ul/li/div[1]/a/@onclick')
        # print(url_list)
        for item in url_list:
            id = re.search('viewZpxx\(\'(.*?)\'', item).group(1)
            if id in id_list:
                continue
            else:
                id_list.append(id)
            link = 'http://jy.fosu.edu.cn/eweb/jygl/zpfw.so?modcode=jygl_zpxxck&subsyscode=zpfw&type=viewZpxx&id='+id
            print(link)
            detail_response = requests.get(link,headers=headers)
            # print(detail_response.text)
            detail_html = HTML(detail_response.text)

            comName = detail_html.xpath('string(//table[@id="tab"][1]//td[@class="td_border_two"]/a/text())')
            comName = comName.replace('\n','').replace('\r','').replace('\t',' ').strip()

            tab_list = detail_html.xpath('//div[@class="z_content"]/table[@id="tab"]')
            title_list = detail_html.xpath('//div[@class="z_content"]/div[@class="bd_title"]/span/text()')
            for tab,title in zip(tab_list,title_list):
                comAddress = ''
                positionName = re.sub('职位\((\d+)\): ', '', title).replace('\n','').replace('\r','').replace('\t',' ').strip()
                jobType = tab.xpath('string(./tr[1]/td[4]/text())').replace('\n','').replace('\r','').replace('\t',' ').strip()
                zhize = tab.xpath('string(./tr[3]/td[2]/text())').replace('\n','').replace('\r','').replace('\t',' ').strip()
                price = tab.xpath('string(./tr[2]/td[6]/text())').replace('\n','').replace('\r','').replace('\t',' ').strip()

                print(comName,comAddress,positionName,jobType,zhize,price)
                save_res = comName+'||'+comAddress+'||'+positionName+'||'+jobType+'||'+zhize+'||'+price+'\n'
                save_res = save_res.replace(',','，').replace('||',',')
                with open('岗位信息.csv', 'a', encoding='gbk',errors='ignore') as f:
                    f.write(save_res)

if __name__ == '__main__':
    with open('岗位信息.csv','w',encoding='gbk') as f:
        f.write('企业名称,企业地点,岗位名称,工作类型,岗位职责,薪资水准\n')
    start()