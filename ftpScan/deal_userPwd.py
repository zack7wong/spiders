#!/usr/bin/env python
# -*- coding:utf-8 -*-

user_list = []
with open('user.txt') as f:
    results = f.readlines()
    for res in results:
        user_list.append(res.strip())


password_list = []
with open('password.txt') as f:
    results = f.readlines()
    for res in results:
        password_list.append(res.strip())


with open('userPassword.txt','a') as f:
    for user in user_list:
        for password in password_list:
            save_res = user+':'+password+'\n'
            print(save_res)
            f.write(save_res)