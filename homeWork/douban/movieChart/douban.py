#!/usr/bin/env python
# -*- coding:utf-8 -*-


#导入包
import requests
from lxml.etree import HTML
import urllib
import re
import matplotlib.pyplot as plt
import os
import time as ttime
from pyecharts import Bar
from pylab import *
from pyecharts import Line,configure

#中文字体显示
# mpl.rcParams['font.sans-serif'] = ['SimHei']
# mpl.rcParams['font.sans-serif'] = ['PingFang']
# myfont = matplotlib.font_manager.FontProperties(fname=r'/System/Library/Fonts/PingFang.ttc')
# myfont = matplotlib.font_manager.FontProperties(fname=r'C:\Windows\Fonts\SimHei.ttf')

#起始url

url = 'https://movie.douban.com/chart'
response = requests.get(url)

#lxml解析结果

html = HTML(response.text)
urls = html.xpath('//html//div[1]/table//td[@valign="top"]/a/@href')
titles = html.xpath('//html//div[1]/table//td[@valign="top"]/a/@title')
imgs = html.xpath('//html//div[1]/table//td[@valign="top"]/a/img/@src')
time_and_names = html.xpath('//html//div[1]/table//td[@valign="top"]/div/p/text()')
pingfens = html.xpath('//html//div[1]/table//td[@valign="top"]/div/div/span[2]/text()')
pingjias = html.xpath('//html//div[1]/table//td[@valign="top"]/div/div/span[3]/text()')

#debug测试

# print(response.text)
# print(urls)

# print(titles)
# print(time_and_names)
# print(pingfens)
# print(pingjias)

#结果集

title_list = []
img_obj_list = []
pingjia_list = []

#初始化写文件

with open('results.csv', 'w') as f:
    f.write('')

#数据拼接

for url,title,img,name,pingfen,pingjia in zip(urls,titles,imgs,time_and_names,pingfens,pingjias):

    #id 正则匹配

    id = re.search('https://movie.douban.com/subject/(\d+)/',url)
    if id:
        id = id.group(1)

    #时间的数据清洗
    time = name.split('/')[0]
    time = time.split('(')[0]

    #演员表的数据清洗

    myname = name.split('/')[1:]
    myname = '/'.join(myname)
    myname = myname.replace(',','，')

    #标题去除逗号分隔符

    title = title.replace(',','，')

    pingjia = pingjia.split('(')[1]
    pingjia = pingjia.split('人')[0]

    #添加到要图表展示的数据

    title_list.append(title)
    pingjia_list.append(int(pingjia))

    #图片下载对象

    obj = {
        'url':img,
        'id':id,
    }

    img_obj_list.append(obj)

    # print(id,url, title, time, myname, pingfen, pingjia)
    save_res = id+','+url+','+title+','+time+','+myname+','+pingfen+','+ pingjia+'\n'
    print(save_res)

    #写文件

    with open('results.csv','a') as f:
        f.write(save_res)


#柱形图
# print(title_list)
# print(pingjia_list)
bar = Bar("柱形图",background_color = 'white',title_text_size = 5,width=2500)
bar.add("豆瓣",title_list,pingjia_list)
bar.show_config()
bar.render(path = 'a.html')

# x = title_list
# y = pingjia_list
# plt.bar(range(len(y)), y,tick_label=x)
# plt.show()

#折线图

line =Line('折线图',background_color = 'white',title_text_size = 5,width=2500)
attr = title_list
v1 = pingjia_list
line.add('豆瓣',attr,v1,mark_line=['average'],is_label_show = True)
line.render(path = 'b.html')

# plt.figure()
# plt.plot(x,y)
# plt.show()

# plt.plot([1, 2, 3], [4, 5, 6])
# plt.xlabel("横轴",fontproperties=myfont)
# plt.ylabel("纵轴",fontproperties=myfont)
# plt.title("pythoner.com",fontproperties=myfont)
# # legend(['图例'],prop=myfont)

# plt.show()

#下载图片

for imgobj in img_obj_list:
    print(imgobj)

    #获取路劲
    thisPath = os.getcwd()
    thisPath = os.path.join(thisPath+'/img/')
    filename = str(imgobj['id'])+'.jpg'

    #路径拼接
    thisPath = thisPath + filename
    # print(thisPath)

    #下载图片
    urllib.request.urlretrieve(imgobj['url'],filename=thisPath)