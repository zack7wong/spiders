#!/usr/bin/env python
# -*- coding:utf-8 -*-

from snownlp import SnowNLP
import db

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

if __name__ == '__main__':
    mysqlCli = db.MysqlClient()
    start()