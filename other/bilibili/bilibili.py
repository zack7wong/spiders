#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import re
import json
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from PIL import Image
from os import path
import numpy as np

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    # 'Cookie': "rpdid=iwkikxiqoodospxmmokqw; stardustvideo=1; CURRENT_FNVAL=16; sid=ljzva72k; _uuid=03657428-C497-FD68-A602-C6B7BC4E158276744infoc; buvid3=D4C4D108-B1A6-4B0B-BF18-00707BB34B8A65962infoc; LIVE_BUVID=AUTO2015509224772438; fts=1550923670",
    # 'Cookie': "rpdid=iwkikxiqoodospxmmokqw; stardustvideo=1; CURRENT_FNVAL=16; sid=ljzva72k; _uuid=03657428-C497-FD68-A602-C6B7BC4E158276744infoc; buvid3=D4C4D108-B1A6-4B0B-BF18-00707BB34B8A65962infoc; LIVE_BUVID=AUTO2015509224772438; fts=1550923670",
    'Host': "www.bilibili.com",
    'Pragma': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    'cache-control': "no-cache",
}

def get_danmu(url):
    # url = 'https://www.bilibili.com/video/av'+id
    print(url)
    response = requests.get(url, headers=headers, verify=False)
    # print(response.text)
    #在网页源码中用正则查找
    res = re.search('window.__INITIAL_STATE__=(.*?);\(function\(\){var s;',response.text).group(1)
    json_obj = json.loads(res)
    # print(json.dumps(json_obj))
    #获取cid
    try:
        title = json_obj['videoData']['title'].replace('/','').replace('“','').replace('”','').strip()
        cid = str(json_obj['videoData']['cid'])
    except:
        title = json_obj['h1Title'].replace('/','').replace('“','').replace('”','').strip()
        cid = str(json_obj['epList'][-1]['cid'])

    # 发起xml请求
    url = 'https://api.bilibili.com/x/v1/dm/list.so?oid='+cid  # 弹幕地址
    print(title)
    print(url)
    response = requests.get(url, verify=False) # 发起请求并获得网页内容
    html = response.content
    html_data = str(html, 'utf-8')  # 对网页进行‘utf-8’解码

    # 解析xml并提取弹幕内容
    soup = BeautifulSoup(html_data, 'lxml')
    results = soup.find_all('d')  # 找到所有的‘d'标签
    comments = []
    id_list  = []
    for x in results:  # 提取每个’d'标签的text内容，即弹幕文字
        comments.append(x.text)
        id = x['p'].split(',')[-1]
        id_list.append(id)
        print(id, x.text)
        with open(title+'_id.txt','a') as f:
            f.write(id+','+x.text+'\n')

    # print(comments)

    item_list = []
    account_list = []
    for sent in comments:
        if sent in account_list:
            for item in item_list:
                if item['key'] == sent:
                    item['value'] += 1
                    break
        else:
            account_list.append(sent)
            obj = {
                'key': sent,
                'value': 1
            }
            item_list.append(obj)
    print(item_list)
    for item in item_list:
        print('弹幕内容：'+item['key']+'  出现的次数：'+str(item['value']))
        with open(title+'_词频统计.txt','a') as f:
            f.write('弹幕内容：'+item['key']+'  出现的次数：'+str(item['value'])+'\n')

    return comments,title

def get_ciyun(title,comments):
    allComments = ' '.join(comments)
    text = allComments.encode()
    # 结巴分词
    wordlist = jieba.cut(text, cut_all=True)
    wl = " ".join(wordlist)

    d = path.dirname(__file__)

    alice_mask = np.array(Image.open(path.join(d, "tupian.jpg")))
    # 设置词云
    wc = WordCloud(background_color="white",  # 设置背景颜色
                   mask=alice_mask,  # 设置背景图片
                   max_words=100,  # 设置最大显示的字数
                   font_path="C:\Windows\Fonts\SimHei.ttf",
                   # font_path="/System/Library/Fonts/PingFang.ttc",
                   max_font_size=50,  # 设置字体最大值
                   random_state=30,
                   prefer_horizontal=1,#横向频率
                   min_font_size = 14 #最小字体
                   )
    myword = wc.generate(wl)  # 生成词云

    # 展示词云图
    plt.imshow(myword)
    plt.axis("off")
    plt.savefig(title+'.jpg')
    plt.show()

def start(url):
    comments,title = get_danmu(url)
    get_ciyun(title,comments)



if __name__ == '__main__':
    url_list = ['https://www.bilibili.com/bangumi/play/ss5969#205890','https://www.bilibili.com/video/av43822309']
    for url in url_list:
        start(url)