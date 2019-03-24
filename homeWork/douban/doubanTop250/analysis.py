#!/usr/bin/env python
# -*- coding:utf-8 -*-

import db
import matplotlib.pyplot as plt
import jieba
from os import path
from wordcloud import WordCloud
import numpy as np
from PIL import Image


def scoreRank(results):
    rank_list = []
    name_list = []
    rating_list = []
    for res in results:
        rank_list.append(int(res[2]))
        name_list.append(res[3])
        rating_list.append(float(res[11]))

    plt.scatter(rank_list, rating_list, alpha=0.6)  # 绘制散点图，透明度为0.6
    plt.savefig("评分与排名散点图.jpg")
    plt.show()


def timeRank(results):
    rank_list = []
    name_list = []
    rating_list = []
    for res in results:
        rank_list.append(int(res[2]))
        name_list.append(res[3])
        rating_list.append(float(res[14]))
    plt.scatter(rank_list, rating_list, alpha=0.6)  # 绘制散点图，透明度为0.6
    plt.savefig("电影时长与排名散点图.jpg")
    plt.show()


def commentRank(results):
    rank_list = []
    name_list = []
    rating_list = []
    for res in results:
        rank_list.append(int(res[2]))
        name_list.append(res[3])
        rating_list.append(float(res[12]))

    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.bar(rank_list, rating_list, tick_label=name_list)
    plt.savefig("评论数与排名柱状图.jpg")
    plt.show()

def yearRank(results):
    rank_list = []
    name_list = []
    rating_list = []
    for res in results:
        try:
            saveYear = float(res[8].split('-')[0])
            rating_list.append(saveYear)
            rank_list.append(int(res[2]))
            name_list.append(res[3])
        except:
            continue

    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.plot(rank_list, rating_list)
    plt.savefig("上映年份和排名折线图.jpg")
    plt.show()



def area(results):
    item_list = []
    account_list = []
    for res in results:
        try:
            myarea = res[9].split('/')[0]
        except:
            continue

        if myarea in account_list:
            for item in item_list:
                if item['key'] == myarea:
                    item['value'] += 1
                    break
        else:
            account_list.append(myarea)
            obj = {
                'key': myarea,
                'value': 1
            }
            item_list.append(obj)

    name_list = []
    num_list = []
    for item in item_list:
        name_list.append(item['key'])
        num_list.append(item['value'])


    plt.pie(num_list, labels=name_list, autopct='%1.2f%%')  # 画饼图
    plt.savefig("不同上映地区影片数量分布饼图.jpg")
    plt.show()

def language(results):
    item_list = []
    account_list = []
    for res in results:
        try:
            myarea = res[15].split('/')[0]
        except:
            continue

        if myarea in account_list:
            for item in item_list:
                if item['key'] == myarea:
                    item['value'] += 1
                    break
        else:
            account_list.append(myarea)
            obj = {
                'key': myarea,
                'value': 1
            }
            item_list.append(obj)

    name_list = []
    num_list = []
    for item in item_list:
        name_list.append(item['key'])
        num_list.append(item['value'])


    plt.pie(num_list, labels=name_list, autopct='%1.2f%%')  # 画饼图
    plt.savefig("不同语言影片数分布饼图.jpg")
    plt.show()

def typeMovie(results):
    item_list = []
    account_list = []
    for res in results:
        try:
            myarea = res[10].split('|')[0]
        except:
            continue

        if myarea in account_list:
            for item in item_list:
                if item['key'] == myarea:
                    item['value'] += 1
                    break
        else:
            account_list.append(myarea)
            obj = {
                'key': myarea,
                'value': 1
            }
            item_list.append(obj)

    name_list = []
    num_list = []
    for item in item_list:
        name_list.append(item['key'])
        num_list.append(item['value'])

    plt.bar(name_list, num_list, tick_label=name_list)
    plt.savefig("不同类型电影柱状图.jpg")
    plt.show()

def ciyun(results):
    book_Str = ''
    for res in results:
        bookName = res[13]
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
    plt.savefig("描述词云图.jpg")
    plt.show()



def start():
    sql = "select * from info"
    results = dbCli.find_all(sql)
    plt.rcParams['font.sans-serif'] = 'SimHei'

    # scoreRank(results)
    # timeRank(results)
    # commentRank(results)
    yearRank(results)
    area(results)
    language(results)
    typeMovie(results)
    ciyun(results)

if __name__ == '__main__':
    dbCli = db.MysqlClient()
    start()
