#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import math
from urllib.parse import quote
import json
import re

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

def get_detail(html,replyCount,title,saveUrl):
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
            with open(saveFileName+'.csv','a',encoding='gbk',errors='ignore') as f:
            # with open(saveFileName+'.csv','a',encoding='utf8',errors='ignore') as f:
                f.write(save_res)
        except:
            continue



def deal(html):
    urls = html.xpath('//ul[@id="thread_list"]/li//a[@class="j_th_tit "]/@href')
    for url in urls:
        try:
            saveUrl = 'http://tieba.baidu.com' + url
            link = 'http://tieba.baidu.com' + url
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
            get_detail(html,replyCount,title,saveUrl)

            #处理剩余页数
            for i in range(2,totalPage+1):
                try:
                    print('帖子当前页：'+str(i))
                    pagelink = link +'?pn='+str(i)
                    print(pagelink)
                    response = requests.get(pagelink,timeout=10)
                    html = HTML(response.text)
                    get_detail(html,replyCount,title,saveUrl)
                except:
                    continue
        except:
            continue


def start(item):
    pageToken = 0
    url = 'http://tieba.baidu.com/f?kw={kw}&pn={pageToken}'.format(kw=item,pageToken=pageToken)
    print(url)
    response = requests.get(url,timeout=10)
    html = HTML(response.text)

    #获取总数
    totalCount = html.xpath('string(//div[@class="th_footer_l"]/span[1]/text())')
    totalPage = math.ceil(int(totalCount)/50)
    print('贴吧总数：'+str(totalCount))
    print('贴吧总页数：'+str(totalPage))

    #处理第一页
    deal(html)

    #处理剩余页数
    for i in range(1,totalPage+1):
        try:
            print('当前列表页：'+str(i))
            pageToken = i*50
            url = 'http://tieba.baidu.com/f?kw={kw}&pn={pageToken}'.format(kw=item, pageToken=pageToken)
            print(url)
            response = requests.get(url,timeout=10)
            html = HTML(response.text)
            deal(html)
        except:
            continue




if __name__ == '__main__':

    saveFileName = '顺丰'
    tieba_list = ['顺丰']

    with open(saveFileName+'.csv','w',encoding='gbk',errors='ignore') as f:
    # with open(saveFileName+'.csv','w',encoding='utf8',errors='ignore') as f:
        f.write('链接,回复数,标题,姓名,等级,吧龄,发帖数,正文,发布时间,楼层数\n')
    for item in tieba_list:
        start(item)