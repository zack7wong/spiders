#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json

userInfo_url = 'https://m.weibo.cn/api/container/getIndex?containerid=100505{userId}'
followers = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{user_id}&page={page}'

for i in range(2,11):
    print('当前页：'+str(i))
    start_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_1826792401&page='+str(i)
    response = requests.get(start_url)
    # print(response.text)
    json_obj = json.loads(response.text)
    try:
        for data in json_obj['data']['cards'][0]['card_group']:
            user_id = str(data['user']['id'])

            user_response = requests.get(userInfo_url.format(userId=user_id))
            user_json_obj = json.loads(user_response.text)
            # print(user_response.text)

            screen_name = str(user_json_obj['data']['userInfo']['screen_name'])
            screen_name = screen_name.replace(',', '，')
            verified = str(user_json_obj['data']['userInfo']['verified'])
            verified_reason = str(user_json_obj['data']['userInfo']['verified_reason']) if 'verified_reason' in user_json_obj['data']['userInfo'] else ''
            verified_reason = verified_reason.replace(',','，')
            description = str(user_json_obj['data']['userInfo']['description'])
            description = description.replace(',', '，')
            gender = str(user_json_obj['data']['userInfo']['gender'])
            if gender == 'm':
                gender = '男'
            else:
                gender = '女'
            fans = str(user_json_obj['data']['userInfo']['followers_count'])
            followers = str(user_json_obj['data']['userInfo']['followers_count'])
            profile_image_url = str(user_json_obj['data']['userInfo']['profile_image_url'])
            save_res = user_id+','+screen_name+','+verified+','+verified_reason+','+description+','+gender+','+profile_image_url+','+fans+','+followers+'\n'
            print(save_res)
            with open('results.csv','a') as f:
                f.write(save_res)
    except:
        continue