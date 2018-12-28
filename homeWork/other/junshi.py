#!/usr/bin/env python
# -*- coding:utf-8 -*-

#导入包
import requests
import json
from lxml.etree import HTML
from wordcloud import WordCloud
import jieba

#请求url
url = 'http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=10&page={page}&size=20'
# print(response.text)

#翻页
for i in range(1,30):
    host = 'http://www.sohu.com/a/'
    response = requests.get(url=url.format(page=i))
    #解析json数据
    json_obj = json.loads(response.text)
    #for循环遍历
    for data in json_obj:
        authorId = str(data['authorId'])
        id = str(data['id'])
        #拼接url
        link = host+id+'_'+authorId
        print(link)
        #请求详情数据
        detail_response = requests.get(link)
        html = HTML(detail_response.text)
        #xpath解析
        contents = html.xpath('//article[@class="article"]/p/text()')
        content = ''.join(contents)
        print(content)
        with open('结果.txt','a') as f:
            f.write(content+'\n')
# print(results)

# 结巴分词
text = open("结果.txt", "rb").read()
wordlist = jieba.cut(text, cut_all=True)
wl = " ".join(wordlist)
# print(wl)

#处理词频
split_res = wl.split(' ')
print(split_res[:200])
item_list =[]
account_list =[]

for res in split_res:
    #无用数据不进入统计
    if res=='' or res ==' ' or len(res)<=1:
        continue

    #不存在计数列表默认值为1
    if res not in account_list:
        account_list.append(res)
        obj = {
            'key':res,
            'value':1,
        }
        item_list.append(obj)
    #已存在列表中，值加1
    else:
        for each in item_list:
            if res == each['key']:
                each['value']+=1
                break

# print(item_list)
#词频按从大到小排序
sort_list = sorted(item_list,key=lambda x:x['value'],reverse=True)
#输出前5个
print(sort_list[:5])