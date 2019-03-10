#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import math
from urllib.parse import quote
import json
import re
import multiprocessing

set_id_list = []

def get_tieziReply(tid,pid):
    try:
        pageToken =1
        tieziReply = 'https://tieba.baidu.com/p/comment?tid={tid}&pid={pid}&pn={pageToken}'.format(tid=tid,pid=pid,pageToken=pageToken)
        # print(tieziReply)
        response = requests.get(tieziReply,timeout=10)
        html = HTML(response.text)
        totalPage = html.xpath('string(//p[@class="j_pager l_pager pager_theme_2"]/a[last()]/@href)')
        if totalPage == '':
            totalPage = 1
        else:
            totalPage = int(totalPage.replace('#',''))
        # print(totalPage)

        #处理第一页
        allStr_list1 = html.xpath('//li//span[@class="lzl_content_main"]/text()')

        #处理剩余页数
        allStr_list2 = []
        for i in range(2,totalPage+1):
            try:
                tieziReply = 'https://tieba.baidu.com/p/comment?tid={tid}&pid={pid}&pn={pageToken}'.format(tid=tid, pid=pid,pageToken=i)
                response = requests.get(tieziReply,timeout=10)
                html = HTML(response.text)
                allStr_list2 = html.xpath('//li//span[@class="lzl_content_main"]/text()')
            except:
                continue

        allStr_list = allStr_list1+allStr_list2
        saveList = []
        for each in allStr_list:
            if each == '        回复 ':
                continue
            if each == '        ':
                continue
            each = each.strip()
            if each == '':
                continue

            each = each.replace(',', '，').replace('\n', ' ').replace('\r', ' ').strip()
            each = re.sub('.*?回复.*?：','',each)
            if each[0] == ' :':
                each = each[1:]
            saveList.append(each)

        allStr = '|||'.join(saveList)
    except:
        allStr = ''
    return allStr

def get_detail(html,replyCount,title,saveUrl,writeNum):
    div_list = html.xpath('//div[@id="j_p_postlist"]/div')

    for div in div_list:
        try:
            thisInfo = div.xpath('string(./@data-field)')
            # print(thisInfo)
            this_json_obj = json.loads(thisInfo)

            floor = str(this_json_obj['content']['post_no'])
            try:
                publishDate = str(this_json_obj['content']['date'])
            except:
                publishDate = div.xpath('string(//div[@class="post-tail-wrap"]/span[last()]/text())')


            # userName = div.xpath('string(.//li[@class="d_name"]/a/text())')

            really_user_name = this_json_obj['author']['user_name']
            userName = this_json_obj['author']['user_nickname'] if this_json_obj['author']['user_nickname'] else really_user_name
            level = div.xpath('string(.//div[@class="d_badge_lv"])')
            contentList = div.xpath('.//div[@class="d_post_content j_d_post_content  clearfix"]/text()|.//div[@class="d_post_content j_d_post_content "]/text()')
            content = ''.join(contentList).replace(',','，').replace('\n',' ').replace('\r',' ').strip()

            # print(userName)
            # print(level)
            # print(content)

            #获取用户信息
            if really_user_name == None:
                continue
            userUrl = 'http://tieba.baidu.com/home/get/panel?ie=utf-8&un='+quote(really_user_name)
            response = requests.get(userUrl,timeout=10)
            # print(response.text)
            json_obj = json.loads(response.text)
            user_year = str(json_obj['data']['tb_age'])
            user_postNum = str(json_obj['data']['post_num'])

            # print(user_year)
            # print(user_postNum)

            #获取帖子回复
            # tid = this_json_obj['content']['thread_id']
            tid = re.search('http://tieba.baidu.com/p/(\d+)',saveUrl).group(1)
            pid = this_json_obj['content']['post_id']
            allStr = get_tieziReply(tid,pid)


            save_res = saveUrl+'|||'+str(replyCount)+'|||'+title+'|||'+userName+'|||'+str(level)+'|||'+user_year+'|||'+user_postNum+'|||'+content+'|||'+publishDate+'|||'+floor+'|||'+allStr
            save_res = save_res.replace(',','，').replace('\n',' ').replace('\r',' ').replace('|||',',').strip()+'\n'
            print(save_res)
            with open(saveFileName+str(writeNum)+'.csv','a',encoding='gbk',errors='ignore') as f:
            # with open(saveFileName+'.csv','a',encoding='utf8',errors='ignore') as f:
                f.write(save_res)
        except:
            continue



def deal(urls,num):
    for url in urls:
        try:
            saveUrl = url
            with open(saveFileName+str(num)+'_已采集.txt','a') as f:
                f.write(saveUrl+'\n')
            link = url
            print(link)

            response = requests.get(link,timeout=10)
            html = HTML(response.text)

            #获取总页数
            replyCount = int(html.xpath('string(//li[@class="l_reply_num"]/span[1])')) #回复数
            title = html.xpath('string(//h1/@title|//h3/@title)')                                   #获取标题
            totalPage = int(html.xpath('string(//li[@class="l_reply_num"]/span[2])'))
            print('帖子总页数：'+str(totalPage))


            #处理第一页
            print('当前页数：1')
            get_detail(html,replyCount,title,saveUrl,num)

            #处理剩余页数
            for i in range(2,totalPage+1):
                try:
                    print('帖子当前页：'+str(i))
                    pagelink = link +'?pn='+str(i)
                    print(pagelink)
                    response = requests.get(pagelink,timeout=10)
                    html = HTML(response.text)
                    get_detail(html,replyCount,title,saveUrl,num)
                except:
                    continue
        except:
            continue



if __name__ == '__main__':

    saveFileName = '苏宁快递'
    tieba_list = ['苏宁快递']

    urls = []
    with open(saveFileName+'_urls.txt') as f:
        results = f.readlines()
        for res in results:
            urls.append(res.strip())


    a = int(len(urls) / 10)
    b = a * 2
    c = a * 3
    d = a * 4
    e = a * 5
    f = a * 6
    g = a * 7
    h = a * 8
    i = a * 9
    j = a * 10
    args = (
        (urls[:a],1),
        (urls[a:b],2),
        (urls[b:c],3),
        (urls[c:d],4),
        (urls[d:e],5),
        (urls[e:f],6),
        (urls[f:g],7),
        (urls[g:h],8),
        (urls[h:i],9),
        (urls[i:j],10),
        (urls[j:],11)
    )
    p = multiprocessing.Pool(10)
    for arg in args:
        p.apply_async(deal, args=arg)
    p.close()
    p.join()