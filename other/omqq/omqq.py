#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
import json
import math
import time
import datetime
from dateutil.relativedelta import relativedelta
from lxml.etree import HTML
import re
import urllib
from PIL import Image
from selenium import webdriver

headers = {
    'accept': "*/*",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "no-cache,no-cache",
    # 'cookie': "vfwebqq=f6c27c04af9d2464c676112181dc7b328be542583714530b5a19756195db58e5b9ac1a7d9a62614c; pgv_info=ssid=s9852505430; pgv_pvid=9277601380; _ga=GA1.2.569029942.1548382908; pt_235db4a7=uid=tMrSur5bIPdltZ1auDKi4Q&nid=1&vid=dMDgAx8yhSt8KcdMbm8IhQ&vn=1&pvn=1&sact=1548382907870&to_flag=0&pl=lKJG0LYLprHQo0Bn3pjvcg*pt*1548382907870; pt_s_235db4a7=vt=1548382907870&cad=; pgv_pvi=9399543808; pgv_si=s1256772608; RK=tbJJjnM52F; ptcz=9cbb7dc45defc734cc2e87ac12e5711a48b6b098323ac3f7b426ff31127d1984; ts_refer=www.google.com/; ts_uid=1685446135; appDownClose=1; userid=14210488; tvfe_boss_uuid=5dbb42da414c8b96; ptisp=cm; _qpsvr_localtk=1550413096610; ptui_loginuin=3353693446; wxky=1; omtoken=b494c28e36; omtoken_expire=1550494195; alertclicked=%7C1%7C; ts_last=om.qq.com/article/videoStatistic",
    # 'cookie': "userid=14210488; omtoken=b494c28e36; ",
    'cookie': "",
    'pragma': "no-cache",
    'referer': "https://om.qq.com/article/videoStatistic",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
}

def login():

    try:
        driver = webdriver.Chrome()
        url = 'https://om.qq.com'
        driver.get(url)
    except:
        print('启动谷歌浏览器失败')
        time.sleep(120)
        exit()

    flag = 0
    while True:
        cookies = driver.get_cookies()

        cookieStr1 = ''
        cookieStr2 = ''
        for cookie in cookies:
            if cookie['name'] == 'userid':
                cookieStr1 = 'userid=' + cookie['value']+';'

                flag += 1

            if cookie['name'] == 'omtoken':
                cookieStr2 = 'omtoken=' + cookie['value'] + ';'
                flag+=1
        if cookieStr1 !='' and cookieStr2 !='':
            endStr = cookieStr1+cookieStr2
        if flag == 2:
            headers['cookie'] = endStr
            print('已登录...')
            break
        print('未检测到登录cookie。。')
        time.sleep(3)

    with open('cookies.txt','w') as f:
        f.write(headers['cookie'])


def get_html_detail(vid,url):
    print('网页url：'+url)
    response = requests.get(url, verify=False)
    response.encoding = 'utf8'
    # print(response.text)
    html = HTML(response.text)
    user_name = html.xpath('string(//span[@class="user_name"])')

    VIDEO_INFO = re.search('var VIDEO_INFO = (.*?)</script>',response.text,re.S)
    if VIDEO_INFO == None:
        return user_name, '', '', '', ''

    VIDEO_INFO_res = VIDEO_INFO.group(1).strip()
    json_obj = json.loads(VIDEO_INFO_res)
    # print(json.dumps(json_obj))
    publishDate = json_obj['video_checkup_time']
    desc = json_obj['desc'] if json_obj['desc'] else ''
    if len(desc)>0:
        tag = desc[-1]
    else:
        tag = ''

    #判断是横屏还是竖屏视频
    pic_url = json_obj['pic_640_360']
    if pic_url == None:
        videoType = ''
    else:
        urllib.request.urlretrieve(pic_url, 'pic.png')
        img = Image.open('pic.png')
        width = img.size[0]
        height = img.size[1]
        if width >= height:
            videoType = '横屏视频'
        else:
            videoType = '竖屏视频'

    return user_name,videoType,publishDate,desc,tag

def get_source(vid):
    url = 'https://napi.om.qq.com/VideoData/SingleVideo?vid='+vid
    response = requests.get(url,headers=headers)
    # print(response.text)
    json_obj = json.loads(response.text)

    totalCount = json_obj['data']['new_total_play_pv']
    resStr = ''

    if totalCount == 0:
        resStr = '天天快报:0.00%;腾讯新闻:0.00%;腾讯视频:0.00%;QQ看点:0.00%;QQ浏览器:0.00%;微信看一看:0.00%;其他:0.00%;'
    else:
        resStr += '天天快报:'+str('%.2f'%(json_obj['data']['total_kuaibao_play_pv']*100/totalCount))+'%;'
        resStr += '腾讯新闻:'+str('%.2f'%(json_obj['data']['total_inews_play_pv']*100/totalCount))+'%;'
        resStr += '腾讯视频:'+str('%.2f'%(json_obj['data']['total_live_play_pv']*100/totalCount))+'%;'
        resStr += 'QQ看点:'+str('%.2f'%(json_obj['data']['total_kandian_play_pv']*100/totalCount))+'%;'
        resStr += 'QQ浏览器:'+str('%.2f'%(json_obj['data']['total_qb_play_pv']*100/totalCount))+'%;'
        resStr += '微信看一看:'+str('%.2f'%(json_obj['data']['total_wx_play_pv']*100/totalCount))+'%;'
        resStr += '其他:'+str('%.2f'%(json_obj['data']['new_total_other_play_pv']*100/totalCount))+'%;'
    print(resStr)
    return resStr


def get_oneWeek_oneMonth(vid,publishDate):
    url = 'https://napi.om.qq.com/VideoData/VideoDailyList?vid={vid}&fields=2%7C7&source=0&startdate={startDate}&enddate={endDate}'

    # oneWeek_startDate = time.strftime('%Y-%m-%d',time.localtime(int(time.time())-60*60*24*7))
    oneWeek_startDate = publishDate
    oneWeek_endDate = time.strftime('%Y-%m-%d',time.localtime(int(time.time())+60*60*24*7))
    oneWeek_url = url.format(vid=vid,startDate=oneWeek_startDate,endDate=oneWeek_endDate)
    # print(oneWeek_url)
    response = requests.get(oneWeek_url, headers=headers)
    json_obj = json.loads(response.text)
    oneWeek_count = 0
    for data in json_obj['data']['list']:
        oneWeek_count+=data['new_daily_play_pv']
    print('一周播放量：'+str(oneWeek_count))

    # oneMonth_startDate = datetime.date.today() - relativedelta(months=+1)
    oneMonth_startDate = publishDate
    # oneMonth_endDate = time.strftime('%Y-%m-%d', time.localtime(int(time.time()) - 60 * 60 * 24))
    oneMonth_endDate = time.strftime('%Y-%m-%d',time.localtime(int(time.time())+60*60*24*30))
    oneMonth_url = url.format(vid=vid,startDate=oneMonth_startDate,endDate=oneMonth_endDate)
    # print(oneMonth_url)
    response = requests.get(oneMonth_url, headers=headers)
    json_obj = json.loads(response.text)
    oneMonth_count = 0
    for data in json_obj['data']['list']:
        oneMonth_count += data['new_daily_play_pv']
    print('一月播放量：'+str(oneMonth_count))
    return str(oneWeek_count),str(oneMonth_count)


def parse_detail(vid):
    print('id:'+vid)
    url = 'https://napi.om.qq.com/VideoData/VideoRealStatis?vid={vid}&fields=2%7C7&source=0'
    start_url = url.format(vid=vid)
    response = requests.get(start_url, headers=headers, verify=False)
    # print(response.text)
    json_obj = json.loads(response.text)

    title = json_obj['data']['title']
    print(title)
    url = json_obj['data']['url']
    total_play = str(json_obj['data']['new_total_play_pv'])
    total_play_finish_rate = str(round(json_obj['data']['total_play_finish_rate']*100,1))
    total_avg_play_time = str(round(json_obj['data']['total_avg_play_time']/60, 2))


    source = get_source(vid)
    user_name, videoType, publishDate, desc, tag = get_html_detail(vid,url)
    oneWeek_count, oneMonth_count = get_oneWeek_oneMonth(vid,publishDate)

    # id,标题,链接,发布人,类型,发布日期,一周播放量,一月播放量,总播放量,播放完成率,播放时长,播放来源,简介,标签
    save_res = vid+'||'+title+'||'+url+'||'+user_name+'||'+videoType+'||'+publishDate+'||'+oneWeek_count+'||'+oneMonth_count+'||'+total_play+'||'+total_play_finish_rate+'||'+total_avg_play_time+'||'+source+'||'+desc+'||'+tag
    save_res = save_res.replace(',','，').replace('\n','').replace('||',',')+'\n'
    print(save_res)
    with open('结果.csv','a',encoding='gbk',errors='ignore') as f:
        f.write(save_res)


def start():
    #获取cookie
    with open('cookies.txt') as f:
        headers['cookie'] = f.read().strip()

    #获取第一页
    start_url = 'https://napi.om.qq.com/VideoData/MediaVideoList?startdate=2019-02-12&enddate=2019-02-18&limit=8&page=1&fields=2%7C3&source=0'
    response = requests.get(start_url, headers=headers, verify=False)
    # print(response.text)
    json_obj = json.loads(response.text)

    #判断登录是否失效
    if 'response' in json_obj and json_obj['response']['code'] == -10403:
        print('登录失效，正在登录。。')
        login()
        start()

    #获取总页数
    total_num = json_obj['data']['total']
    totalPage = math.ceil(total_num/8)
    print('总页数是：'+str(totalPage))

    #处理第一页
    print('当前页：1')
    for item in json_obj['data']['list']:
        vid = item['vid']
        parse_detail(vid)

    #处理剩余页数
    for i in range(2,totalPage+1):
        print('当前页：'+str(i))
        url = 'https://napi.om.qq.com/VideoData/MediaVideoList?startdate=2019-02-12&enddate=2019-02-18&limit=8&page={pageToken}&fields=2%7C3&source=0'
        start_url = url.format(pageToken=i)
        response = requests.get(start_url, headers=headers, verify=False)
        # print(response.text)
        json_obj = json.loads(response.text)
        for item in json_obj['data']['list']:
            vid = item['vid']
            try:
                parse_detail(vid)
            except:
                print('当前id出错：'+str(vid))
                with open('错误.txt','a') as f:
                    f.write(vid+'\n')

    print('程序运行完毕~')
    time.sleep(6000)


if __name__ == '__main__':
    print('程序开始运行')
    with open('结果.csv','w',encoding='gbk') as f:
        #类型：横屏视频，竖屏视频
        f.write('id,标题,链接,发布人,类型,发布日期,一周播放量,一月播放量,总播放量,播放完成率,播放时长,播放来源,简介,标签\n')
    start()