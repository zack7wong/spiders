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

def get_driver():
    executable_path = '/usr/local/Cellar/phantomjs/2.1.1/bin/phantomjs'

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 "
    )

    driver = webdriver.PhantomJS(executable_path=executable_path, desired_capabilities=dcap)
    driver.set_page_load_timeout(15)

    return driver

URL = 'https://www.aqistudy.cn/historydata/daydata.php?city={city}&month={thisdate}'
year_list = ['2015','2016','2017','2018']
month_list = ['01','02','03','04','05','06','07','08','09','10','11','12']
city_name = ['秦皇岛','邢台','承德','沧州','蚌埠','马鞍山','铜陵','安庆','齐齐哈尔','铁岭','朝阳','葫芦岛','四平','安阳','新乡','焦作','黄石','泸州','德阳','潮州','赤峰','营口','兰州','乌鲁木齐','郑州','长沙'
    ,'贵阳','昆明','北京','许昌','邯郸','太原','大连','徐州','杭州','福州','潍坊','吉安','吴忠','辽源','南通','绍兴','芜湖','景德镇','威海','黄冈','常德','攀枝花','遵义','延安','嘉峪关']

driver = webdriver.Chrome()
for year in year_list:
    for month in month_list:
        for city in city_name:
            thisdate = year + '-' + month
            start_url = URL.format(city=city,thisdate=thisdate)
            print(start_url)
            try:
                driver.get(start_url)

                time.sleep(3)
                html = HTML(driver.page_source)
                date_list = html.xpath('//table[@class="table table-condensed table-bordered table-striped table-hover table-responsive"]//tr/td[1]/text()')
                aqi_list = html.xpath('//table[@class="table table-condensed table-bordered table-striped table-hover table-responsive"]//tr/td[2]/text()')
                zhiliang_list = html.xpath('//table[@class="table table-condensed table-bordered table-striped table-hover table-responsive"]//tr/td[3]//text()')
                pm2_list = html.xpath('//table[@class="table table-condensed table-bordered table-striped table-hover table-responsive"]//tr/td[4]/text()')
                pm10_list = html.xpath('//table[@class="table table-condensed table-bordered table-striped table-hover table-responsive"]//tr/td[5]/text()')
                so2_list = html.xpath('//table[@class="table table-condensed table-bordered table-striped table-hover table-responsive"]//tr/td[6]/text()')
                co_list = html.xpath('//table[@class="table table-condensed table-bordered table-striped table-hover table-responsive"]//tr/td[7]/text()')
                no2_list = html.xpath('//table[@class="table table-condensed table-bordered table-striped table-hover table-responsive"]//tr/td[8]/text()')
                o3_list = html.xpath('//table[@class="table table-condensed table-bordered table-striped table-hover table-responsive"]//tr/td[9]/text()')

                print(date_list)


                if len(date_list) < 1:
                    print(city_name, year, month)
                    continue

                for date,aqi,zhiliang,pm2,pm10,so2,co,no2,o3 in zip(date_list,aqi_list,zhiliang_list,pm2_list,pm10_list,so2_list,co_list,no2_list,o3_list):
                    with open('kongqi.csv','a') as f:
                        save_res = city+','+date + ',' + aqi + ',' + zhiliang + ',' + pm2 + ',' + pm10 + ',' + so2 + ',' + co + ',' + no2 + ',' + o3+'\n'
                        f.write(save_res)




                # driver.delete_all_cookies()
                # driver.close()
                # driver.quit()
            except:
                print(city_name, year, month)
