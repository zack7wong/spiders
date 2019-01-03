#!/usr/bin/env python
# -*- coding:utf-8 -*-

import itchat
import json
itchat.auto_login(hotReload = True)
friends = itchat.get_friends(update = True)
num=1
for data in friends[1:]:
    print(json.dumps(data))
    user_id = str(data['AttrStatus'])
    screen_name = str(data['NickName'])
    verified = str(data['VerifyFlag'])
    city = str(data['Province'])
    description = str(data['Signature'].replace('\n','').replace('\r',''))
    if data['Sex'] == 1:
        gender = '女'
    else:
        gender = '男'
    profile_image_url = str(data['HeadImgUrl'])
    save_res = user_id + ',' + screen_name + ',' + verified + ',' + city + ',' + description + ',' + gender + ',' + profile_image_url + '\n'
    print(save_res)

    #下载头像
    image = itchat.get_head_img(userName=data["UserName"])  # 用 itchat.get_head_img(userName=None)来爬取好友列表的头像
    # fileImage = open("headimg/" + str(num) + '_' + data['NickName'] + ".jpg", 'wb')  # 将好友头像下载到本地文件夹
    fileImage = open("headimg/" + str(num)  + ".jpg", 'wb')  # 将好友头像下载到本地文件夹
    fileImage.write(image)
    fileImage.close()
    num += 1

    #保存文件
    with open('weixin_results.csv', 'a') as f:
        f.write(save_res)
