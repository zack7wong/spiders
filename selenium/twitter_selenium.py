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
from lxml.etree import HTML
from lxml import etree

id_list = []

url = 'https://twitter.com/search?f=tweets&vertical=default&q=%23CIIE&src=typd'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=' + '127.0.0.1:1087')
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(
    chrome_options=chrome_options
)
driver.get(url)
time.sleep(3)
while True:
    try:
        driver.execute_script("window.scrollBy(0,5000)")
        time.sleep(5)
        # print(driver.page_source)

        html = HTML(driver.page_source)
        results = html.xpath('//div[@class="stream"]/ol/li')
        for res in results:
            try:
                detail_html_text = etree.tostring(res)
                detail_html = HTML(detail_html_text.decode())
                content_list = detail_html.xpath('//p[@class="TweetTextSize  js-tweet-text tweet-text"]//text()')
                content = ''.join(content_list).replace('\n','').replace('\r','').replace('\t','').replace(',','，').strip()
                commentCount = detail_html.xpath('string(//div[@class="ProfileTweet-action ProfileTweet-action--reply"]//span[@class="ProfileTweet-actionCountForPresentation"]//text())')
                shareCount = detail_html.xpath('string(//div[@class="ProfileTweet-action ProfileTweet-action--retweet js-toggleState js-toggleRt"]//span[@class="ProfileTweet-actionCountForPresentation"]//text())')
                likeCount = detail_html.xpath('string(//div[@class="ProfileTweet-action ProfileTweet-action--favorite js-toggleState"]//span[@class="ProfileTweet-actionCountForPresentation"]//text())')
                publisthDate = detail_html.xpath('string(//a[@class="tweet-timestamp js-permalink js-nav js-tooltip"]/span/@data-time)')
                publishDateStr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(publisthDate)))
                posterId = detail_html.xpath('string(//a[@class="account-group js-account-group js-action-profile js-user-profile-link js-nav"]/@href)')[1:]
                id = detail_html.xpath('string(//a[@class="tweet-timestamp js-permalink js-nav js-tooltip"]/@data-conversation-id)')
                url = 'https://twitter.com' + detail_html.xpath('string(//a[@class="tweet-timestamp js-permalink js-nav js-tooltip"]/@href)')
                # print(id,posterId,url,content,commentCount,shareCount,likeCount,publishDateStr,publisthDate)

                if id not in id_list:
                    print(id + ' || ' + posterId + ' || ' + url + ' || ' + content + ' || ' + commentCount + ' || ' + shareCount + ' || ' + likeCount + ' || ' + publishDateStr + ' || ' + publisthDate)
                    with open('CIIE.csv','a') as f:
                        save_res = id+','+posterId+','+url+','+content+','+commentCount+','+shareCount+','+likeCount+','+publishDateStr+','+publisthDate + '\n'
                        f.write(save_res)
                    id_list.append(id)

            except:
                pass
    except:
        pass