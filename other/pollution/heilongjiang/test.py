#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     test
   Description :
   Author :        hayden_huang
   Date：          2019/3/2 22:12
-------------------------------------------------
"""

from selenium import webdriver
driver = webdriver.Chrome()
driver.get('http://1.189.191.146:8000/eMonPubHLJ/Factory.aspx?code=912330065742110930')
driver.find_element_by_css_selector('#ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_ddlIndicatorCategory > option:nth-child(2)').click()