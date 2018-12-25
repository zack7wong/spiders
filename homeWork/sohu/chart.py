#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pyecharts import Bar
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from PIL import Image
from os import path
import numpy as np
from pyecharts import Line,configure

# with open('resuolts.txt') as f:
#     results = f.read()

text = open("results.txt", "rb").read()
# 结巴分词
wordlist = jieba.cut(text, cut_all=True)
wl = " ".join(wordlist)
#
# d = path.dirname(__file__)
#
# alice_mask = np.array(Image.open(path.join(d, "tupian.jpg")))
# # 设置词云
# wc = WordCloud(background_color="white",  # 设置背景颜色
#                mask = alice_mask,  #设置背景图片
#                max_words=2000,  # 设置最大显示的字数
#                # stopwords = "", #设置停用词
#                # font_path="C:\Windows\Fonts\SimHei.ttf",
#                font_path="/System/Library/Fonts/PingFang.ttc",
#                max_font_size=50,  # 设置字体最大值
#                random_state=30,
#                )
# myword = wc.generate(wl)  # 生成词云
#
#
# # 展示词云图
# plt.imshow(myword)
# plt.axis("off")
# plt.show()


mysplit_res = wl.split(' ')

item_list = []
account_list = []
for res in mysplit_res:
    if res == '':
        continue
    if res not in account_list:
        account_list.append(res)
        obj = {
            'key':res,
            'value':1
        }
        item_list.append(obj)
    else:
        for key in item_list:
            if key['key'] == res:
                key['value']+=1
                break

x_list = []
y_list = []
for item in item_list:
    x_list.append(item['key'])
    y_list.append(item['value'])
# bar = Bar("新闻","新闻",width=1500,title_text_size = 5)
# bar.add("新闻词频",x_list,y_list,label_text_size=5)
# bar.show_config()
# bar.render()
line =Line('折线图',background_color = 'white',title_text_size = 5,width=2500)
attr = x_list[:50]
v1 = y_list[:50]
line.add('词频',attr,v1,mark_line=['average'],is_label_show = True)
line.render(path = 'render.html')