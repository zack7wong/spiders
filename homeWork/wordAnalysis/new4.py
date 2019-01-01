#!/usr/bin/env python
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from PIL import Image
from os import path
import numpy as np

def deal(filename):
    text = open(filename, "rb").read()
    # 结巴分词
    wordlist = jieba.cut(text, cut_all=True)
    wl = " ".join(wordlist)

    d = path.dirname(__file__)

    alice_mask = np.array(Image.open(path.join(d, "ciyun.jpeg")))
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

    plt.savefig(filename+'.png')
    plt.show()

deal('武动乾坤.txt')
deal('红楼梦.txt')