#!/usr/bin/env python
# -*- coding:utf-8 -*-

import download
import json
import re
import os
import config
import time
from lxml.etree import HTML

RESULTS_LIST = []
bodong = ''

def start(pageToken,start_url):
    body = config.BODY.format(pageToken=pageToken)
    response = download.get_html(start_url,'post',body=body)
    html = HTML(response.text)
    results = html.xpath('//table[@class="gridview"]//tr/td[2]/text()')
    if pageToken == '1':
        global bodong
        bodong = results[0]

    for res in results:
        RESULTS_LIST.append(res)

def parse_html(results):
    ab_list = []
    ac_list = []
    bc_list = []
    for res in results:
        ab = res.split(',')[2][:2]
        ac = res.split(',')[2][0]+res.split(',')[2][2]
        bc = res.split(',')[2][1:3]
        if len(list(set(ab_list))) < 90:
            ab_list.append(ab)
        if len(list(set(ac_list))) < 90:
            ac_list.append(ac)
        if len(list(set(bc_list))) < 90:
            bc_list.append(bc)
        # print('波动值为：'+res + '  ab：'+ ab + '  ac：'+ ac + '  bc：'+ bc)

    ab_list = list(set(ab_list))
    ac_list = list(set(ac_list))
    bc_list = list(set(bc_list))
    #
    # print('ab:'+str(ab_list))
    # print('ac:'+str(ac_list))
    # print('bc:'+str(bc_list))
    # print('\n')

    abx_list = []
    axc_list = []
    xbc_list = []
    for i in range(10):
        for ab in ab_list:
            abx = ab + str(i)
            abx_list.append(abx)

    for i in range(10):
        for ac in ac_list:
            axc = ac[0] + str(i) + ac[1]
            axc_list.append(axc)

    for i in range(10):
        for bc in bc_list:
            xbc = str(i)+bc
            xbc_list.append(xbc)

    # print("abx: "+ str(abx_list))
    # print("abx长度为：" + str(len(abx_list)))
    # print("axc: "+ str(axc_list))
    # print("axc长度为：" + str(len(axc_list)))
    # print("xbc: "+ str(xbc_list))
    # print("xbc长度为：" + str(len(xbc_list)))
    # print('\n')
    intersecti_list = []
    for intersecti in abx_list:
        if intersecti in axc_list and intersecti in xbc_list:
            intersecti_list.append(intersecti)

    old_num_list = []
    try:
        with open('results.txt') as f:
            results = f.readlines()
            for res in results:
                num = res.split(' ')
                old_num_list = old_num_list + num
    except:
        pass

    zhongjiang = bodong[-3:]
    if zhongjiang in old_num_list:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '  最新波动值为：' + bodong + '  中奖！')
    else:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '  最新波动值为：' + bodong + '  未中奖')

    # print('交集为：'+ str(intersecti_list))
    # print('交集长度为：'+ str(len(intersecti_list)))

    with open('results.txt','w') as f:
        for i in range(len(intersecti_list)):
            # print(intersecti_list[i], end=' ')
            f.write(intersecti_list[i]+' ')
            if (i + 1) % 10 == 0:
                # print('\n')
                f.write('\n')

def test_enough(results):
    ab_list = []
    ac_list = []
    bc_list = []
    for res in results:
        ab = res.split(',')[2][:2]
        ac = res.split(',')[2][0] + res.split(',')[2][2]
        bc = res.split(',')[2][1:3]
        if len(list(set(ab_list))) < 90:
            ab_list.append(ab)
        if len(list(set(ac_list))) < 90:
            ac_list.append(ac)
        if len(list(set(bc_list))) < 90:
            bc_list.append(bc)

        if len(list(set(ab_list)))>=90 and len(list(set(ac_list)))>=90 and len(list(set(ac_list)))>=90:
            return True

def run(start_url):
    for i in range(1,20):
        # print('当前页数: '+str(i))
        start(str(i),start_url)
        if test_enough(RESULTS_LIST):
            break

    parse_html(RESULTS_LIST)

if __name__ == '__main__':
    print('=============================')
    print('|| 正信在线稳定运营0污点打入市场||')
    print('|| 人人赚分红模式，人人不贴分红 || ')
    print('|| 日提500万大户必备平台之一   || ')
    print('|| 正信在线2筹备中敬请期待     || ')
    print('|| 在线咨询qq 6557397        || ')
    print('|| QQ 1757011479            || ')
    print('=============================')
    print('程序开始运行,请稍等。。。')
    download = download.Download()
    #初始化请求的链接
    response = download.get_html('http://www.77tj.org/')
    html = HTML(response.text)
    now = html.xpath('string(//table[@class="gridview"]//tr[2]/td[2])')

    mynow_url = config.START_URL
    body = config.BODY.format(pageToken='1')
    response = download.get_html(mynow_url, 'post', body=body)
    html = HTML(response.text)
    mynow = html.xpath('string(//table[@class="gridview"]//tr[2]/td[2])')

    if mynow == now:
        start_url = config.START_URL
    else:
        start_url = config.START_URL2

    while True:
        if int(time.time()) % 60 == 0:
            run(start_url)
            RESULTS_LIST.clear()
            time.sleep(1)