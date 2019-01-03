#!/usr/bin/env python
# -*- coding:utf-8 -*-

import TencentYoutuyun
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from PIL import Image
from os import path
import numpy as np

item_list = []
with open('results.csv') as f:
    results = f.readlines()
    for res in results:
        img_url = res.split(',')[6]
        item_list.append(img_url)

appid = '10163570'
secret_id = 'AKIDqUu4zefMr65pKaJNyJRKyPeeT6TaQ9Zj'
secret_key = '61kGXYLvFKDtKWTBesrgV6RXO0MTN5Yl'
userid = '123'

end_point = TencentYoutuyun.conf.API_YOUTU_END_POINT

youtu = TencentYoutuyun.YouTu(appid, secret_id, secret_key, userid, end_point)

for item in item_list:
    try:
        print(item)
        ret = youtu.imagetag(image_path=item,data_type =1)
        resStr = json.dumps(ret['tags'][0]['tag_name'])
        # print(resStr)
        # resStr = resStr.decode('utf8')
        res = json.loads(resStr, encoding="utf8")
        print(res)
        with open('head.txt','a') as f:
            f.write(res+'\n')
    except:
        continue

text = open("head.txt", "rb").read()
# 结巴分词
wordlist = jieba.cut(text, cut_all=True)
wl = " ".join(wordlist)

d = path.dirname(__file__)

alice_mask = np.array(Image.open(path.join(d, "head.jpeg")))
# 设置词云
wc = WordCloud(background_color="white",  # 设置背景颜色
               mask = alice_mask,  #设置背景图片
               max_words=2000,  # 设置最大显示的字数
               # stopwords = "", #设置停用词
               # font_path="C:\Windows\Fonts\SimHei.ttf",
               font_path="/System/Library/Fonts/PingFang.ttc",
               max_font_size=50,  # 设置字体最大值
               random_state=30,
               )
myword = wc.generate(wl)  # 生成词云

# 展示词云图
plt.imshow(myword)
plt.axis("off")
plt.savefig("头像词云.jpg")
plt.show()
