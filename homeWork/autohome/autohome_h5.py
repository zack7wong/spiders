#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import re
import json
from lxml import etree
from urllib.parse import unquote_plus
import random

# 汽车之家的需要爬取秦论坛，帖子内容，发帖时间，是否精华，作者，点击量，回复量和回复内容

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Cookie': "CYHTooltip=1; __ah_uuid=263BA464-4B46-4693-ACD3-A29CFF356EC8; fvlid=1547109859431cf0wlckp52; sessionid=5BFF7CEB-1ADB-45D1-9C2F-54DD96B33089%7C%7C2019-01-10+16%3A44%3A27.228%7C%7C0; ahpau=1; area=440305; historybbsName4=c-2761%7C%E7%A7%A6%2Cc-2733%7C%E5%A5%A5%E8%BF%AARS; UM_distinctid=1684bfe1a0f163-09a82743f3ba43-10376654-1fa400-1684bfe1a107a5; CNZZDATA1262640694=597270780-1547460849-https%253A%252F%252Fclub.autohome.com.cn%252F%7C1547460849; ASP.NET_SessionId=2ift50va4wgxontlfoyckfad; autoac=247A21D6A2581BAA247369B962602B6E; autotc=F8A11D4B87CCB2A0098D56769842448F; pvidchain=101061; sessionip=121.35.102.25; sessionvid=458D4941-FE31-44D7-B043-5418967EEF00; clubUserShow=55335774|692|2|%E6%B8%B8%E5%AE%A2|0|0|0||2019-01-15+11%3A43%3A01|0; clubUserShowVersion=0.1; papopclub=32E5E058BC67506B0BE2660A1997D0E3; pbcpopclub=0c2e1852-c646-48ee-bb10-6f97b172a15a; pepopclub=0DC064BDE5D71E43E0C944A829B1596D; ahpvno=24; ref=0%7C0%7C0%7C0%7C2019-01-15+11%3A43%3A47.113%7C2019-01-10+16%3A44%3A27.228",
    'Host': "club.autohome.com.cn",
    'Pragma': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "17408e9f-3981-4f0d-ab0c-25c6a3b713a8"
}

def get_comment(detail_response,commentStr):
    # print(commentStr)
    text = detail_response.text
    variables = re.findall("var (\w{3})='(.)';", text)
    var_tables = {each[0]: each[1] for each in variables}
    target_script = re.search('<div class="content conttxt".+?<script>(.+?\(document\);)</script>', text, re.DOTALL)
    need_decrypt_results = re.search("\[''\+(.+?)\]\(''\+(.+?)\+\w{3}\(''\)\);.+?''\+(.+?)\)", target_script.group(1))
    target_method, target_text, target_loc = decrypt_text(var_tables, need_decrypt_results.group(1)), \
                                             decrypt_text(var_tables, need_decrypt_results.group(2)), \
                                             decrypt_text(var_tables, need_decrypt_results.group(3))

    assert target_method == "decodeURIComponent"
    target_text = unquote_plus(target_text)
    target_loc = [int(i) for i in target_loc.split(";")]
    # print(repr(target_method), repr(target_text), repr(target_loc))
    ret_str_lst = []
    unformatted_content_html = re.search('<p class="rrlycontxt".+?<div class="reply-handle"', commentStr, re.DOTALL)
    if unformatted_content_html:
        unformatted_content_html = unformatted_content_html.group(0)
    else:
        return None
    unformatted_content_text_groups = re.findall(">([^\s<>]+)<|(\"hs_kw(\d).+?\"/)", unformatted_content_html, re.DOTALL)
    for each in unformatted_content_text_groups:
        if each[0]:
            ret_str_lst.append(each[0])
        elif each[1]:
            next_loc_index = int(each[2])
            next_text_index = target_loc[next_loc_index]
            ret_str_lst.append(target_text[next_text_index])
    result = "".join(ret_str_lst)

    return result


def get_content(detail_response):
    text = detail_response.text
    # print(text)
    variables = re.findall("var (\w{3})='(.)';", text)
    var_tables = {each[0]: each[1] for each in variables}
    target_script = re.search('<div class="content conttxt".+?<script>(.+?\(document\);)</script>', text, re.DOTALL)
    need_decrypt_results = re.search("\[''\+(.+?)\]\(''\+(.+?)\+\w{3}\(''\)\);.+?''\+(.+?)\)", target_script.group(1))
    target_method, target_text, target_loc = decrypt_text(var_tables, need_decrypt_results.group(1)), \
                                             decrypt_text(var_tables, need_decrypt_results.group(2)), \
                                             decrypt_text(var_tables, need_decrypt_results.group(3))

    assert target_method == "decodeURIComponent"
    target_text = unquote_plus(target_text)
    target_loc = [int(i) for i in target_loc.split(";")]
    # print(repr(target_method), repr(target_text), repr(target_loc))
    ret_str_lst = []
    unformatted_content_html = re.search('<div class="content conttxt".+?<script>', text, re.DOTALL).group(0)
    unformatted_content_text_groups = re.findall(">([^\s<>]+)<|('hs_kw(\d).+?'>)", unformatted_content_html, re.DOTALL)
    for each in unformatted_content_text_groups:
        if each[0]:

            ret_str_lst.append(each[0])
        elif each[1]:
            next_loc_index = int(each[2])
            next_text_index = target_loc[next_loc_index]
            ret_str_lst.append(target_text[next_text_index])
    result = "".join(ret_str_lst)

    return result

def decrypt_text(var_tables, text):
    text = text.split("+")
    ret_lst = []
    for each in text:
        ret_lst.append(var_tables[each])
    return "".join(ret_lst)

def parse(link,detail_response):
    html = HTML(detail_response.text)
    # print(detail_response.text)
    id = re.search('https://club.m.autohome.com.cn/bbs/thread/(.*?)/(\d+)-1.html',link).group(2)
    url = link

    if html.xpath('string(//em[@class="mark-tu"])') == '精':
        jinghua = '是'
    else:
        jinghua = '否'
    userName = html.xpath('string(//a[@class="user-name"])').strip()
    title = html.xpath('string(//title)').replace('_秦论坛_手机汽车之家','').strip()
    publishDate = html.xpath('string(//time)').strip()
    replyCount = html.xpath('string(//span[@id="replys"])').strip()
    clickCount = html.xpath('string(//span[@id="views"])').strip()
    content = get_content(detail_response).replace('&nbsp;','')

    #获取评论
    commentEtreeList = html.xpath('//section[@id="reply-wrap"]/section')
    all_comment_list = []
    for eachEtree in commentEtreeList:
        try:
            commentStr = etree.tostring(eachEtree, encoding="utf-8").decode('utf8')
            commentContent = get_comment(detail_response,commentStr)
            if commentContent:
                all_comment_list.append(commentContent)
            # with open('comment.csv','a') as f:
            #     commentRes = id +','+commentContent.replace(',','，').replace('\n', ' ').strip()+'\n'
            #     f.write(commentRes)
        except:
            print('评论获取出错')
            continue
    all_comment_list = '----'.join(all_comment_list).replace(',','，')

    #吸入
    save_res = id + '||' + url + '||' + userName + '||' + title + '||' + jinghua + '||' + clickCount + '||' + replyCount + '||' + content + '||' + publishDate+'||'
    save_res = save_res.replace(',', '，').replace('\n', ' ').replace('\r', ' ').replace('||',',').strip() + all_comment_list+'\n'
    print(save_res)
    with open('post.csv', 'a', encoding='utf8', errors='ignore') as f:
        f.write(save_res)

def start():
    headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cache-Control': "no-cache",
        'Connection': "keep-alive",
        # 'Cookie': "__ah_uuid=263BA464-4B46-4693-ACD3-A29CFF356EC8; fvlid=1547109859431cf0wlckp52; sessionid=5BFF7CEB-1ADB-45D1-9C2F-54DD96B33089%7C%7C2019-01-10+16%3A44%3A27.228%7C%7C0; ahpau=1; historybbsName4=c-2761%7C%E7%A7%A6%2Cc-2733%7C%E5%A5%A5%E8%BF%AARS; UM_distinctid=1684bfe1a0f163-09a82743f3ba43-10376654-1fa400-1684bfe1a107a5; pbcpopclub=504a2d68-dc94-40a2-9ab9-c830958b26fe; sessionuid=5BFF7CEB-1ADB-45D1-9C2F-54DD96B33089%7C%7C2019-01-10+16%3A44%3A27.228%7C%7C0; __utmc=1; live-voteid=pc568003659713411056; __utma=1.1482135073.1547550058.1547550058.1547608811.2; __utmz=1.1547608811.2.2.utmcsr=club.autohome.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; isFromBD=; sessionvid=80A4FE71-CC04-4A66-9EF3-513130A1129A; historyClub=2761; pvidchain=101762,3460109,101762,3460109,101762,3460109,101762,3460109,3460109; pmpopclub=5795222ECE75A74D44E468F1FB16E406; autoac=7EA89D3DA5B6FCCBA246E850B0916168; autotc=EBD4390513E59244D83604C864C1E232; ahpvno=62; sessionip=59.59.86.220; ref=blog.csdn.net%7C0%7C2112108%7Cwww.cnblogs.com%7C2019-01-16+17%3A02%3A15.086%7C2019-01-16+12%3A05%3A02.229; area=350602",
        'Host': "club.m.autohome.com.cn",
        'Pragma': "no-cache",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36",
        'cache-control': "no-cache",
    }

    for i in range(1,3361):
        proxies = {
            'http': 'http://JIANYIHTT' + str(random.randint(1, 20)) + ':KIFKOYY84J@http-proxy-t1.dobel.cn:9180',
            'https': 'http://JIANYIHTT' + str(random.randint(1, 20)) + ':KIFKOYY84J@http-proxy-t1.dobel.cn:9180',
        }

        print('当前页：'+str(i))
        start_url = 'https://club.m.autohome.com.cn/Adaptive/Forum/GetTopicListPartial?bbs=c&bbsid=2761&pageindex={pageToken}&type=&sort=&qaType='.format(pageToken=i)
        print(start_url)
        try:
            response = requests.get(start_url,verify=False,timeout=10,headers=headers,proxies=proxies)
            # print(response.text)
            html = HTML(response.text)
            url_list = html.xpath('//body/li/a/@href')

            for url in url_list:

                proxies = {
                    'http': 'http://JIANYIHTT' + str(random.randint(1, 20)) + ':KIFKOYY84J@http-proxy-t1.dobel.cn:9180',
                    'https': 'http://JIANYIHTT' + str(
                        random.randint(1, 20)) + ':KIFKOYY84J@http-proxy-t1.dobel.cn:9180',
                }

                link = 'https://club.m.autohome.com.cn'+url
                print(link)
                try:
                    detail_response = requests.get(link,verify=False,timeout=10,headers=headers,proxies=proxies)
                    parse(link,detail_response)
                except:
                    print('详情页错误')
                    with open('详情错误.txt','a') as f:
                        f.write(str(link)+'\n')
                    continue
        except:
            print('列表页错误')
            with open('列表页.txt','a') as f:
                f.write(start_url+'\n')
            continue


        # print('当前页：' + str(i))
        # start_url = 'https://club.m.autohome.com.cn/Adaptive/Forum/GetTopicListPartial?bbs=c&bbsid=2761&pageindex={pageToken}&type=&sort=&qaType='.format(pageToken=i)
        # print(start_url)
        # response = requests.get(start_url, verify=False)
        # # print(response.text)
        # html = HTML(response.text)
        # url_list = html.xpath('//body/li/a/@href')
        #
        # for url in url_list:
        #     link = 'https://club.m.autohome.com.cn' + url
        #     print(link)
        #
        #     proxies = {
        #         'http':'http://JIANYIHTT'+str(random.randint(1,20))+':KIFKOYY84J@http-proxy-t1.dobel.cn:9180',
        #         'https':'http://JIANYIHTT'+str(random.randint(1,20))+':KIFKOYY84J@http-proxy-t1.dobel.cn:9180',
        #     }
        #
        #     detail_response = requests.get(link,proxies=proxies, headers=headers, verify=False)
        #     parse(link, detail_response)
        #     exit()

if __name__ == '__main__':
    with open('post.csv','w') as f:
        f.write('id,url,用户名,标题,是否精华,点击数,回复数,内容,发布时间,评论内容\n')
    start()