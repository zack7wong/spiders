#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML

def start():
    with open('url.txt') as f:
        results = f.readlines()
        for res in results:
            try:
                url = res.strip()
                print(url)
                response = requests.get(url)
                # print(response.text)
                html = HTML(response.text)

                comName = html.xpath('string(//table[1]//tr[2]/td[2])').replace('\n', '').replace('\r', '').replace('\t', ' ').strip()
                comAddress = html.xpath('string(//table[1]//tr[3]/td[2])').replace('\n', '').replace('\r', '').replace('\t', ' ').strip()
                positionName = html.xpath('string(//table[2]//tr[2]/td[2])').replace('\n', '').replace('\r', '').replace('\t', ' ').strip()
                jobType = html.xpath('string(//table[2]//tr[2]/td[4])').replace('\n', '').replace('\r', '').replace('\t', ' ').strip()
                zhize = html.xpath('string(//table[2]//tr[9]/td[2])').replace('\n', '').replace('\r', '').replace('\t', ' ').strip()
                price = html.xpath('string(//table[2]//tr[5]/td[4])').replace('\n', '').replace('\r', '').replace('\t', ' ').strip()

                save_res = comName + '||' + comAddress + '||' + positionName + '||' + jobType + '||' + zhize + '||' + price + '\n'
                save_res = save_res.replace(',', '，').replace('||', ',')
                print(save_res)
                with open('岗位信息.csv', 'a', encoding='gbk', errors='ignore') as f:
                    f.write(save_res)
            except:
                print('error...'+str(res))
                continue
if __name__ == '__main__':
    with open('岗位信息.csv','w',encoding='gbk') as f:
        f.write('企业名称,企业地点,岗位名称,工作类型,岗位职责,薪资水准\n')
    start()