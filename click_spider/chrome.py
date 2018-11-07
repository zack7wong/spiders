#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import download
import config
import re
import time
import random
from lxml.etree import HTML
from lxml import etree
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Chrome(object):
    def __init__(self):
        self.driver = None
        self.urls = []

    def get_urlobj(self):
        with open('urls.txt') as f:
            results = f.readlines()
            for res in results:
                try:
                    keyword = res.split(',')[0]
                    url = res.split(',')[1].strip()
                    url_obj = {
                        'url': url,
                        'keyword': keyword,
                    }
                    self.urls.append(url_obj)
                except:
                    print('该行文本格式有误')
                    print(res)
                    with open('failed_urls.txt','a') as ff:
                        ff.write(res)


    def get_driver(self):
        # width = config.width
        # height = config.height
        # # 执行路径
        # executable_path = r'E:\phantomjs.exe'
        #
        # dcap = dict(DesiredCapabilities.PHANTOMJS)
        # dcap["phantomjs.page.settings.userAgent"] = (
        #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 "
        # )
        #
        # driver = webdriver.PhantomJS(executable_path=executable_path, desired_capabilities=dcap)
        # # 界面宽度
        # driver.set_window_size(width=width, height=height)
        # # 设置超时
        # driver.set_page_load_timeout(15)
        self.driver = webdriver.Chrome()

    def search(self, url_obj):
        WebDriverWait(self.driver, 15, 0.5).until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, config.c_s)))
        self.driver.find_element_by_css_selector('#kw').send_keys(url_obj['keyword'])
        self.driver.find_element_by_css_selector('#su').click()
        time.sleep(2)
        self.parse_html(url_obj)

    def parse_html(self, url_obj):
        flag =False
        pageToken=1
        while True:
            print('当前页数： ' + str(pageToken))
            if pageToken == 1:
                 cssToken = pageToken + 1
            elif pageToken >=7:
                cssToken = 8
            else:
                cssToken = pageToken + 2
            pageToken += 1

            time.sleep(2)
            html_str = self.driver.page_source
            html = HTML(html_str)
            results = html.xpath('//div[@id="content_left"]/div')
            for res in results:
                detail_html_text = etree.tostring(res)
                search_parse = url_obj['url'] + '|' + url_obj['url'].replace('https://', '').replace('http://', '')
                detail_search_res = re.search(search_parse, detail_html_text.decode())
                if detail_search_res:
                    id_str = re.search('<div class="result c-container " id="(\d+)"', detail_html_text.decode())
                    if id_str:
                        if len(id_str.group(1)) == 1:
                            rank = id_str.group(1)
                            clickToken = id_str.group(1)[0] + ' '
                        else:
                            rank = id_str.group(1)[1]
                            clickToken = id_str.group(1)[0] + ' ' + id_str.group(1)[1]
                        print('已找到该网站，第' + str(pageToken) + '页,第' + rank +'条')
                        selecter_str = '#\\3{clickToken} > h3 > a'.format(clickToken=clickToken)
                        try:
                            WebDriverWait(self.driver, 5, 0.5).until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, selecter_str)))
                            self.driver.find_element_by_css_selector(selecter_str).click()
                            print('百度页面点击成功')
                        except:
                            print('百度页面点击异常')
                            return None
                        time.sleep(3)
                        print('开始随机点击网站。。')
                        self.random_click(url_obj)
                    flag = True
                    break

            if flag or pageToken >= 20:
                break

            #翻页
            css_selector = '#page > a:nth-child({cssToken})'.format(cssToken=str(cssToken))
            WebDriverWait(self.driver, 5, 0.5).until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))
            self.driver.find_element_by_css_selector(css_selector).click()

    def random_click(self,url_obj):
        html_str = requests.get(url_obj['url']).text
        # html_str = self.driver.page_source
        find_res = re.findall('<a.*?href="(.*?)"', html_str)
        print(find_res)
        click_res = random.sample(find_res, 3)
        for click in click_res:
            if click[0:4] == 'http':
                url = click
            else:
                if url_obj['url'][-1] == '/':
                    domain = url_obj['url'][:-1]
                else:
                    domain = url_obj['url']
                url = domain + click

            print(url)
            self.driver.get(url)
            time.sleep(5)

