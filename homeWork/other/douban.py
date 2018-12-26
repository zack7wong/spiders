#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
from lxml.etree import HTML

with open('results.csv', 'a') as f:
    save_res = '序号,电影名,评论者,时间,标题,内容,点赞,踩,回复\n'
    f.write(save_res)


num = 1
for i in range(0,3):
    URL = 'https://movie.douban.com/review/best/?start={page}'

    response = requests.get(URL.format(page=i*20))
    html = HTML(response.text)

    names = html.xpath('//div[@class="review-list chart "]//a[@class="subject-img"]/img/@alt')
    commenters = html.xpath('//div[@class="review-list chart "]//a[@class="name"]/text()')
    times = html.xpath('//div[@class="review-list chart "]//span[@class="main-meta"]/text()')
    titles = html.xpath('//div[@class="review-list chart "]//h2/a/text()')
    mycontents = html.xpath('//div[@class="review-list chart "]//div[@class="short-content"]/text()')
    contents = []
    for cont in mycontents:
        cont = cont.strip()
        cont = cont.replace(' ','').replace('\n','').replace('... (','')
        if cont != '' and cont !=')':
            contents.append(cont)
    likes = html.xpath('//div[@class="review-list chart "]//a[@class="action-btn up"]/span/text()')
    unlikes = html.xpath('//div[@class="review-list chart "]//a[@class="action-btn down"]/span/text()')
    replys = html.xpath('//div[@class="review-list chart "]//a[@class="reply"]/text()')

    # print(names)
    # print(commenters)
    # print(times)
    # print(titles)
    # print(contents)
    # print(len(contents))
    #
    # print(likes)
    # print(unlikes)
    # print(replys)

    # print(len(contents))
    # for cont in contents:
    #     print(cont)

    for name,commenter,time,title,content,like,unlike,reply in zip(names,commenters,times,titles,contents,likes,unlikes,replys):
        title = title.replace('\n','').replace(',','，')
        content = content.replace('\n','').replace(',','，').replace(' ','')
        like = like.strip()
        unlike = unlike.strip()
        reply = reply[:-2]
        print(name,commenter,time,title,content,like,unlike,reply)
        save_res = str(num)+','+name+','+commenter+','+time+','+title+','+content+','+like+','+unlike+','+reply+'\n'
        with open('results.csv','a') as f:
            f.write(save_res)
        num+=1
