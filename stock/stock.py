#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     stock
   Description :
   Author :        hayden_huang
   Date：          2018/12/3 16:31
-------------------------------------------------
"""

import requests
import time
from lxml.etree import HTML
from lxml import etree
import datetime

def get_html(type):
    try:
        if type=='1':
            try:
                with open(filename, 'w') as f:
                    # f.write('symbol,size,price\n')
                    f.write('')
            except:
                print('初始化文件失败')

        item_list = []
        url = 'https://api.tmxmoney.com/mocimbalance/en/TSX/moc.html'
        proxies = {
            'https':'http://127.0.0.1:1087'
        }
        # response = requests.get(url,timeout=10,proxies=proxies)
        response = requests.get(url,timeout=10)
        if response.status_code == 200:
            html = HTML(response.text)
            results = html.xpath('//table[@class="tablemaster"]//tr')
            for res in results:
                detail_html_str = etree.tostring(res)
                detail_html = HTML(detail_html_str.decode())
                symbol = detail_html.xpath('string(//td[1]/a)')
                if symbol == '':
                    continue
                size = detail_html.xpath('string(//td[3])')
                price = detail_html.xpath('string(//td[4])')
                if type == '1':
                    print(symbol,size,price)
                    with open(filename,'a') as f:
                        save_res = symbol+','+size+','+price+'\n'
                        f.write(save_res)
                elif type =='2':
                    obj = {
                        'symbol':symbol,
                        'size':size,
                        'price':float(price),
                    }
                    item_list.append(obj)
            #价格分区
            if type =='2':
                sort_filename = 'sort_' + filename
                with open(sort_filename, 'w') as f:
                    # f.write('symbol,size,price\n')
                    f.write('')

                sort_res_list = sorted(item_list, key=lambda x: x['price'])
                for sort_res in sort_res_list:
                    symbol = sort_res['symbol']
                    size = sort_res['size']
                    price = str(sort_res['price'])
                    print(symbol, size, price)

                    with open(sort_filename,'a') as f:
                        save_res = symbol+','+size+','+price+'\n'
                        f.write(save_res)
        else:
            print('未获取到数据。。')
    except:
        print('未知错误。。')

def jisuan():
    print('正在读取历史数据...')
    symbol_list = []
    item_list = []
    file_num = 0
    for lishi_file in lishi_date_list:
        lishi_filename = lishi_file+'.csv'
        try:
            file_num += 1
            print('正在读取 '+lishi_file)
            with open(lishi_filename) as f:
                resutls = f.readlines()
                for res in resutls:
                    symbol = res.split(',')[0]
                    size = res.split(',')[1]

                    if symbol in symbol_list:
                        for item in item_list:
                            if symbol == item['key']:
                                item['value'].append(int(size))
                    else:
                        symbol_list.append(symbol)
                        item_list.append({'key':symbol,'value':[int(size)]})

        except:
            print(lishi_file+' 读取失败！')
            file_num -=1

    # print(item_list)
    print('已读取文件个数：'+ str(file_num))
    #获取当天数据
    print('正在获取当天数据。。')
    jisuan_list = []
    today_list = []
    url = 'https://api.tmxmoney.com/mocimbalance/en/TSX/moc.html'
    proxies = {
        'https': 'http://127.0.0.1:1087'
    }
    try:
        # response = requests.get(url, timeout=10, proxies=proxies)
        response = requests.get(url,timeout=10)
        if response.status_code == 200:
            html = HTML(response.text)
            results = html.xpath('//table[@class="tablemaster"]//tr')
            for res in results:
                detail_html_str = etree.tostring(res)
                detail_html = HTML(detail_html_str.decode())
                symbol = detail_html.xpath('string(//td[1]/a)')
                if symbol == '':
                    continue
                size = detail_html.xpath('string(//td[3])')
                price = detail_html.xpath('string(//td[4])')
                obj = {
                    'key': symbol,
                    'value': int(size),
                    'price':price
                }
                today_list.append(obj)
        else:
            print('获取当天数据失败。。')
            return None
    except:
        print('获取当天数据失败。。')
        return None

    print('正在历史数据计算平均数。。')
    for item in item_list:
        item['avg'] = sum(item['value']) / file_num


    with open('results.csv', 'w') as f:
        f.write('')
    for item in item_list:
        for today in today_list:
            if today['key'] == item['key']:
                save_res = today['key']+','+str(today['value'])+','+str(item['avg'])+','+str(today['value']/item['avg'])+','+today['price']+'\n'
                print(save_res)
                with open('results.csv','a') as f:
                    f.write(save_res)



if __name__ == '__main__':
    thisdate = time.strftime('%Y%m%d', time.localtime())

    lishi_date_list = []
    now = datetime.datetime.now()

    for i in range(14):
        date = now + datetime.timedelta(days=-(i+1))
        date = str(date).split(' ')[0].replace('-','')
        lishi_date_list.append(date)

    filename = thisdate + '.csv'

    while True:
        type = input('请输入要执行的功能 [1]获取当天数据，[2]获取当天数据并按价格分区，[3]历史10天数据计算：')
        if type == '1' or type == '2' :
            get_html(type)
        else:
            jisuan()

        print('10秒后关闭。。。')
        time.sleep(10)
        exit()