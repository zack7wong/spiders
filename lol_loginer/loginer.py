#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
import time
import re

account_list = []

area_list = {
    'Brazil':'#login-form-region > option:nth-child(1)',
    'EU_Nordic_East':'#login-form-region > option:nth-child(2)',
    'EU_West':'#login-form-region > option:nth-child(3)',
    'Japan':'#login-form-region > option:nth-child(4)',
    'Korea':'#login-form-region > option:nth-child(5)',
    'Latin_America_North':'#login-form-region > option:nth-child(6)',
    'Latin_America_South':'#login-form-region > option:nth-child(7)',
    'North_America':'#login-form-region > option:nth-child(8)',
    'Oceania':'#login-form-region > option:nth-child(9)',
    'Public_Beta':'#login-form-region > option:nth-child(10)',
    'Russia':'#login-form-region > option:nth-child(11)',
    'Turkey':'#login-form-region > option:nth-child(12)',
}

def login(account):
    name = account['name']
    password = account['password']
    area = account['area']
    try:
        driver = webdriver.Chrome()
        url = 'https://auth.riotgames.com/authorize?redirect_uri=https://login.support.riotgames.com/login_callback&client_id=player-support-zendesk&ui_locales=en-us%20en-us&response_type=code&scope=openid%20email'
        driver.get(url)
        driver.find_element_by_css_selector('#login-form-username').send_keys(name)
        time.sleep(1)
        driver.find_element_by_css_selector('#login-form-password').send_keys(password)
        time.sleep(1)
        driver.find_element_by_css_selector('#region-selector > span.placeholder > span.placeholder-text').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#login-form-region').click()
        time.sleep(1)
        driver.find_element_by_css_selector(area_list[area]).click()
        time.sleep(1)
        driver.find_element_by_css_selector('#login-button').click()
        WebDriverWait(driver, 15).until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, '#bottom')))
        html = driver.page_source
        get_email(html,account)
        driver.delete_all_cookies()
        driver.close()
        driver.quit()
        time.sleep(8)
    except:
        print('加载超时失败')
        driver.delete_all_cookies()
        driver.close()
        driver.quit()
        wirte_failed(account)


    # driver.find_elements_by_xpath('//*[@id="login-form-username"]').send_keys('Wouterr6')
    # driver.find_elements_by_xpath('//*[@id="login-form-password"]').send_keys('Fruitsap12')
    # driver.find_elements_by_xpath('//*[@id="login-form-password"]').click()
    # driver.find_elements_by_xpath('//*[@id="region-selector"]/span[1]/span[1]').click()
    # driver.find_elements_by_xpath('//*[@id="login-form-region"]').click()
    # driver.find_elements_by_xpath('#login-form-region > option:nth-child(3)').click()
    # driver.find_elements_by_xpath('//*[@id="login-button"]').click()

def get_email(html,account):
    search_res = re.search('HelpCenter.*?"email":"(.*?)","name"',html)
    if search_res:
        email = search_res.group(1)
        print('成功: ' + email)
        write_success(account,email)
    else:
        print('失败')
        wirte_failed(account)

def write_success(account,email):
    write_res = account['name']+':'+account['password']+':'+account['area']+':'+email+'\n'
    with open('success.txt','a') as f:
        f.write(write_res)

def wirte_failed(account):
    write_res = account['name'] + ':' + account['password'] + ':' + account['area'] + '\n'
    with open('faild.txt', 'a') as f:
        f.write(write_res)

def get_account():
    success_list = []
    try:
        with open('success.txt') as f:
            results = f.readlines()
            for res in results:
                name = res.split(':')[0]
                success_list.append(name)
    except:
        pass

    with open('account.txt') as f:
        results = f.readlines()
        for res in results:
            try:
                name = res.split(':')[0]
                password = res.split(':')[1].strip()
                area = res.split(':')[2].strip()
                account_obj = {
                    'name': name,
                    'password': password,
                    'area': area,
                }
                if name in success_list:
                    continue
                account_list.append(account_obj)
            except:
                print('该行文本格式有误')
                print(res)
                with open('failed.txt', 'a') as ff:
                    ff.write(res)

if __name__ == '__main__':
    get_account()
    for account in account_list:
        print('正在获取：' + str(account))
        login(account)