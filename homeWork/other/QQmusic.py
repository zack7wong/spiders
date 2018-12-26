#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import time
import json

url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?tpl=3&page=detail&date={mydate}&topid=4&type=top&song_begin={page}&song_num=30&g_tk=136022792'

with open('结果.csv', 'w') as f:
    myres = '序号,歌曲名,歌手,时长\n'
    f.write(myres)
mynum = 1

for i in range(0,5):
    mydate = time.strftime('%Y-%m-%d',time.localtime())
    response = requests.get(url.format(mydate=mydate,page=i*30))
    json_obj = json.loads(response.text)
    # print(response.text)

    for data in json_obj['songlist']:
        # print(json.dumps(data))
        music = data['data']['songname']
        singer = data['data']['singer'][0]['name']
        mymin = int(data['data']['interval'] / 60)
        mysecend = int(data['data']['interval'] % 60)
        mytime = str(mymin) +':'+str(mysecend)
        # print(music,singer,mytime)
        myres = str(mynum)+','+music+','+singer+','+mytime+'\n'
        print(myres)
        with open('结果.csv','a') as f:
            f.write(myres)
        mynum+=1