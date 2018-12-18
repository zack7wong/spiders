#!/usr/bin/env python
# -*- coding:utf-8 -*-

#导入包
import requests
from lxml.etree import HTML

#网页请求相应头
headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Cookie': "log_sid=15449306963294D8AB931576B6922528BA3C77EC4F8FE; BAIDUID=4D8AB931576B6922528BA3C77EC4F8FE:FG=1; BDUSS=W5pYVpHVHJXWEp5MENhWjZYNENibEhrR2dwMG10dXo3QnJURENaUDVLRFVuVHBjQUFBQUFBJCQAAAAAAAAAAAEAAADx1DNYyKHD-9fW1eLDtMTRaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANQQE1zUEBNcZ; Hm_lvt_d0ad46e4afeacf34cd12de4c9b553aa6=1544925294; tracesrc=-1%7C%7C-1; u_lo=0; u_id=; u_t=; u_login=1; userid=1479791857; app_vip=show; Hm_lpvt_d0ad46e4afeacf34cd12de4c9b553aa6=1544930696",
    'Host': "music.taihe.com",
    'Pragma': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'cache-control': "no-cache",
}

#请求url
url = 'http://music.taihe.com/top/dayhot'
#发送请求
response = requests.get(url,headers=headers)
#对结果编码
response.encoding='utf8'
#lxml解析结果
html = HTML(response.text)
#xpath获取歌曲标题
titles = html.xpath('//div[@class="normal-song-list song-list song-list-hook clear song-list-btnBoth  song-list-btnTop song-list-btnBottom"]/ul/li//span[@class="song-title "]/a/text()')
names = html.xpath('//div[@class="normal-song-list song-list song-list-hook clear song-list-btnBoth  song-list-btnTop song-list-btnBottom"]/ul/li//span[@class="author_list"]/@title')
# print(len(titles))
num = 1
#循环遍历
for title,name in zip(titles,names):
    print(str(num)+'  '+name+title.strip())
    #写文件
    with open('music.txt','a',encoding='utf8') as f:
        f.write(str(num)+'  '+name+title.strip()+'\n')
    num+=1