#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
from lxml.etree import HTML

def start():
    for i in range(1,50):
        print('当前页：'+str(i))
        start_url = 'http://esf.hu.tmsf.com/webty/WebFyAction_getGpxxSelectList.jspx'
        body = 'wtcsjg=&jzmj=&hxs=&cqid=&ordertype=&fwyt=&havepic=&starttime=&endtime=&keywords=&page={pageToken}&xqid=0'
        data = body.format(pageToken=i)
        response = requests.post(start_url,data=data)
        print(response.text)

        json_obj = json.loads(response.text)
        for item in json_obj['list']:
            gpfyid = str(item['gpfyid'])
            fwtybh = str(item['fwtybh'])
            url = 'http://esf.hu.tmsf.com/webty/WebFyAction_toGpxxInfo.jspx?gpfyid={gpfyid}&fwtybh={fwtybh}'.format(gpfyid=gpfyid,fwtybh=fwtybh)
            response = requests.get(url)
            html = HTML(response.text)

            louceng = html.xpath('string(//div[@id="fyxx_top"]/div[1]/div[1]/span[@class="f_grey3"])')
            chaoxiang = html.xpath('string(//div[@id="fyxx_top"]/div[2]/div[1]/span[@class="f_grey3"])')
            mianji = html.xpath('string(//div[@id="fyxx_top"]/div[2]/div[2]/span[@class="f_grey3"])')
            xiaoqu = html.xpath('string(//div[@id="fyxx_top"]/div[3]/div[1]/span[@class="f_grey3"])')
            chengqu = html.xpath('string(//div[@id="fyxx_top"]/div[4]/div[1]/span[@class="f_grey3"])')
            qiye = html.xpath('string(//div[@class="fy_detail_company_content"]/ul/li/a)')
            miaoshu = html.xpath('string(//div[@class="fy_detail_text"])').strip()

            save_res = url + '||' + louceng + '||' + chaoxiang + '||' + mianji + '||' + xiaoqu + '||' + chengqu + '||' + qiye + '||' + miaoshu
            print(save_res)
            save_res = save_res.replace('\n', '').replace(',', '，').replace('||', ',') + '\n'
            with open('二手房.csv', 'a', encoding='gbk', errors='ignore') as f:
                f.write(save_res)


if __name__ == '__main__':
    with open('二手房.csv', 'w', encoding='gbk', errors='ignore') as f:
        f.write('链接,楼层,朝向,面积,小区,城区,经纪企业,描述\n')
    start()