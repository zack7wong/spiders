#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
import time
import re
import requests
from lxml.etree import HTML
from urllib.parse import quote


def reg():

    driver = webdriver.Chrome()
    driver.get('https://github.com/join?source=header-home')
    driver.find_element_by_css_selector('#user_login').send_keys(username)
    driver.find_element_by_css_selector('#user_email').send_keys(email)
    driver.find_element_by_css_selector('#user_password').send_keys(password)

    driver.find_element_by_css_selector('#signup_button').click()

    #检测是否注册完成
    flag = 0
    while True:
        cookies = driver.get_cookies()
        # print(cookies)
        for cookie in cookies:
            if cookie['name'] == 'logged_in':
                if cookie['value'] == 'yes':
                    flag += 1

            if cookie['name'] == 'dotcom_user':
                if cookie['value'] == username:
                    flag += 1

        if flag == 2:
            print('已注册完成！')
            break
        print('注册尚未完成。。')
        time.sleep(3)

def login(driver):
    # 昵称：adse12143
    # 密码：sf32sa12
    # 邮箱：safw32@163.com

    driver.get('https://github.com/login')
    driver.find_element_by_css_selector('#login_field').send_keys(username)
    driver.find_element_by_css_selector('#password').send_keys(password)
    driver.find_element_by_css_selector('#login > form > div.auth-form-body.mt-3 > input.btn.btn-primary.btn-block').click()

def get_info(driver):
    url = 'https://github.com/trending'
    driver.get(url)
    driver.find_element_by_link_text('Developers').click()
    driver.find_element_by_xpath(' //*[@id="container"]//div/details/summary/span').click()
    time.sleep(2)
    driver.find_element_by_xpath('//div[@class="select-menu-list"]/a[2]/span').click()
    time.sleep(5)
    html = HTML(driver.page_source)
    name_list = html.xpath('//div[@class="explore-content"]//li//h2/a/@href')
    for name in name_list:
        print(name[1:].strip())

def start():
    reg()


    driver = webdriver.Chrome()
    print('正在登录。。。')
    login(driver)

    print('获取数据。。。')
    get_info(driver)

    time.sleep(100)

if __name__ == '__main__':
    print('正在注册。。。')
    username = input('请输入注册昵称：')
    password = input('请输入注册密码：')
    email = input('请输入注册邮箱：')
    start()