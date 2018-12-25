#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
from lxml.etree import HTML
import urllib
import re
import matplotlib.pyplot as plt
import os
import time as ttime

from pylab import *
# mpl.rcParams['font.sans-serif'] = ['SimHei']
# mpl.rcParams['font.sans-serif'] = ['PingFang']
# myfont = matplotlib.font_manager.FontProperties(fname=r'/System/Library/Fonts/PingFang.ttc')
# myfont = matplotlib.font_manager.FontProperties(fname=r'C:\Windows\Fonts\SimHei.ttf')

url = 'https://movie.douban.com/chart'
response = requests.get(url)

html = HTML(response.text)
urls = html.xpath('//html//div[1]/table//td[@valign="top"]/a/@href')
titles = html.xpath('//html//div[1]/table//td[@valign="top"]/a/@title')
imgs = html.xpath('//html//div[1]/table//td[@valign="top"]/a/img/@src')
time_and_names = html.xpath('//html//div[1]/table//td[@valign="top"]/div/p/text()')
pingfens = html.xpath('//html//div[1]/table//td[@valign="top"]/div/div/span[2]/text()')
pingjias = html.xpath('//html//div[1]/table//td[@valign="top"]/div/div/span[3]/text()')

# print(response.text)
# print(urls)
# print(titles)
# print(time_and_names)
# print(pingfens)
# print(pingjias)

title_list = []
img_obj_list = []
pingjia_list = []

with open('results.csv', 'w') as f:
    f.write('')

for url,title,img,name,pingfen,pingjia in zip(urls,titles,imgs,time_and_names,pingfens,pingjias):

    id = re.search('https://movie.douban.com/subject/(\d+)/',url)
    if id:
        id = id.group(1)

    time = name.split('/')[0]
    time = time.split('(')[0]
    myname = name.split('/')[1:]
    myname = '/'.join(myname)
    myname = myname.replace(',','，')
    title = title.replace(',','，')

    pingjia = pingjia.split('(')[1]
    pingjia = pingjia.split('人')[0]

    title_list.append(title)
    pingjia_list.append(int(pingjia))

    obj = {
        'url':img,
        'id':id,
    }

    img_obj_list.append(obj)

    # print(id,url, title, time, myname, pingfen, pingjia)
    save_res = id+','+url+','+title+','+time+','+myname+','+pingfen+','+ pingjia+'\n'
    print(save_res)

    with open('results.csv','a') as f:
        f.write(save_res)


#柱形图
x = title_list
y = pingjia_list
plt.bar(range(len(y)), y,tick_label=x)
plt.show()

#折线图
# x=title_list
# y=pingjia_list
time.sleep(2)
plt.figure()
plt.plot(x,y)
plt.show()

# plt.plot([1, 2, 3], [4, 5, 6])
# plt.xlabel("横轴",fontproperties=myfont)
# plt.ylabel("纵轴",fontproperties=myfont)
# plt.title("pythoner.com",fontproperties=myfont)
# # legend(['图例'],prop=myfont)

# plt.show()

#下载图片

for imgobj in img_obj_list:
    print(imgobj)
    thisPath = os.getcwd()
    thisPath = os.path.join(thisPath+'/img/')
    filename = str(imgobj['id'])+'.jpg'
    thisPath = thisPath + filename
    # print(thisPath)
    urllib.request.urlretrieve(imgobj['url'],filename=thisPath)