#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     test
   Description :
   Author :        hayden_huang
   Date：          2018/11/28 20:15
-------------------------------------------------
"""

import aiohttp
import asyncio
from lxml.etree import HTML
import re
import random
import config

detail_url_list = []
detail_url_list2 = []


HOST = 'https://www.amazon.com'
headers ={
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'cookie': 'session-id=134-7713137-0318165; ubid-main=134-1941950-8510221; x-wl-uid=1TQ5dHz9lotI7TJu+aSSZ3cWjhwQMBSdtiG1B26ZcHJVKXCrfmDxqyiv68htTrq3TUv6IOcombPQ=; session-id-time=2082787201l; session-token=k4dQGFWH5l9fzy8P50qdVGJOgG/tXtsya+aFp/60KBUmNyZ9KQnAwaT76c4DYKwhCbIfHo8HL+belb5LfQsEF/aBjUdQCJVZ8qjEh7d8WUIJ7XAWqU0rQReKUwNg5mUrh6DFvq1a0bvpLd+ohFitki/i3zvwANoydp2g8YLA77U7aERyE6+zjff+VAT5wkaV; csm-hit=adb:adblk_no&tb:05RDS2Y8BT07XZGM4NK8+b-70NP4EFN2PS0W9G4HXVG|1543498490326&t:1543410388180',
    'pragma': 'no-cache',
    'referer': 'https://www.amazon.com/s/ref=lp_2256164011_ex_n_1?rh=n%3A10329849011%2Cn%3A16310101%2Cn%3A%2116310211%2Cn%3A371469011&bbn=10329849011&ie=UTF8&qid=1543497206',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}

proxy_num = 0
myip = ''
proxy = ''

async def fetch(session, url):
    try:
        if config.proxy_on:
            global proxy_num,myip,proxy
            if proxy_num %15==0:
                myip = config.get_ip(config.proxy_url)
                proxy = 'http://'+myip
            proxy_num += 1
            async with session.get(url,headers=headers,timeout=10,proxy=proxy) as response:
                return await response.text()
        else:
            async with session.get(url,headers=headers,timeout=10) as response:
                return await response.text()
    except:
        return None

def read():
    success_list = []
    account_list = []
    try:
        with open('success_url.txt') as f:
            results = f.readlines()
            for res in results:
                url = res.strip()
                success_list.append(url)
    except:
        pass

    with open('all_url.txt') as f:
        results = f.readlines()
        for res in results:
            try:
                url = res.strip()
                if url in success_list:
                    continue
                account_list.append(url)
            except:
                print('该行文本格式有误')
                print(res)

    return account_list

async def get_detail(url):
    async with aiohttp.ClientSession() as session:
        try:
            aiohtml = await fetch(session, url)
            html = HTML(aiohtml)
            name = html.xpath('string(//div[@class="a-section a-spacing-small a-spacing-top-small"]/span/span)')
            count = html.xpath('string(//span[@id="s-result-count"]/text())')
            endcount = re.search('.*?(\d+,\d+|\d+) results', count)
            if endcount:
                endcount = endcount.group(1)
            elif endcount == None:
                endcount = re.search('(\d+) result', count).group(1)

            if endcount == None:
                endcount = ''
            print(name + ' , ' + endcount)
            name = name.replace(',', '，')
            endcount = endcount.replace(',', '')
            url = url.replace(',', '，')
            with open('results.csv', 'a') as f:
                f.write(endcount + ',' + name + ',' + url + '\n')
            with open('success_url.txt', 'a') as f:
                f.write(url + '\n')
        except:
            with open('failed_url.txt', 'a') as f:
                f.write(url + '\n')

async def main():
    async with aiohttp.ClientSession() as session:
        try:
            all_url = read()
            for url in all_url:
                await get_detail(url)

        except:
            print('未知错误')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())






