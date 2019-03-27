#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import download
from lxml.etree import HTML

def start():
    try:
        with open('讯代理.txt') as f:
            IP_URL = f.read().strip()
    except:
        print('缺失文件，请在当前目录下创建 讯代理.txt')
        time.sleep(40000000)

    while True:
        try:
            useProxy = input('是否使用代理ip ([1].使用  [2].不使用) ：')
            startNum = int(input('请输入起始数字：'))
            endNum = int(input('请输入末尾数字：'))
            if endNum < startNum:
                print('末尾数字小于起始数字，请重新输入')
                continue
            break
        except:
            print('请输入数字！！')
            continue



    for i in range(startNum,endNum+1):
        try:
            print('当前数字：'+str(i))
            url = 'http://shanzhunet.com/mp/'+str(i)
            if useProxy == '1':
                response = down.get_html(url, proxy=True, IP_URL=IP_URL)
            else:
                response = down.get_html(url, proxy=False, IP_URL=IP_URL)

            if response:
                # print(response.text)
                html = HTML(response.text)
                #姓名 电话 地址  公司 职位 是否VIP
                name = html.xpath('string(//h1[@class="uname"]/text())')
                phone = html.xpath('string(//span[@id="telD"]/text())')
                allInfo = html.xpath('string(//div[@class="userinfo"]/p/text())').strip()
                address = allInfo.split('|')[1]
                company = allInfo.split('|')[0].split(' ')[0]
                position = allInfo.split('|')[0].split(' ')[1]
                vip = html.xpath('string(//input[@id="vip"]/@value)')

                print(name,phone,address,company,position,vip)
                savr_res = str(i)+','+name+','+phone+','+address+','+company+','+position+','+vip+'\n'
                with open('结果.csv','a',encoding='gbk',errors='ignore') as f:
                    f.write(savr_res)
        except:
            print('未知错误')




if __name__ == '__main__':
    with open('结果.csv', 'w', encoding='gbk', errors='ignore') as f:
        f.write('id,姓名,电话,地址,公司,职位,是否vip\n')

    down = download.Download()
    start()