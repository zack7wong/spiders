#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import re
from lxml.etree import HTML

def start():
    id_list = []
    url = 'http://1.189.191.146:8000/eMonPubHLJ/Default.aspx'
    response = requests.get(url)
    # print(response.text)
    html = HTML(response.text)
    links = html.xpath('//map[@id="Map"]/area/@href')

    urls = html.xpath('//div[@id="ctl00_ctl00_cphMain_cphMainPage_TreeView1"]//table//a[@target="_blank"]/@href')
    titles = html.xpath('//div[@id="ctl00_ctl00_cphMain_cphMainPage_TreeView1"]//table//a[@target="_blank"]/font/text()')

    print(urls)
    print(len(urls))
    print(titles)
    print(len(titles))

    for url,title in zip(urls,titles):
        saveurl = 'http://1.189.191.146:8000/eMonPubHLJ/'+url
        saveRes = saveurl+','+title+'\n'
        print(saveRes)
        if saveurl not in id_list:
            with open('helongjiang_id.txt','a') as f:
                f.write(saveRes)
            id_list.append(saveurl)


    for url11 in links:
        print(url11)
        link = 'http://1.189.191.146:8000/eMonPubHLJ/'+url11
        response = requests.get(link)
        html = HTML(response.text)

        urls = html.xpath('//div[@id="ctl00_ctl00_cphMain_cphMainPage_TreeView1"]//table//a[@target="_blank"]/@href')
        titles = html.xpath('//div[@id="ctl00_ctl00_cphMain_cphMainPage_TreeView1"]//table//a[@target="_blank"]/font/text()')
        print(urls)
        print(len(urls))
        print(titles)
        print(len(titles))

        for url, title in zip(urls, titles):
            saveurl = 'http://1.189.191.146:8000/eMonPubHLJ/' + url
            saveRes = saveurl + ',' + title + '\n'
            if saveurl not in id_list:
                with open('helongjiang_id.txt', 'a') as f:
                    f.write(saveRes)
                id_list.append(saveurl)

if __name__ == '__main__':
    start()