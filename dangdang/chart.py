#!/usr/bin/env python
# -*- coding:utf-8 -*-

import db
import matplotlib.pyplot as plt
import pandas as pd

from wordcloud import WordCloud
import jieba
from PIL import Image
from os import path
import numpy as np


def deal_now_price(results):
    book_list = []
    price_list = []
    for res in results[:10]:
        # print(res)
        if res[4] == None:
            continue
        bookName = res[3][:10]
        price = res[4]

        book_list.append(bookName)
        price_list.append(float(price))



    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.bar(range(len(price_list)), price_list, tick_label=book_list)
    plt.savefig("书籍价格柱状图.jpg")
    plt.show()

def deal_publishing(results):
    item_list = []
    account_list = []
    for res in results:
        if res[10] in account_list:
            for item in item_list:
                if item['key'] == res[10]:
                    item['value'] += 1
                    break
        else:
            account_list.append(res[10])
            obj = {
                'key': res[10],
                'value': 1
            }
            item_list.append(obj)

    item_list = sorted(item_list, key=lambda x: x['value'], reverse=True)
    name_list = []
    num_list = []
    for item in item_list[:10]:
        name_list.append(item['key'])
        num_list.append(item['value'])

    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.pie(num_list, labels=name_list, autopct='%1.2f%%')  # 画饼图
    plt.savefig("出版社饼图.jpg")
    plt.show()

def deal_commentCount(results):
    book_list = []
    commentCount_list = []
    for res in results[:10]:
        # print(res)
        if res[7] == None:
            continue
        bookName = res[3][:10]
        commentCount = res[7]

        book_list.append(bookName)
        commentCount_list.append(int(commentCount))



    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.plot(book_list, commentCount_list)
    # plt.bar(range(len(commentCount_list)), commentCount_list, tick_label=book_list)
    plt.savefig("评论数折线图.jpg")
    plt.show()

def deal_ciyun(results):
    book_Str = ''
    for res in results[:10]:
        bookName = res[3]
        book_Str += bookName

    text = book_Str.encode()
    # 结巴分词
    wordlist = jieba.cut(text, cut_all=True)
    wl = " ".join(wordlist)

    d = path.dirname(__file__)

    alice_mask = np.array(Image.open(path.join(d, "tupian.jpg")))
    # 设置词云
    wc = WordCloud(background_color="white",  # 设置背景颜色
                   mask=alice_mask,  # 设置背景图片
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
    plt.savefig("书名词云图.jpg")
    plt.show()


def main():
    sql = "select * from books"
    results = mysqlCli.find_all(sql)

    deal_now_price(results)
    deal_publishing(results)
    deal_commentCount(results)
    deal_ciyun(results)

if __name__ == '__main__':
    mysqlCli = db.MysqlClient()
    main()