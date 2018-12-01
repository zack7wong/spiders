#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     test
   Description :
   Author :        hayden_huang
   Date：          2018/11/29 21:44
-------------------------------------------------
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

def get_driver():
    """
    :return: 此处调节driver参数
    """
    # 执行路径
    # executable_path = r'E:\phantomjs.exe'
    executable_path = '/usr/local/Cellar/phantomjs/2.1.1/bin/phantomjs'

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 "
    )

    driver = webdriver.PhantomJS(executable_path=executable_path, desired_capabilities=dcap)
    # driver = webdriver.PhantomJS(executable_path=executable_path)
    # 界面宽度
    # driver.set_window_size(width=width, height=height)
    # 设置超时
    driver.set_page_load_timeout(15)

    # Firefox
    # executable_path = r'E:\geckodriver.exe'
    # width = 3000
    # height = 3000
    # options = webdriver.FirefoxOptions()
    # options.headless = True
    # driver = webdriver.Firefox(executable_path=executable_path)
    # driver.set_window_size(width=width,height=height)
    return driver

# driver = get_driver()
# driver.get('view-source:https://www.amazon.com/s/ref=lp_16318981_nr_n_0?fst=as%3Aoff&rh=n%3A10329849011%2Cn%3A16310101%2Cn%3A%2116310211%2Cn%3A6506977011%2Cn%3A16318981%2Cn%3A724694011&bbn=10329849011&ie=UTF8&qid=1543497502&rnid=10329849011')
# time.sleep(10)
# print(driver.page_source)

import requests

url = "https://www.amazon.com/s/ref=lp_16318981_nr_n_0"

querystring = {"fst":"as%3Aoff","rh":"n%3A10329849011%2Cn%3A16310101%2Cn%3A%2116310211%2Cn%3A6506977011%2Cn%3A16318981%2Cn%3A724694011","bbn":"10329849011","ie":"UTF8","qid":"1543497502","rnid":"10329849011"}

payload = ""
headers = {
    'cache-control': "no-cache",
    'Postman-Token': "32ef783d-e29f-4727-88c2-6406c3b97566"
    }

proxies = {
    'https':'http://127.0.0.1:9999'
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring,proxies=proxies,verify=False,allow_redirects=False)

print(response.text)



import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://www.amazon.com/s/ref=lp_16318981_nr_n_0?fst=as%3Aoff&rh=n%3A10329849011%2Cn%3A16310101%2Cn%3A%2116310211%2Cn%3A6506977011%2Cn%3A16318981%2Cn%3A724694011&bbn=10329849011&ie=UTF8&qid=1543497502&rnid=10329849011'
        html = await fetch(session, url)
        print(html)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())