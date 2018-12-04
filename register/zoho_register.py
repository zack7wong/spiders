#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import requests
import json
import re
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

success_num = 0

HEADERS = {
     'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    # 'Content-Length': "232",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    # 'Cookie': "a8c61fa0dc=6e15a611e5c4ec13f4a5d9bd7bfe2063; iamcsr=58d9b8fe-49fe-4423-a69c-172ecb753104; JSESSIONID=EEECC9069D3A37CD226294CF3DED01E7; Hm_lvt_d8145ef350792690dbbc2a2b0e6d7eb6=1543758679; stk=96972ce8c2112ee4ed70bf3cb27eb82f; dcl_pfx_lcnt=0; Hm_lpvt_d8145ef350792690dbbc2a2b0e6d7eb6=1543758789; rtk=c526b2a4-40ad-4816-a91b-8a1ba05060b3",
    'Host': "accounts.zoho.com.cn",
    'Origin': "https://www.zoho.com.cn",
    'Pragma': "no-cache",
    'Referer': "https://www.zoho.com.cn/mail/",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'cache-control': "no-cache"
}
SEND_CODE_URL = 'https://accounts.zoho.com.cn/accounts/register.ac'
LOGIN_URL = 'https://accounts.zoho.com.cn/u/verifyotp'

iamcsrcoo=''
username = ''


class Shenhua(object):
    def __init__(self):
        pass

    def login(self):
        url = 'http://api.shjmpt.com:9002/pubApi/uLogin?uName=shagua999888&pWord=shagua999888'
        response = requests.get(url,timeout=40)
        token = response.text.split('&')[0]
        return token

    def get_phone(self,token):
        url = 'http://api.shjmpt.com:9002/pubApi/GetPhone?ItemId=127136&token={token}'.format(token=token)
        response = requests.get(url,timeout=40)
        return_res = response.text.replace(';', '')
        return return_res

    def get_message(self, token, phone):
        for i in range(8):
            url = 'http://api.shjmpt.com:9002/pubApi/GMessage?token={token}&ItemId=127136&Phone={phone}'.format(token=token, phone=phone)
            response = requests.get(url,timeout=40)
            print(response.text)
            if '&' in response.text:
                message = response.text.split('&')[3]
                search_res = re.search('\d{7}', message)
                if search_res:
                    print('获取手机验证码成功')
                    return search_res.group(0)
            time.sleep(5)
        print('获取手机验证码失败')
        return None

def random_username():
    pwdstr = "1234567890abcdefghizklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    pwd_list = []
    random_num = random.sample(range(6, 10), 1)
    random_num = random_num[0]

    for i in range(random_num):
        pwd_list.append(random.choice(pwdstr))
    return ''.join(pwd_list)

def get_cookie():
    global iamcsrcoo
    url = 'https://accounts.zoho.com.cn/accounts/register.js?service_language=&servicename=VirtualOffice&mobile_only=true&loadcss=false&serviceurl=/'
    response =requests.get(url)
    cookie_dic = response.cookies.get_dict()
    str_cookie = ''
    for key in cookie_dic.keys():
        value = cookie_dic[key]
        str_cookie +=key+'='+value+';'
        if key == 'iamcsr':
            iamcsrcoo = cookie_dic[key]
    print(str_cookie)
    HEADERS['cookie'] = str_cookie

def send_code(phone):
    print('请求发送验证码。。')
    #mytest7788!Q    fF23@1
    global username
    username = random_username()
    firstname = username[:3]
    lastname = username[3:]
    body = 'username={username}&password=fF23@1&firstname={firstname}&lastname={lastname}&country_code=CN&mobile={phone}&confirm_country_code=CN&confirmMobile={phone}&tos=false&mobile_only=true&serviceurl=%2F&servicename=VirtualOffice&is_ajax=true'.format(phone=phone,username=username,firstname=firstname,lastname=lastname)
    print(SEND_CODE_URL)
    print(body)
    print(HEADERS)
    response = requests.post(SEND_CODE_URL, headers=HEADERS, data=body,verify=False,timeout=10)
    if response is not None:
        print('返回的token：' + response.text)
        json_obj = json.loads(response.text)
        status = json_obj['data']['httpResponseCode']
        if status == 200:
            cookie_dic = response.cookies.get_dict()
            str_cookie = ''
            for key in cookie_dic.keys():
                value = cookie_dic[key]
                str_cookie += key + '=' + value + ';'
            print(str_cookie)
            HEADERS['cookie'] += str_cookie
            return True
    return None

def login(phone, code):

    this_url = 'https://accounts.zoho.com.cn/ui/settings/verifyMobileSignup.jsp?serviceurl=https%3A%2F%2Fmail.zoho.com.cn%2F&servicename=VirtualOffice'
    this_response = requests.get(this_url, headers=HEADERS, verify=False)
    # cookie_dic = this_response.cookies.get_dict()
    # str_cookie = ''
    # for key in cookie_dic.keys():
    #     value = cookie_dic[key]
    #     str_cookie += key + '=' + value + ';'
    # print(str_cookie)
    # HEADERS['cookie'] = str_cookie

    global iamcsrcoo
    body = 'otpcode={code}&iamcsrcoo={iamcsrcoo}&servicename=VirtualOffice&serviceurl=https%3A%2F%2Fmail.zoho.com.cn%2F'.format(iamcsrcoo=iamcsrcoo,code=code)
    response = requests.post(LOGIN_URL, headers=HEADERS, data=body,verify=False)
    if response is not None:
        if 'showsuccess' in response.text:
            print('登录成功，正在请求跳过验证。。')
            cookie_dic = response.cookies.get_dict()
            str_cookie = ''
            for key in cookie_dic.keys():
                value = cookie_dic[key]
                str_cookie += key + '=' + value + ';'
                if key == 'iamcsr':
                    iamcsrcoo = cookie_dic[key]
            # print(str_cookie)
            this_iamcsr = HEADERS['cookie']
            myiamcsr = re.search('_iamtt=(.*?);', this_iamcsr).group(1)
            HEADERS['cookie'] = HEADERS['cookie'].replace(myiamcsr, '')
            HEADERS['cookie'] += str_cookie


            get_mai_url ='https://accounts.zoho.com.cn/accounts/announcement/tfa-banner?serviceurl=https%3A%2F%2Fmail.zoho.com.cn%2F&servicename=VirtualOffice'
            end_response = requests.get(get_mai_url, headers=HEADERS, verify=False)
            cookie_dic = end_response.cookies.get_dict()
            str_cookie = ''
            print(HEADERS['cookie'])
            for key in cookie_dic.keys():
                value = cookie_dic[key]
                if key == 'iamcsrocrmai':
                    str_cookie += key + '=' + value + ';'
                if key =='iamcsr':
                    this_iamcsr = HEADERS['cookie']
                    myiamcsr = re.search('iamcsr=(.*?);',this_iamcsr).group(1)
                    HEADERS['cookie'] = HEADERS['cookie'].replace(myiamcsr,value)
            # print(str_cookie)
            HEADERS['cookie'] += str_cookie
            print(HEADERS['cookie'])


            # end_url = 'https://accounts.zoho.com.cn/accounts/announcement/tfa-banner/next?status=3&serviceurl=https%3A%2F%2Fmail.zoho.com.cn%2F&servicename=VirtualOffice'
            # end_response = requests.get(end_url, headers=HEADERS, verify=False)
            #
            # _iamadt = re.search('_iamadt=(.*?);', HEADERS['cookie']).group(1)
            # _z_identity = re.search('_z_identity=(.*?);', HEADERS['cookie']).group(1)
            # _iambdt = re.search('_iambdt=(.*?);', HEADERS['cookie']).group(1)
            # all = '_iamadt='+_iamadt+';_z_identity='+_z_identity+';_iambdt='+_iambdt
            # HEADERS['cookie'] = all
            #
            #
            # host_url ='https://mail.zoho.com.cn/'
            # host_response = requests.get(host_url, headers=HEADERS, verify=False)
            # cookie_dic = host_response.cookies.get_dict()
            # str_cookie = ''
            # for key in cookie_dic.keys():
            #     value = cookie_dic[key]
            #     str_cookie += key + '=' + value + ';'
            # print(str_cookie)
            # HEADERS['cookie'] += str_cookie
            # print(HEADERS['cookie'])
            #
            #
            # do_url = 'https://mail.zoho.com.cn/biz/index.do'
            # do_response = requests.get(do_url, headers=HEADERS, verify=False)
            #
            # zm_url = 'https://mail.zoho.com.cn/zm/'
            # zm_response = requests.get(zm_url, headers=HEADERS, verify=False)
            #
            # if zm_response.status_code ==200:
            #     print('跳过验证成功')
            #     return True

            #做登录
            # res = chrome_login(username)
            # if res:
            #     return True
            # else:
            #     return False
            # login_url = 'https://accounts.zoho.com.cn/signin?servicename=VirtualOffice&signupurl=https://workplace.zoho.com.cn/orgsignup.do'
            # login_response = requests.get(login_url, verify=False)
            # cookie_dic = login_response.cookies.get_dict()
            # str_cookie = ''
            # mythisiamcsrcoo = ''
            # for key in cookie_dic.keys():
            #     value = cookie_dic[key]
            #     str_cookie += key + '=' + value + ';'
            #     if key == 'iamcsr':
            #         mythisiamcsrcoo = cookie_dic[key]
            # print(str_cookie)
            # HEADERS['cookie'] = str_cookie
            #
            # auth_url ='https://accounts.zoho.com.cn/signin/auth'
            # body = 'LOGIN_ID='+username+'%40zoho.com.cn&PASSWORD=fF23@1&cli_time=1543775314805&remember=2592000&iamcsrcoo='+mythisiamcsrcoo+'&servicename=VirtualOffice&serviceurl=https%3A%2F%2Fmail.zoho.com.cn'
            # auth_response = requests.post(auth_url, data=body, headers=HEADERS, verify=False)
            # print(auth_response.text)
            # print(auth_response.status_code)

    print('登录失败')
    return False

def chrome_login(username):
    url = 'https://accounts.zoho.com.cn/signin?servicename=VirtualOffice&signupurl=https://workplace.zoho.com.cn/orgsignup.do'
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)
    driver.find_element_by_css_selector('#lid').send_keys(username)
    driver.find_element_by_css_selector('#pwd').send_keys('fF23@1')
    driver.find_element_by_css_selector('#signin_submit').click()
    try:
        WebDriverWait(driver, 15, 0.5).until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, '#skip')))
        driver.delete_all_cookies()
        driver.close()
        driver.quit()
        return True
    except:
        return False




def start():
    # try:
        get_cookie()
        token = shenhua.login()
        phone = shenhua.get_phone(token)
        print('\n' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        print('当前手机号:' + phone)
        validate_token = send_code(phone)
        if validate_token:
            message_res = shenhua.get_message(token, phone)
            if message_res:
                reg_res = login(phone, message_res)
                if reg_res:
                    global success_num
                    success_num+=1
                    with open('account.txt', 'a') as f:
                        write_res = username + '@zoho.com.cn----fF23@1' + '\n'
                        f.write(write_res)
                        return

            print('注册失败')
            return
        else:
            print('发送验证码失败')
            return
    # except:
    #     print('异常，跳过。。')

if __name__ == '__main__':
    shenhua = Shenhua()
    num = input('请输入注册个数：')
    for i in range(int(num)):
        start()
        HEADERS['cookie'] = ''
        iamcsrcoo=''
        username= ''
    print('注册数: '+ num+ '  成功数: '+str(success_num))

