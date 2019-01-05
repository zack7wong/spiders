#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pyecharts import Line,configure
from pyecharts import Bar, Grid
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from PIL import Image
from os import path
import numpy as np

name_list = []
price_list = []
with open('results.csv') as f:
    results = f.readlines()
    for res in results[51:61]:
        name = res.split(',')[1].strip()[:5]
        price = float(res.split(',')[2].replace('¥',''))
        # comment = int(res.split(',')[3].replace('条评论','').strip())
        name_list.append(name)
        price_list.append(price)

line =Line('折线图',background_color = 'white',title_text_size = 5,width=1500)
attr = name_list[:10]
line.add('现价',name_list,price_list,mark_line=['average'],is_label_show = True)
line.render(path = '折线图.html')


bar = Bar("柱状图")
bar.add("柱状图", name_list, price_list, is_stack=True,width=1500)
bar.render(path = '条形图.html')

# grid = Grid(width=1500)
# grid.add(line, grid_bottom="60%", grid_right="60%")
# grid.add(bar, grid_bottom="60%", grid_right="60%")
# grid.render('图表.html')

text = open("results.csv", "rb").read()
# 结巴分词
wordlist = jieba.cut(text, cut_all=True)
wl = " ".join(wordlist)

d = path.dirname(__file__)

alice_mask = np.array(Image.open(path.join(d, "tupian.jpeg")))
# 设置词云
wc = WordCloud(background_color="white",  # 设置背景颜色
               mask = alice_mask,  #设置背景图片
               max_words=2000,  # 设置最大显示的字数
               # stopwords = "", #设置停用词
               font_path="C:\Windows\Fonts\SimHei.ttf",
               # font_path="/System/Library/Fonts/PingFang.ttc",
               max_font_size=50,  # 设置字体最大值
               random_state=30,
               )
myword = wc.generate(wl)  # 生成词云

# 展示词云图
plt.imshow(myword)
plt.axis("off")
plt.show()