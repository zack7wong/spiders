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
        print(item)
        url = item['url']
        driver.get(url)
        time.sleep(2)

        #输入日期查询
        driver.find_element_by_css_selector('#ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_txtStartTime').click()
        driver.find_element_by_css_selector('#ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_txtStartTime').clear()
        driver.find_element_by_css_selector('#ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_txtStartTime').send_keys('2014-01-01')

        driver.find_element_by_css_selector('#ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_txtEndTime').click()
        driver.find_element_by_css_selector('#ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_txtEndTime').clear()
        driver.find_element_by_css_selector('#ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_txtEndTime').send_keys('2014-12-31')

        driver.find_element_by_css_selector('#ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_btnSearch').click()
        time.sleep(8)


        #获取数据
        #企业名称、污染源类型（废水、废气）、监测点位、监测方式、监测时间、监测项目、执行标准、检测值、单位、标准限值、是否达标、是否停产、备注
        flagObj = {}
        obj = {}
        exitFlag = False
        while True:
            html = HTML(driver.page_source)

            tr_list = html.xpath('//table[@id="ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_gvHistoryData"]//tr')
            for tr in tr_list[1:-2]:
                title = ''
                EntTypeName = ''
                jiancedianName = tr.xpath('string(./td[1]/text())')
                jianceType =    tr.xpath('string(./td[2]/text())')
                jianceTime = tr.xpath('string(./td[3]/text())')
                jianceProject = tr.xpath('string(./td[4]/text())')
                zhixingBiaozhun = tr.xpath('string(./td[5]/text())')
                jianceValue = tr.xpath('string(./td[6]/span/text())')
                danwei = tr.xpath('string(./td[7]/text())')
                biaozhunXianzhi = tr.xpath('string(./td[8]/span/text())')
                shifouDabiao = tr.xpath('string(./td[9]/span/text())')
                shifouTingchan = tr.xpath('string(./td[11]/span/text())')
                beizhu = tr.xpath('string(./td[12]/text())')

                # print(jianceTime)

                obj = {
                    'title':title,
                    'EntTypeName':EntTypeName,
                    'jiancedianName':jiancedianName,
                    'jianceType':jianceType,
                    'jianceTime':jianceTime,
                    'jianceProject':jianceProject,
                    'zhixingBiaozhun':zhixingBiaozhun,
                    'jianceValue':jianceValue,
                    'danwei':danwei,
                    'biaozhunXianzhi':biaozhunXianzhi,
                    'shifouDabiao':shifouDabiao,
                    'shifouTingchan':shifouTingchan,
                    'beizhu':beizhu,
                }
                print(obj)
                flagNum = 0
                for key in flagObj.keys():
                    if flagObj[key] == obj[key]:
                        flagNum+=1
                if flagNum == 13:
                    print('已经到了页尾')
                    exitFlag = True

            if exitFlag:
                break

            flagObj = copy.deepcopy(obj)

            # 获取点击的selector
            print('开始点击下一页')
            # selector = html.xpath('string(//table[@class="PagerStyleInfo5"]//td[last()-1]/input/@id)')
            # selectorStr = '#' + selector
            # print(selectorStr)
            # driver.find_element_by_css_selector(selectorStr).click()
            driver.find_element_by_xpath('//table[@id="ctl00_ctl00_cphMain_cphMainPage_UCDataSearch_gvHistoryData"]//table[@class="PagerStyleInfo5"]//td[last()-1]/input').click()
            time.sleep(6)
            # print(driver.page_source)

        break
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