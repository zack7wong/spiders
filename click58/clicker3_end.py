#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from lxml.etree import HTML
import re
import requests
import json
import time
from requests import RequestException

account_list = []

#IP_URL = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=76e61e3813bd4db29d4374c6edbe7720&orderno=YZ201811220862kmEuoK&returnType=2&count=1'


def get_ip(url):
    print('正在获取IP。。')
    try:
        response = requests.get(url)
        if response.status_code == 200:
            res_json = json.loads(response.text)
            if res_json['ERRORCODE'] == '0':
                ip = res_json['RESULT'][0]['ip']
                port = res_json['RESULT'][0]['port']
                ip_res = ip + ':' + port
                print('获取IP成功，当前IP为：', str(ip_res))
                return ip_res
            elif res_json['ERRORCODE'] == '10036' or res_json['ERRORCODE'] == '10038' or res_json[
                'ERRORCODE'] == '10055':
                print('提前IP过快，5秒后重新请求', res_json)
                time.sleep(5)
                return get_ip(url)
            else:
                print('未知错误，5秒后重新请求', res_json)
                time.sleep(5)
                return get_ip(url)
    except RequestException:
        print('请求IP_url出错，正在重新请求', url)
        time.sleep(5)
        return get_ip(url)


def get_driver(ip):
    desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
    desired_capabilities["pageLoadStrategy"] = "none"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=' + ip)
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(
        chrome_options=chrome_options
    )
    driver.set_page_load_timeout(50)
    return driver


def start(ip, not_click_tilte_list):
    url = 'https://km.58.com/daibanguohu/'
    driver = get_driver(ip)

    try:
        driver.get(url)
        time.sleep(30)
        
    except:
        print('首页加载异常')
        driver.execute_script('window.stop()')
        driver.delete_all_cookies()
        driver.close()
        driver.quit()
        return 0

    # WebDriverWait(driver, 15, 0.5).until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, '#jingzhun')))
    html_str = driver.page_source
    html = HTML(html_str)
    #table_res = html.xpath('//div[@id="infolist"]/table[1]//tr[@class="ac_item"]')
    for i in range(1,2):
        table_num = str(i)
        table_res = html.xpath('//div[@id="infolist"]/table['+table_num+']//tr')
        for num in range(1, len(table_res) + 1,2):
            title_xpath = 'string(//div[@id="infolist"]/table['+table_num+']//tr[{num}]/td[2]//div[@class="tdiv"]/a/text())'.format(num=num)
            title = html.xpath(title_xpath).replace('\n', '').replace('\t', '').replace('\r', '').strip()
            if title not in not_click_tilte_list:
                print(title)
                #click_xpath = '//div[@id="infolist"]/table[1]//tr[@class="ac_item"][{num}]/td[2]//div[@class="tdiv"]/a'.format(num=num)
                click_xpath = '//div[@id="infolist"]/table['+table_num+']//tr[{num}]/td[2]//div[@class="tdiv"]/a'.format(num=num)
                ip = get_ip(IP_URL)
                driver = get_driver(ip)
                try:
                    driver.get(url)
                    time.sleep(30)
                    driver.find_element_by_xpath(click_xpath).click()
                    print('等待4分钟。。。')
                    time.sleep(240)
                    driver.delete_all_cookies()
                    driver.close()
                    driver.quit()
                except:
                    print('加载异常')
                    driver.execute_script('window.stop()')
                    driver.delete_all_cookies()
                    driver.close()
                    driver.quit()
                    continue


    print('该轮浏览完毕')


if __name__ == '__main__':
    print('程序开始运行。。。')
    with open('标题.txt') as f:
        not_click_tilte = f.read().strip().replace('\r','')
    not_click_tilte_list = not_click_tilte.split(',')
    print('当前标题：'+str(not_click_tilte_list))
    while True:
        print('\n新的一轮开始。。。')
        with open('讯代理.txt') as f:
            IP_URL = f.read()
        ip = get_ip(IP_URL)
        start(ip, not_click_tilte_list)
