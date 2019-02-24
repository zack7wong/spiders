#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import re
import time
import copy
from hashlib import md5
from urllib.parse import quote

USE_PROXY = False

proxies = {
    'http':'http://127.0.0.1:1087',
    'https':'http://127.0.0.1:1087',
}

start_headers = {
    # 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    # 'Cookie': "M1SH_2132_saltkey=TlWmWRlR; M1SH_2132_lastvisit=1547106198; _ga=GA1.2.2010949758.1547109800; M1SH_2132_ulastactivity=58660HwN9pWCdlZV8Rdon0IJ1T5c%2BzeR6PiH8MhG%2Bcaffx092Z4%2B; M1SH_2132_lastcheckfeed=503430%7C1547110183; M1SH_2132_auth=b338n%2FRXnpc%2B5WqnLuAQra7CuV%2B%2F%2BvohgI4AckL6KcGx0yXo31z5khdcqmzvYulHSfMpfMS9%2BWCqUtSs88kExxOAKsk; Forum_auth=458f2lvV3f3Kit62cxprEkDYwVOV7QTEAEkEKkoyn%2FStbaw30e%2B0uSQtVw; M1SH_2132_nofavfid=1; M1SH_2132_visitedfid=291; M1SH_2132_viewid=tid_12344835; M1SH_2132_smile=1D1; __atuvc=2%7C2; M1SH_2132_fastpostrefresh=1; M1SH_2132_st_p=503430%7C1547111029%7C7ace5dc31fff7d2741a4ad9d27bccc47; M1SH_2132_seccode=16612.47f15ac64b4c638123; tracker=afe3VwvLN3swjpwNfAVRa3am5nhgXQM8Ch1HpL6nnaClTWmIc3qP94fE1kNBrMbD7oqDdz2WNvri509ICu6ove6c; _gid=GA1.2.306610996.1547983763; _fbp=fb.1.1547983764864.1116971272; M1SH_2132_checkpm=1; M1SH_2132_lip=13.229.46.217%2C1547984068; M1SH_2132_sendmail=1; _gat=1; M1SH_2132_sid=yLtcx2; M1SH_2132_lastact=1547984070%09misc.php%09patch; _dc_gtm_UA-46392415-16=1; _td=7abfabef-9bfb-4893-90ee-c416eaefb8b1; _gali=pt",
    'Cookie': "_ga=GA1.2.2010949758.1547109800; __atuvc=2%7C2%2C0%7C3%2C18%7C4; _gid=GA1.2.1662820720.1550463292; _fbp=fb.1.1550463293074.567664784; M1SH_2132_saltkey=VPA8WbhP; M1SH_2132_lastvisit=1550469032; M1SH_2132_sid=lLOoOq; tracker=6cb7%2F0sgI6ZW6nNHo%2BU3EX6nmvU6CH4ofnFV5SSnhL0UAmR%2F67SQlkJyb%2F5eXPGeyJ2NNTPBjdce350; M1SH_2132_sendmail=1; M1SH_2132_seccode=12531.23d08fcb9b430b7857; M1SH_2132_ulastactivity=c3dciqy8mQ5bgZSNANbaX4gS4b5HMu%2FCaHygQo9%2BYLT9XYU6r3aq; M1SH_2132_lastcheckfeed=503430%7C1550472639; M1SH_2132_checkfollow=1; M1SH_2132_lip=13.250.7.111%2C1550472632; M1SH_2132_auth=b2dbR2zxnvMjdHW844Gji9U%2BGvRhxRN%2BBeK54lOHmebWsDcsSdBXhmDC0cj5FFgqsWgD9mQ78EVqsxgxA%2FOK61gxFOc; Forum_auth=ea7c09jwPY9ib2D34j6ApuXHstWxOwRino%2BPm1GIpD8emVF3x8fAiWGE3g; M1SH_2132_checkpm=1; _td=7abfabef-9bfb-4893-90ee-c416eaefb8b1; M1SH_2132_lastact=1550472643%09misc.php%09patch; _gali=pt",
    'Host': "forum.cyberctm.com",
    'Pragma': "no-cache",
    # 'Referer': "https://forum.cyberctm.com/space-uid-503430.html",
    'Referer': "https://forum.cyberctm.com",
    # 'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
}



class RClient(object):
    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password.encode()).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('captcha.png', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers,
                          timeout=30)
        return r.json()

    def rk_report_error(self, im_id):
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers, timeout=30)
        return r.json()

def replace_cooke(cookieStr,CookieDic):
    for key in CookieDic:
        cookieStr = re.sub(key + '=(.*?);', key + '=' + CookieDic[key] + ';', cookieStr)
        # if re.search(key,cookieStr):
        #     continue
        # else:
        #     cookieStr +=key+'='+CookieDic[key] + ';'

    return cookieStr

def doing(seccode,headers,link,mycomment):
    print(seccode)
    # 请求换一张图片
    update_img_url = 'https://forum.cyberctm.com/misc.php?mod=seccode&action=update&idhash=' + seccode
    if USE_PROXY:
        update_response = requests.get(update_img_url, headers=headers, proxies=proxies, timeout=10)
    else:
        update_response = requests.get(update_img_url, headers=headers,timeout=10)
    update_response_CookieDic = update_response.cookies.get_dict()
    cookieStr = headers['Cookie']
    cookieStr = replace_cooke(cookieStr, update_response_CookieDic)
    headers['Cookie'] = cookieStr

    # 请求并保存图片
    img_url = 'https://forum.cyberctm.com/' + re.search('src="(misc.php.*?)"', update_response.text).group(1)
    # print(img_url)
    if USE_PROXY:
        img_reponse = requests.get(img_url, headers=headers, proxies=proxies, timeout=10)
    else:
        img_reponse = requests.get(img_url, headers=headers, timeout=10)
    img_reponse_CookieDic = img_reponse.cookies.get_dict()
    cookieStr = headers['Cookie']
    cookieStr = replace_cooke(cookieStr, img_reponse_CookieDic)
    headers['Cookie'] = cookieStr

    with open('captcha.png', 'wb') as f:
        f.write(img_reponse.content)

    # 开始打码
    print('正在处理验证码。。')
    with open('captcha.png', 'rb') as f:
        im = f.read()
    captcha_res = rc.rk_create(im, 3040)
    print(captcha_res)
    captcha_res = captcha_res['Result']

    # check 验证码
    headers['X-Requested-With'] = 'XMLHttpRequest'
    check_url_START = 'https://forum.cyberctm.com/misc.php?mod=seccode&action=check&inajax=1&modid=forum::viewthread&idhash={seccode}&secverify={captcha_res}'
    check_url = check_url_START.format(seccode=seccode,captcha_res=captcha_res)
    # print(check_url)
    # print(headers)
    if USE_PROXY:
        check_response = requests.get(check_url, headers=headers, proxies=proxies, timeout=10)
    else:
        check_response = requests.get(check_url, headers=headers, timeout=10)
    # print(check_response.text)
    check_response_CookieDic = check_response.cookies.get_dict()
    cookieStr = headers['Cookie']
    cookieStr = replace_cooke(cookieStr, check_response_CookieDic)
    headers['Cookie'] = cookieStr
    del headers['X-Requested-With']

    # 开始回复
    tid = re.search('https://forum.cyberctm.com/forum.php\?mod=viewthread&tid=(\d+)&extra=', link).group(1)
    reply_url = 'https://forum.cyberctm.com/forum.php?mod=post&action=reply&fid=291&tid={tid}&extra=&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1'.format(tid=tid)
    body = 'message={message}&seccodehash={seccode}&seccodemodid=forum%3A%3Aviewthread&seccodeverify={seccodeverify}&posttime={posttime}&formhash=e633004f&usesig=1&subject=%2B%2B'
    posttime = str(int(time.time()) - 1)
    data = body.format(message=quote(mycomment), seccodeverify=captcha_res, posttime=posttime, seccode=seccode)
    # print(data)

    headers['Content-Type'] = "application/x-www-form-urlencoded"
    headers['Content-Length'] = str(len(data))

    # print(reply_url)
    # print(headers)

    if USE_PROXY:
        response = requests.post(reply_url, headers=headers, data=data, proxies=proxies, timeout=10)
    else:
        response = requests.post(reply_url, headers=headers, data=data,timeout=10)
    # print(response.text)
    if '非常感謝，回覆發佈成功' in response.text:
        print('发布成功！')
    elif '抱歉，您兩次發表間隔少於 10 秒，請稍候再發表' in response.text:
        print('抱歉，您兩次發表間隔少於 10 秒，請稍候再發表')
    elif '抱歉，驗證碼填寫錯誤' in response.text:
        print('抱歉，驗證碼填寫錯誤')
        print('验证码出错，正在重试')
        return False
    else:
        print('发布失败')
    print('两个帖子发布时间需要间隔10秒，正在暂停10秒..')
    time.sleep(10)
    return True

def setComment(link,mycomment):
    headers = copy.deepcopy(start_headers)
    if USE_PROXY:
        detail_response = requests.get(link, headers=headers, proxies=proxies, timeout=10)
    else:
        detail_response = requests.get(link, headers=headers, timeout=10)
    # 处理获取返回的cookie
    deatail_response_CookieDic = detail_response.cookies.get_dict()
    cookieStr = headers['Cookie']
    cookieStr = replace_cooke(cookieStr, deatail_response_CookieDic)
    headers['Cookie'] = cookieStr

    # 匹配获取图片的code
    seccode = re.search('<span id="seccode_(.*?)"></span>', detail_response.text)

    #发帖有验证码
    if seccode:
        seccode = seccode.group(1)
        doingRes = doing(seccode,headers,link,mycomment)
        if doingRes:
            return True
        else:
            return False
    else:
        #发帖无验证码
        # check
        print('第一次发布，无验证码，正在处理')
        headers['X-Requested-With'] = 'XMLHttpRequest'
        check_url = 'https://forum.cyberctm.com/forum.php?mod=ajax&action=checkpostrule&inajax=yes&ac=reply'
        if USE_PROXY:
            check_response = requests.get(check_url, headers=headers, proxies=proxies, timeout=10)
        else:
            check_response = requests.get(check_url, headers=headers, timeout=10)

        check_response_CookieDic = check_response.cookies.get_dict()
        cookieStr = headers['Cookie']
        cookieStr = replace_cooke(cookieStr, check_response_CookieDic)
        headers['Cookie'] = cookieStr
        del headers['X-Requested-With']

        ##################
        seccode = re.search('<span id="seccode_(.*?)"></span>', check_response.text)
        if seccode:
            seccode = seccode.group(1)
            doingRes = doing(seccode, headers, link, mycomment)
            if doingRes:
                return True
            else:
                return False
        else:
            print('第一次发布，没有获取到验证码')
        ##################

        # # 开始回复
        # tid = re.search('https://forum.cyberctm.com/forum.php\?mod=viewthread&tid=(\d+)&extra=', link).group(1)
        # reply_url = 'https://forum.cyberctm.com/forum.php?mod=post&action=reply&fid=291&tid={tid}&extra=&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1'.format(tid=tid)
        # # body = 'message={message}&seccodemodid=forum%3A%3Aviewthread&posttime={posttime}&formhash=3da10717&usesig=1&subject=++'
        # body = 'message={message}&posttime={posttime}&formhash=3da10717&usesig=1&subject=++'
        # posttime = str(int(time.time()) - 1)
        # data = body.format(message=quote(mycomment), posttime=posttime)
        #
        # headers['Content-Type'] = "application/x-www-form-urlencoded"
        # headers['Content-Length'] = str(len(data))
        # response = requests.post(reply_url, headers=headers, data=data, proxies=proxies)
        # print(response.text)
        # if '非常感謝，回覆發佈成功' in response.text:
        #     print('发布成功！')
        # elif '抱歉，您兩次發表間隔少於 10 秒，請稍候再發表' in response.text:
        #     print('抱歉，您兩次發表間隔少於 10 秒，請稍候再發表')
        # elif '抱歉，驗證碼填寫錯誤' in response.text:
        #     print('抱歉，驗證碼填寫錯誤')
        # else:
        #     print('发布失败')
        # print('两个帖子发布时间需要间隔10秒，正在暂停10秒..')
        # time.sleep(10)

def start():

    #获取第一页
    pageToken = 1
    start_url = 'https://forum.cyberctm.com/home.php?mod=space&uid=503430&do=thread&view=me&order=dateline&page='+str(pageToken)
    if USE_PROXY:
        response = requests.get(start_url, headers=start_headers, proxies=proxies)
    else:
        response = requests.get(start_url, headers=start_headers)
    # print(response.text)
    html = HTML(response.text)

    url_list = html.xpath('//ul[@id="waterfall"]/li/div/h2/a/@href')
    title_list = html.xpath('//ul[@id="waterfall"]/li/div/h2/a/text()')

    num = 1
    item_list = []
    for url,title in zip(url_list,title_list):
        #请求详情页
        print(str(num)+'. '+title)
        link = 'https://forum.cyberctm.com/' + url
        # print(link)
        obj = {
            'numkey':str(num),
            'link':link,
            'title':title
        }
        item_list.append(obj)
        num+=1

    #获取第二页
    pageToken = 2
    start_url = 'https://forum.cyberctm.com/home.php?mod=space&uid=503430&do=thread&view=me&order=dateline&page=' + str(pageToken)
    if USE_PROXY:
        response = requests.get(start_url, headers=start_headers, proxies=proxies)
    else:
        response = requests.get(start_url, headers=start_headers)
    # print(response.text)
    html = HTML(response.text)

    url_list = html.xpath('//ul[@id="waterfall"]/li/div/h2/a/@href')
    title_list = html.xpath('//ul[@id="waterfall"]/li/div/h2/a/text()')

    for url, title in zip(url_list, title_list):
        # 请求详情页
        print(str(num) + '. ' + title)
        link = 'https://forum.cyberctm.com/' + url
        # print(link)
        obj = {
            'numkey': str(num),
            'link': link,
            'title': title
        }
        item_list.append(obj)
        num += 1


    #开始评论回复
    num_input_listStr = input('\n请输入要发布评论的帖子的序号：')
    sleepTime = input('\n请输入多少分钟后循环发布：')

    while True:
        num_input_list = num_input_listStr.split('.')
        with open('评论内容.txt') as f:
            mycomment = f.read().strip()

        print('当前评论内容是：'+mycomment)
        for item in item_list:
            for num_input in num_input_list:
                if item['numkey'] == num_input:
                    print('\n正在评论：'+str(item['numkey']))
                    try:
                        setRes = setComment(item['link'],mycomment)
                        if setRes:
                            pass
                        else:
                            setRes = setComment(item['link'], mycomment)
                    except:
                        print('未知错误')

                    break
        sleepTimeMin = 60*int(sleepTime)
        print('\n当前时间：'+str(time.strftime('%Y-%m-%d %H:%M:%S')))
        print('等待下一轮：'+sleepTime+'分钟后重新启动。。。')
        time.sleep(sleepTimeMin)



if __name__ == '__main__':
    rc = RClient('zero9988', 'zero007.', '121381', '56ac8da0371748d799d312b77ff2b16f')
    start()