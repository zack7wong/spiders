#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
from lxml.etree import HTML
import re


def parse_detail(response):
    html = HTML(response.text)
    div_list = html.xpath('//div[@class="trade-list-contain j-list-content"]//div[@class="demand"]')
    for item in div_list:
        title = item.xpath('string(.//p[@class="d-title"]/span/@title)').strip()
        price = item.xpath('string(.//b[@class="d-base-price"]/text())').replace('￥','').strip()
        des = item.xpath('string(.//p[@class="d-des"]/@title)').strip()
        url = 'https:' + item.xpath('string(./a/@href)').strip()

        save_res = title+'||'+price+'||'+des+'||'+url
        save_res = save_res.replace(',','，').replace('\n','').replace('||',',')+'\n'
        print(save_res)

        with open('结果.csv', 'a', encoding='gbk', errors='ignore') as f:
            f.write(save_res)

def start(catid):
    start_url = 'https://task.zbj.com/'+catid
    print('正在爬取：'+start_url)
    response = requests.get(start_url)
    # print(response.text)
    html = HTML(response.text)

    #获取总页数
    totalPage = html.xpath('string(//span[@class="zbj-paging-text"]/text())')
    totalPage = re.search('共.*?，(\d+)页',totalPage)
    if totalPage:
        totalPage = int(totalPage.group(1))
        print('总页数：'+str(totalPage))
    else:
        totalPage = 1
        print('没有获取到总页数')


    #处理第一页内容
    print('当前页：1')
    parse_detail(response)

    # 处理后续页数
    if totalPage !=1:
        for i in range(2,totalPage+1):
            print('当前页：'+str(i))
            each_url = 'https://task.zbj.com/{catid}/page{pageToken}.html'.format(catid=catid,pageToken=i)
            response = requests.get(each_url)
            parse_detail(response)



if __name__ == '__main__':
    with open('结果.csv','w',encoding='gbk',errors='ignore') as f:
        f.write('标题,预算,项目描述,url\n')
    while True:
        catid = input('请输入要爬取的分类：')
        start(catid)