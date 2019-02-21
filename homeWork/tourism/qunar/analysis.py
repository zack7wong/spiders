#!/usr/bin/env python
# -*- coding:utf-8 -*-

from snownlp import SnowNLP
import db
import jieba
import re

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from PIL import Image
from os import path
import numpy as np


import jieba.posseg as pseg


def read():
    sql = "select * from qunarComment"
    results = mysqlCli.find_all(sql)
    item_list = []
    for res in results:
        if res[4] == '用户未点评，系统默认好评。':
            continue
        item_list.append(res)
    return item_list

def start():
    results = read()
    for res in results[:100]:
        # print(res)
        content = res[4]
        content = content.replace('&#x20;', ' ').replace('\n', ' ').replace('&#x0A;', ' ').replace('&#x2F;', ' ')

        # # positive的概率 情感分析结果是【0，1】区间上的一个值，越接近1，情感越积极，越接近0，情感越消极

        # s = SnowNLP(content)
        # print('\n'+content)
        # print(s.words)
        # print(s.summary())
        # summaryList = s.summary()
        # endSentiments = 0
        # for summaryStr in summaryList:
        #     each = SnowNLP(summaryStr)
        #     print(summaryStr,each.sentiments)
        #     endSentiments +=each.sentiments
        #
        # endRes = endSentiments/len(summaryList)
        #
        # if 0 <= endRes and endRes < 0.50:
        #     print('差评')
        # else:
        #     print('好评')

        s = SnowNLP(content)
        print('\n'+content)
        print(s.words)
        print(s.sentiments)

        if 0 <= s.sentiments and s.sentiments < 0.50:
            print('差评')
        else:
            print('好评')


    # text = open("b.txt", "rb").read()
    # # 结巴分词
    # wordlist = jieba.cut(text, cut_all=True)
    # wl = " ".join(wordlist)

def fenci():
    all_str = ''
    results = read()
    for res in results[:100]:
        content = res[4]
        all_str+=content
    results = all_str

    #动词副词
    cixing_dic = {'a': '形容词', 'b': '区别词', 'c': '连词', 'd': '副词', 'm': '数词', 'n': '名词', 'p': '介词', 'q': '量词', 'r': '代词',
                  'u': '助词', 'v': '动词'}
    pattern_all_zh = r'([\u4e00-\u9fa5])'
    wudong = re.findall(pattern_all_zh, results, re.S)
    wudong = ''.join(wudong)
    words = pseg.cut(wudong)
    item_list = []
    account_list = []
    for w in words:
        if str(w.flag)[0] in cixing_dic.keys():
            print(w.word, cixing_dic[str(w.flag)[0]])

            if str(w.flag)[0] in account_list:
                for item in item_list:
                    if item['key'] == str(w.flag)[0]:
                        item['value'] += 1
                        break
            else:
                account_list.append(str(w.flag)[0])
                obj = {
                    'key': str(w.flag)[0],
                    'value': 1,
                    'name': cixing_dic[str(w.flag)[0]]
                }
                item_list.append(obj)

    for item in item_list:
        print(item['name'] + ' 有 ' + str(item['value']) + ' 个')

    #统计成语
    wudong_split_res = jieba.cut(wudong, cut_all=False, HMM=True)
    wudong_split_res = " ".join(wudong_split_res)
    wudong_split_res = wudong_split_res.split(' ')
    # print(wudong_split_res)

    item_list = []
    account_list = []
    # print(wudong_split_res)
    for sent in wudong_split_res:
        if len(sent) != 4:
            continue
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

    allnum = 0
    for item in item_list:
        allnum += item['value']
        print('4字词语为 ' + str(item['key']) + ' 的有 ' + str(item['value']) + '个')

def ciyun():
    all_str = ''
    results = read()
    for res in results[:100]:
        content = res[4]
        all_str += content

    text = all_str.encode()
    # 结巴分词
    wordlist = jieba.cut(text, cut_all=True)
    wl = " ".join(wordlist)

    d = path.dirname(__file__)

    alice_mask = np.array(Image.open(path.join(d, "china.jpg")))
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

    plt.savefig('去哪儿词云图.jpg')
    plt.show()


if __name__ == '__main__':
    mysqlCli = db.MysqlClient()
    #情感分析
    start()

    #分词分析
    fenci()

    #词云
    ciyun()