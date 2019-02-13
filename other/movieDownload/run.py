#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import urllib
import re
import os

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    # 'Cookie': "ASP.NET_SessionId=gvj5dbb0z2xjhpkdarkdowkv;",
              # "ASP.NET_SessionId=gvj5dbb0z2xjhpkdarkdowkv; UM_distinctid=168dfc3f82d103-01fd5b1b82ab77-10376654-1fa400-168dfc3f82e1fe; LoginInfo=userEmail=546094038@qq.com&userName=zrx2011&userpass=72511; CNZZDATA1000377994=227412378-1549942388-%7C1550018383; "
    'Host': "www.lavafox.com",
    'Pragma': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
}

def read_txt():
    item_list = []
    with open('mid.txt') as f:
        results = f.readlines()
        for res in results[1:]:
            mid = res.split(' ')[0]
            sid = res.split(' ')[1].strip()
            obj = {
                'mid':mid,
                'sid':sid,
            }
            item_list.append(obj)
    return item_list

def login():
    global headers
    print('正在登录。。')

    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['X-Requested-With'] = 'XMLHttpRequest'

    url = 'https://www.lavafox.com/Handler/register-form.ashx'
    body = 'qlemail=546094038@qq.com&action=valid_email&email=546094038@qq.com'
    response = requests.post(url, headers=headers, data=body, timeout=15)
    mycookie = response.cookies.get_dict()
    NET_SessionId = mycookie['ASP.NET_SessionId']
    print(NET_SessionId)
    print(response.text)
    headers['Cookie'] = 'ASP.NET_SessionId='+NET_SessionId


    body = 'action=login&lemail=546094038@qq.com&lpwd=682565&lrme=0'
    response = requests.post(url, headers=headers, data=body, timeout=15)
    print(response.text)
    del headers['Content-Type']
    del headers['X-Requested-With']
#     用户名546094038@qq.com
# 密码682565

def get_words(item):
    print('\n正在处理单词。。')
    start_url = 'https://www.lavafox.com/study-words.aspx?Mid={mid}&&Sid={sid}'
    url = start_url.format(mid=item['mid'],sid=item['sid'])
    print('单词url：'+url)
    response = requests.get(url, headers=headers, timeout=15)
    # print(response.text)
    html = HTML(response.text)
    article_html = html.xpath('//article[@class="post post-large"]')
    chuchu = html.xpath('string(//section[@class="page-top"]//h2/font/a/text())').replace('（','').replace('）','')
    print(chuchu)
    for article in article_html:
        word = article.xpath('string(.//h2/text())')
        yinbiao = article.xpath('string(.//h2/a/text())').strip()
        content = article.xpath('.//p[1]/text()')
        content = ''.join(content)
        english = article.xpath('string(.//div[@style="font-size:16px;color:#333;"]/a/text())').strip()
        chinese = article.xpath('string(.//div[@class="post-content"]/div[last()]/text())').strip()
        english_chinese = english+chinese
        audio_url = 'https://www.lavafox.com/'+article.xpath('string(.//div[@style="font-size:16px;color:#333;"]//source/@src)').strip()
        # audio_url = 'https://www.lavafox.com/'+article.xpath('string(.//audio/source/@src)').strip()
        print(word)
        print(yinbiao)
        print(content)
        print(english)
        print(chinese)
        # print(audio_url)

        save_res = url+'||'+word+'||'+chuchu+'||'+yinbiao+'||'+content+'||'+english_chinese+'||'+audio_url
        save_res = save_res.replace(',','，').replace('\n','').replace('||',',')+'\n'
        with open('words.csv','a',encoding='gbk',errors='ignore') as f:
            f.write(save_res)

        #下载音频

        fileName = re.search('https://www.lavafox.com/images/(sound|mp3)/(.*?).mp3',audio_url)
        if fileName:
            fileName = fileName.group(2)
            fileName = fileName + '.mp3'
            print('正在下载单词音频：'+fileName)
            LocalPath = os.path.join('audio', fileName)
            urllib.request.urlretrieve(audio_url, LocalPath)

def get_movies(item):
    print('\n正在处理视频。。')
    start_url = 'https://www.lavafox.com/study-movie.aspx?Mid={mid}&&Sid={sid}'
    url = start_url.format(mid=item['mid'], sid=item['sid'])
    print('视频url：' + url)
    response = requests.get(url, headers=headers, timeout=15)
    # print(response.text)
    html = HTML(response.text)
    chuchu = html.xpath('string(//section[@class="page-top"]//h2/font/a/text())').replace('（', '').replace('）', '')
    print(chuchu)
    movie_url = html.xpath('string(//video/source/@src)')
    print(movie_url)

    save_res = url + '||' + chuchu + '||' + movie_url
    save_res = save_res.replace(',', '，').replace('\n', '').replace('||', ',') + '\n'
    with open('movies.csv', 'a', encoding='gbk', errors='ignore') as f:
        f.write(save_res)

    # 下载视频
    fileName = re.search('https://www.lavafox.com/images/partVideo/(.*?).mp4', movie_url).group(1)
    fileName = fileName + '.mp4'
    print('正在下载视频：' + fileName)
    LocalPath = os.path.join('movie', fileName)
    urllib.request.urlretrieve(movie_url, LocalPath)

def get_sentences(item):
    print('\n正在处理句子。。')
    start_url = 'https://www.lavafox.com/study-talk.aspx?Mid={mid}&&Sid={sid}'
    url = start_url.format(mid=item['mid'], sid=item['sid'])
    print('句子url：' + url)
    response = requests.get(url, headers=headers, timeout=15)
    # print(response.text)
    html = HTML(response.text)
    article_html = html.xpath('//article[@class="post post-large"]')
    chuchu = html.xpath('string(//section[@class="page-top"]//h2/font/a/text())').replace('（', '').replace('）', '')
    print(chuchu)
    for article in article_html:
        english = article.xpath('string(.//h2/a/text())').strip()
        chinese = article.xpath('.//div[@class="post-content"]/p/text()')
        chinese = ''.join(chinese).strip()
        audio_url = 'https://www.lavafox.com/' + article.xpath('string(.//audio/source/@src)').strip()
        print(english)
        print(chinese)
        # print(audio_url)

        save_res = url + '||' + english  + '||' + chinese + '||' + chuchu + '||' + audio_url
        save_res = save_res.replace(',', '，').replace('\n', '').replace('||', ',') + '\n'
        with open('sentences.csv', 'a', encoding='gbk', errors='ignore') as f:
            f.write(save_res)

        # 下载句子音频
        # fileName = re.search('https://www.lavafox.com/images/sound/(.*?).mp3', audio_url).group(1)
        fileName = re.search('https://www.lavafox.com/images/(sound|mp3)/(.*?).mp3', audio_url).group(2)
        fileName = fileName + '.mp3'
        print('正在下载句子音频：' + fileName)
        LocalPath = os.path.join('audio', fileName)
        urllib.request.urlretrieve(audio_url, LocalPath)

def start(item):
    get_words(item)
    get_sentences(item)
    get_movies(item)


if __name__ == '__main__':
    with open('words.csv', 'w', encoding='gbk') as f:
        f.write('链接,单词,出处,音标,中文涵义,例句,例句音频地址\n')

    with open('movies.csv', 'w', encoding='gbk') as f:
        f.write('链接,出处,视频地址\n')

    with open('sentences.csv', 'w', encoding='gbk') as f:
        f.write('链接,英文句子,中文解释,出处,音频地址\n')


    login()
    item_list = read_txt()
    for item in item_list:
        start(item)