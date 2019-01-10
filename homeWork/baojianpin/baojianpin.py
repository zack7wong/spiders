#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     baojianpin
   Description :
   Author :        hayden_huang
   Date：          2018/12/25 17:49
-------------------------------------------------
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

driver = webdriver.Chrome()
url = 'http://samr.cfda.gov.cn/WS01/CL0001/'
# url = 'http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=30&tableName=TABLE30&title=%B9%FA%B2%FA%B1%A3%BD%A1%CA%B3%C6%B7&bcId=118103385532690845640177699192'
driver.get(url)
print(driver.page_source)
time.sleep(3)

url = 'http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=30&tableName=TABLE30&title=%B9%FA%B2%FA%B1%A3%BD%A1%CA%B3%C6%B7&bcId=118103385532690845640177699192'

driver.get(url)

time.sleep(2)
driver.find_element_by_css_selector('#tr2p1 > td > table > tbody > tr > td:nth-child(3)').click()
# driver.execute_script("window.scrollBy(0,500)")
# driver.find_element_by_css_selector('#content > table:nth-child(2) > tbody > tr:nth-child(1) > td > p > a').click()
# driver.find_element_by_xpath('//img[@src="images/dataanniu_07.gif"]').click()
# driver.find_element_by_css_selector('#goInt').send_keys('2')
# button = driver.find_element_by_css_selector('#content > table:nth-child(4) > tbody > tr > form')
# driver.execute_script("$(arguments[0]).click()", button)
# print(driver.page_source)


#//div[@id="content"]//table//tr//a/@href