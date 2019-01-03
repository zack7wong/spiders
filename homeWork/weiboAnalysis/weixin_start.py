#!/usr/bin/env python
# -*- coding:utf-8 -*-

import itchat
import json
itchat.auto_login(hotReload = True)
friends = itchat.get_friends(update = True)
for data in friends[1:]:
    user_id = data['AttrStatus']
    screen_name = data['AttrStatus']
    verified = data['AttrStatus']
    verified_reason = data['AttrStatus']
    description = data['AttrStatus']
    gender = data['AttrStatus']
    profile_image_url = data['AttrStatus']
    fans = data['AttrStatus']
    followers = data['AttrStatus']
    save_res = user_id + ',' + screen_name + ',' + verified + ',' + verified_reason + ',' + description + ',' + gender + ',' + profile_image_url + ',' + fans + ',' + followers + '\n'
    print(save_res)
    with open('weixin_results.csv', 'a') as f:
        f.write(save_res)