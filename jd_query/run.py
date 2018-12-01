#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     run
   Description :
   Author :        hayden_huang
   Date：          2018/11/23 15:25
-------------------------------------------------
"""

import download
import time
import requests
import config
import json
import math
from lxml.etree import HTML
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def start(kw):
    try:
        oldone_date = time.time() - 86400*30
        startDate = time.strftime('%Y-%m-%d', time.localtime(oldone_date))
        oldmonth_date = time.time() - 86400
        endDate = time.strftime('%Y-%m-%d', time.localtime(oldmonth_date))
        url = 'https://sz.jd.com/industryKeyWord/getIndustrySummDataTrend.ajax?channel=2&date=30{endDate}&endDate={endDate}&kw={kw}&startDate={startDate}'.format(startDate=startDate,endDate=endDate,kw=kw)
        response = requests.get(url,headers=config.HEADERS,timeout=10)
        json_obj = json.loads(response.text)
        avg = round(json_obj['content']['series'][0]['avg'])

        chengjiao_url = 'https://sz.jd.com/industryKeyWord/getKeywordsSummData.ajax?channel=2&date=30{endDate}&endDate={endDate}&kw={kw}&startDate={startDate}'.format(startDate=startDate,endDate=endDate,kw=kw)
        chengjiao_response = requests.get(chengjiao_url, headers=config.HEADERS,timeout=10)
        chengjiao_json_obj = json.loads(chengjiao_response.text)
        chengjiao = chengjiao_json_obj['content']['ConvertRate']['value']
        chengjiao =  str("%.2f"%(float(chengjiao)*100))+'%'

        jd_url = 'https://search.jd.com/Search?keyword={kw}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.his.0.0&psort=3&click=0'.format(kw=kw)
        jd_response = requests.get(jd_url,timeout=10)
        jd_response.encoding = 'utf8'
        html = HTML(jd_response.text)
        jd = html.xpath('string(//span[@id="J_resCount"])')

        #占比
        zhanbi_url = 'https://sz.jd.com/industryKeyWord/getCategoryDistribution.ajax?channel=2&date={startDate}&endDate={endDate}&kw={kw}&startDate={startDate}'.format(startDate=startDate,endDate=endDate,kw=kw)
        zhanbi_response = requests.get(zhanbi_url, headers=config.HEADERS, timeout=10)
        zhanbi_json_obj = json.loads(zhanbi_response.text)
        item_list = ""
        for data in zhanbi_json_obj['content']['data']:
            name = data[0]
            value = data[1]
            value = str("%.2f" % (float(value) * 100)) + '%'
            item_list += name+':'+value+','


        print(kw +' 的平均指数是：'+str(avg)+' 成交转化率是：'+chengjiao+' 京东商品数：'+jd+' 分布：'+item_list)
        with open('results.csv','a') as f:
            write_res = kw+','+str(avg)+','+chengjiao+','+jd+','+item_list+'\n'
            f.write(write_res)
    except:
        print(kw+' 未知错误')
        with open('failed.txt','a') as f:
            write_res = kw+'\n'
            f.write(write_res)


if __name__ == '__main__':
    down = download.Download()
    with open('results.csv','w') as f:
        f.write('')
    with open('failed.txt','w') as f:
        f.write('')

    driver = webdriver.Chrome()
    url = 'https://sz.jd.com/login.html?ReturnUrl=http%3A%2F%2Fsz.jd.com%2FindustryKeyWord%2FkeywordQuerys.html'
    driver.get(url)

    # c_s = 'body > div.normal-body > div.header > div'
    # WebDriverWait(driver, 15, 0.5).until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, c_s)))
    # driver.find_element_by_css_selector('body > div.normal-body > div.header > div').click()
    #
    # login = 'body > div.login-form > div.login-tab.login-tab-r > a'
    # WebDriverWait(driver, 15, 0.5).until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, login)))
    # driver.find_element_by_css_selector('body > div.login-form > div.login-tab.login-tab-r > a').click()
    # time.sleep(1)
    # driver.find_element_by_css_selector('#loginname').send_keys('爱心软件')
    # driver.find_element_by_css_selector('#nloginpwd').send_keys('rj7866') #爱厘觅 dg8821

    print('请登录')
    flag = False
    while True:
        cookies = driver.get_cookies()
        for cookie in cookies:
            if cookie['name'] == 'thor':
                config.HEADERS['cookie'] = 'thor=' + cookie['value']
                print('已登录...')
                flag = True
                break
        if flag:
            break
        print('未检测到登录cookie。。')
        time.sleep(3)

    while True:
        kw = input('请输入要查询的关键词(如需批量请输入  all)：')
        if kw == 'all':
            with open('keyword.txt') as f:
                results = f.readlines()
                for res in results:
                    kw = res.strip()
                    start(kw)
        else:
            start(kw)