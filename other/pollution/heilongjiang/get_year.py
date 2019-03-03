#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
import time
import db
import copy
from lxml.etree import HTML


def start(item_list):
    driver = webdriver.Chrome()
    for item in item_list:
        try:
            print(item)
            url = item['url']
            driver.get(url)
            time.sleep(3)

            #获取是废水还是废气
            html = HTML(driver.page_source)
            nameList = html.xpath('//select[@id="ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_ddlIndicatorCategory"]/option/text()')
            print(nameList)

            thisList = []
            for name in nameList:
                if name == '废水' or name == '废气':
                    nameIndex = nameList.index(name)
                    nameIndex = str(nameIndex+1)
                    this_obj = {
                        'EntTypeName':name,
                        'selectorObj':'#ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_ddlIndicatorCategory > option:nth-child('+nameIndex+')',
                    }
                    thisList.append(this_obj)

            #类型循环
            for EntTypeNameObj in thisList:
                try:
                    EntTypeName = EntTypeNameObj['EntTypeName']
                    selectorObj = EntTypeNameObj['selectorObj']
                    driver.find_element_by_css_selector(selectorObj).click()
                    #输入日期查询
                    date_list = [{'startDate':'2014-01-01','endDate':'2014-12-31'},{'startDate':'2015-01-01','endDate':'2015-12-31'},{'startDate':'2016-01-01','endDate':'2016-12-31'},{'startDate':'2017-01-01','endDate':'2017-12-31'},{'startDate':'2018-01-01','endDate':'2018-12-31'},{'startDate':'2019-01-01','endDate':'2019-03-01'},]
                    for dateObj in date_list:
                        driver.find_element_by_css_selector('#ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_txtStartTime').click()
                        driver.find_element_by_css_selector('#ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_txtStartTime').clear()
                        driver.find_element_by_css_selector('#ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_txtStartTime').send_keys(dateObj['startDate'])

                        driver.find_element_by_css_selector('#ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_txtEndTime').click()
                        driver.find_element_by_css_selector('#ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_txtEndTime').clear()
                        driver.find_element_by_css_selector('#ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_txtEndTime').send_keys(dateObj['endDate'])

                        driver.find_element_by_css_selector('#ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_btnSearch').click()
                        time.sleep(8)

                        try:
                            driver.find_element_by_xpath('//table[@id="ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_gvHistoryData"]//table[@class="PagerStyleInfo5"]//td[last()]/input').click()
                            time.sleep(12)

                            html =HTML(driver.page_source)
                            totalNum = html.xpath('string(//table[@id="ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_gvHistoryData"]//table[@class="PagerStyleInfo5"]//td[3]/a[last()]/text())').strip()

                            save_res = item['url']+','+item['title']+','+dateObj['startDate']+','+dateObj['endDate']+','+totalNum+','+EntTypeName+'\n'
                            print(save_res)
                            with open('new_heilongjiang_id.txt','a') as f:
                                f.write(save_res)
                        except:
                            continue
                except:
                    continue
        except:
            continue

if __name__ == '__main__':
    dbclient = db.MysqlClient()
    item_list = []
    with open('heilongjiang_id.txt') as f:
        results = f.readlines()
        for res in results:
            url = res.split(',')[0]
            title = res.split(',')[1].strip()
            obj = {
                'url': url,
                'title': title,
            }
            item_list.append(obj)

    start(item_list)