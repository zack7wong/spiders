#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
from lxml.etree import HTML


driver = webdriver.Chrome()

account = 1

for i in range(1,11):
    url = "https://www.qidian.com/rank/fin?page="+str(i)
    driver.get(url)

    html = HTML(driver.page_source)
    titles = html.xpath('//div[@class="book-img-text"]//h4/a/text()')
    urls = html.xpath('//div[@class="book-img-text"]//h4/a/@href')
    authors = html.xpath('//div[@class="book-img-text"]//p[@class="author"]/a[1]/text()')
    mytypes = html.xpath('//div[@class="book-img-text"]//p[@class="author"]/a[2]/text()')
    intros = html.xpath('//div[@class="book-img-text"]//p[@class="intro"]/text()')
    mytimes = html.xpath('//div[@class="book-img-text"]//p[@class="update"]/span/text()')
    # dianjis = html.xpath('//div[@class="book-img-text"]//span[@class="qqIQdXrX"]/text()')

    # print(titles)
    # print(urls)
    # print(authors)
    # print(mytypes)
    # print(intros)
    # print(mytimes)
    # print(dianjis)
    for title,url,author,mytype,intro,mytime in zip(titles,urls,authors,mytypes,intros,mytimes):
        url = 'http:'+url
        intro = intro.replace('\n','').replace('\r','').replace(' ','')
        jieguo = str(account)+','+title+','+url+','+author+','+mytype+','+intro+','+mytime+'\n'
        print(jieguo)
        with open('jieguo.csv','a') as f:
            f.write(jieguo)
        account+=1