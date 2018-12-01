#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.proxy import *
from selenium import webdriver
from lxml.etree import HTML
import re
import requests
import json
import time
from requests import RequestException

account_list = []

IP_URL ='http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=76e61e3813bd4db29d4374c6edbe7720&orderno=YZ201811220862kmEuoK&returnType=2&count=1'


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
    # myProxy = ip
    # proxy = Proxy({
    #     'proxyType': ProxyType.MANUAL,
    #     'httpProxy': myProxy,
    #     'ftpProxy': myProxy,
    #     'sslProxy': myProxy,
    #     'noProxy': ''
    # })
    # driver = webdriver.Firefox(proxy=proxy)

    agent_IP = ip.split(':')[0]
    agent_Port = ip.split(':')[1]
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.share_proxy_settings", True)
    profile.set_preference("network.http.use-cache", False)
    profile.set_preference("network.proxy.http", agent_IP)
    profile.set_preference("network.proxy.http_port", int(agent_Port))
    profile.set_preference('network.proxy.ssl_port', int(agent_Port))
    profile.set_preference('network.proxy.ssl', agent_IP)
    profile.set_preference("general.useragent.override", "whater_useragent")
    profile.update_preferences()
    driver = webdriver.Firefox(firefox_profile=profile)

    return driver

def start(ip,not_click_tilte_list):
    try:
        url = 'https://km.58.com/daibanguohu/'
        driver = get_driver(ip)
        driver.get(url)

        WebDriverWait(driver, 15, 0.5).until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, '#jingzhun')))
        html_str = driver.page_source
        html = HTML(html_str)
        table_res = html.xpath('//div[@id="infolist"]/table[1]//tr[@class="ac_item"]')
        for num in range(1, len(table_res)+1):
            title_xpath = 'string(//div[@id="infolist"]/table[1]//tr[@class="ac_item"][{num}]/td[2]//div[@class="tdiv"]/a/text())'.format(num=num)
            title = html.xpath(title_xpath).replace('\n','').replace('\t','').replace('\r','').strip()
            if title not in not_click_tilte_list:
                print(title)
                click_xpath = '//div[@id="infolist"]/table[1]//tr[@class="ac_item"][{num}]/td[2]//div[@class="tdiv"]/a'.format(num=num)
                ip = get_ip(IP_URL)
                driver = get_driver(ip)
                driver.get(url)
                driver.find_element_by_xpath(click_xpath).click()
                print('等待2分钟。。。')
                time.sleep(120)
                driver.delete_all_cookies()
                driver.close()
                driver.quit()
        print('该轮浏览完毕')
    except:
        print('未知错误')


if __name__ == '__main__':
    print('程序开始运行。。。')
    not_click_tilte = input('请输入不点击的标题名称：')
    not_click_tilte_list = not_click_tilte.split(',')
    while True:
        print('\n新的一轮开始。。。')
        ip = get_ip(IP_URL)
        start(ip,not_click_tilte_list)