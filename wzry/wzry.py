#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import urllib.request
import os
from lxml.etree import HTML
import db
import re
import time
from selenium import webdriver
from lxml.etree import HTML

def get_weapon():
    url = 'https://pvp.qq.com/web201605/js/item.json'
    response = requests.get(url)
    # print(response.text)
    json_obj = json.loads(response.text)
    for data in json_obj:
        print(data)
        arms_id = str(data['item_id'])
        arms_name = str(data['item_name'])
        arms_type = str(data['item_type'])
        arms_price = str(data['price'])
        arms_total_price = str(data['total_price'])
        arms_des = str(data['des1'].replace('<p>','').replace('</p>','').replace('<br>',','))

        img_url = 'http://game.gtimg.cn/images/yxzj/img201606/itemimg/{arms_id}.jpg'
        img_start_url = img_url.format(arms_id=arms_id)
        filepath = os.path.join('armsImg',arms_id+'.jpg')
        urllib.request.urlretrieve(img_start_url,filepath)
        arms_img_path = filepath
        print(arms_img_path)
        sql = "insert into arms(arms_id,arms_name,arms_type,arms_price,arms_total_price,arms_des,arms_img_path) values ('%s','%s','%s','%s','%s','%s','%s')"\
              %(arms_id,arms_name,arms_type,arms_price,arms_total_price,arms_des,arms_img_path)
        print(sql)

        mysqlClient.save(sql)
        # break

def get_jineng():
    url = 'https://pvp.qq.com/web201605/js/summoner.json'
    response = requests.get(url)
    # print(response.text)
    json_obj = json.loads(response.text)
    for data in json_obj:
        print(data)
        jineng_id = str(data['summoner_id'])
        jineng_name = str(data['summoner_name'])
        jineng_rank = str(data['summoner_rank'])
        jineng_des = str(data['summoner_description'].replace('<p>','').replace('</p>','').replace('<br>',','))

        img_url = 'http://game.gtimg.cn/images/yxzj/img201606/summoner/{jineng_id}.jpg'
        img_start_url = img_url.format(jineng_id=jineng_id)
        filepath = os.path.join('jinengImg',jineng_id+'.jpg')
        urllib.request.urlretrieve(img_start_url,filepath)
        jineng_img_path = filepath
        print(jineng_img_path)
        sql = "insert into jineng(jineng_id,jineng_name,jineng_rank,jineng_des,jineng_img_path) values ('%s','%s','%s','%s','%s')"\
              %(jineng_id,jineng_name,jineng_rank,jineng_des,jineng_img_path)
        print(sql)

        mysqlClient.save(sql)

def get_video(results):
    #视频
    video_url1 = 'https://gicp.qq.com/wmp/data/js/v3/WMP_PVP_WEBSITE_NEWBEE_DATA_V1.js?callback=newbee_hero_list_callback&_=1546331084970'
    video_url2 = 'https://gicp.qq.com/wmp/data/js/v3/WMP_PVP_WEBSITE_DATA_18_VIDEO_V3.js?callback=web_hero_list_v3&_=1546331084971'

    response1 = requests.get(video_url1)
    resStr = response1.text.replace('newbee_hero_list_callback(','').replace('"})','"}')
    json_obj1 = json.loads(resStr)
    for item in json_obj1['video'].keys():
        if json_obj1['video'][item] == None:
            continue
        for data in json_obj1['video'][item]:
            for res in results:
                if res[2] == item:
                    hero_id = res[1]
                    iVideoId = str(data['iVideoId'])
                    url = 'https://pvp.qq.com/v/detail.shtml?G_Biz=18&tid=' + str(data['iVideoId'])
                    title = str(data['sTitle'])
                    publishDateStr = str(data['sIdxTime'])
                    viewCount = str(data['iTotalPlay'])

                    sql = "insert into heroVideo(hero_id,iVideoId,url,title,publishDateStr,viewCount) values ('%s','%s','%s','%s','%s','%s')" \
                          % (hero_id,iVideoId,url,title,publishDateStr,viewCount)
                    print(sql)

                    mysqlClient.save(sql)

def get_video_url(results):
    driver = webdriver.Chrome()
    for res in results:
        videoID = res[2]
        url = res[3]
        driver.get(url)
        time.sleep(5)
        html = HTML(driver.page_source)
        videoUrl = html.xpath('string(//div[@class="tvp_video"]/video/@src)')
        print(videoUrl)
        sql = "update heroVideo set videoUrl='%s' where iVideoId='%s'"%(videoUrl,videoID)
        mysqlClient.save(sql)


def get_hero_detail(hero_id,hero_url):
    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'cache-control': "no-cache,no-cache",
        # 'cookie': "pt2gguin=o0775340093; ptisp=ctc; RK=XOJxMywUOC; ptcz=92a5d48deb2e6dc47038db022be5da2fe86849760ec80c51c6dfe7ea71b0cb50; vfwebqq=c22a60248aa23dd3fdc043283404bfe4fd6343fd5060a63d0caa86013c78dba5d47ace2bd4fca30a; pgv_pvi=5397110784; pgv_si=s5569012736; pgv_info=ssid=s9843456360; pgv_pvid=1036094262; PTTuserFirstTime=1546214400000; PTTosFirstTime=1546214400000; ts_uid=5216747840; PTTosav=osav; PTTperWeekNum=1; ieg_ingame_userid=nhR1c8c4C3t3UQ1jS8EAuxyhoRlXEhWt; eas_sid=a10524K6M2m6B056r6E0c1Z5o0; LW_sid=Z1T5e406X276M0S6V7E5E7C729; LW_uid=V145L4t6L206h026R7q5X768M1; PTTrouteLine=herolist_strategy_item_summoner_item_summoner_summoner; isHostDate=17897; isOsDate=17897; ts_last=pvp.qq.com/web201605/herodetail/105.shtml",
        'pragma': "no-cache",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        'Postman-Token': "1e6be6f8-78a6-4871-9607-77f11ff81d09"
    }
    response = requests.get(hero_url,headers=headers)
    response.encoding = 'gbk'
    # print(response.text)

    html = HTML(response.text)
    all_shuxing = html.xpath('//ul[@class="cover-list"]/li/span/i/@style')
    #4个属性
    shengcun = all_shuxing[0].replace('width:','').replace('%','')
    gongji = all_shuxing[1].replace('width:','').replace('%','')
    jineng = all_shuxing[2].replace('width:','').replace('%','')
    shangshou = all_shuxing[3].replace('width:','').replace('%','')

    #两个故事
    yingxiong_story = html.xpath('//div[@id="hero-story"]/div[2]/p/text()')
    yingxiong_story = ''.join(yingxiong_story)
    lishi_story = html.xpath('//div[@id="history"]/div[2]/p/text()')
    lishi_story = ''.join(lishi_story)

    #加点建议
    jiadian1 = html.xpath('string(//div[@class="sugg-info2 info"]/p[@class="icon sugg-skill"][1]/img/@src)')
    jiadian1 = re.search('//game.gtimg.cn/.*?/(\d+).png',jiadian1).group(1)
    jiadian2 = html.xpath('string(//div[@class="sugg-info2 info"]/p[@class="icon sugg-skill"][2]/img/@src)')
    jiadian2 = re.search('//game.gtimg.cn/.*?/(\d+).png',jiadian2).group(1)
    jiadian3 = html.xpath('string(//div[@class="sugg-info2 info"]/p[@id="skill3"]/@data-skill)')

    # print(shengcun)
    # print(gongji)
    # print(jineng)
    # print(shangshou)
    # print(yingxiong_story)
    # print(lishi_story)
    # print(jiadian1)
    # print(jiadian2)
    # print(jiadian3)
    update_sql = "update hero set shengcun='%s',gongji='%s',jineng='%s',shangshou='%s',yingxiong_story='%s',lishi_story='%s',jiadian1='%s',jiadian2='%s',jiadian3='%s' where hero_id = '%s'"\
                 %(shengcun,gongji,jineng,shangshou,yingxiong_story,lishi_story,jiadian1,jiadian2,jiadian3,hero_id)
    print(update_sql)
    mysqlClient.save(update_sql)

    #技能
    jineng_ids = html.xpath('//ul[@class="skill-u1"]/li/img/@src')[:4]
    jineng_names = html.xpath('//div[@class="skill-show"]/div/p[@class="skill-name"]/b/text()')
    jineng_lengques = html.xpath('//div[@class="skill-show"]/div/p[@class="skill-name"]/span[1]/text()')[:4]
    jineng_xiaohaos = html.xpath('//div[@class="skill-show"]/div/p[@class="skill-name"]/span[2]/text()')[:4]
    jineng_descs = html.xpath('//div[@class="skill-show"]/div/p[@class="skill-desc"]/text()')
    jineng_tipss = html.xpath('//div[@class="skill-show"]/div/div[@class="skill-tips"]/text()')

    # print(jineng_ids)
    # print(jineng_names)
    # print(jineng_lengques)
    # print(jineng_xiaohaos)
    # print(jineng_descs)
    # print(jineng_tipss)
    for jineng_id,jineng_name,jineng_lengque,jineng_xiaohao,jineng_desc,jineng_tips in zip(jineng_ids,jineng_names,jineng_lengques,jineng_xiaohaos,jineng_descs,jineng_tipss):
        jineng_img_url = 'http:'+jineng_id
        jineng_id = re.search('//game.gtimg.cn/.*?/(\d+).png',jineng_id).group(1)
        jineng_img_path = 'heroJinengImg/'+jineng_id+'.png'
        filepath = os.path.join('heroJinengImg', jineng_id + '.png')
        urllib.request.urlretrieve(jineng_img_url, filepath)

        sql = "insert into heroJineng(hero_id,jineng_id,jineng_name,jineng_lengque,jineng_xiaohao,jineng_desc,jineng_tips,jineng_img_path) values ('%s','%s','%s','%s','%s','%s','%s','%s')"\
              %(hero_id,jineng_id,jineng_name,jineng_lengque,jineng_xiaohao,jineng_desc,jineng_tips,jineng_img_path)
        print(sql)
        mysqlClient.save(sql)

    #关系
    guanxi_list = html.xpath('//div[@class="hero-list-desc"]/p/text()')
    zuijia1 = guanxi_list[0]
    zuijia2 = guanxi_list[1]
    yazhi1 = guanxi_list[2]
    yazhi2 = guanxi_list[3]
    beiyazhi1 = guanxi_list[4]
    beiyazhi2 = guanxi_list[5]
    # print(zuijia1)
    # print(zuijia2)
    # print(yazhi1)
    # print(yazhi2)
    # print(beiyazhi1)
    # print(beiyazhi2)
    sql = "insert into heroGuanxi(hero_id,zuijia1,zuijia2,yazhi1,yazhi2,beiyazhi1,beiyazhi2) values ('%s','%s','%s','%s','%s','%s','%s')" \
          % (hero_id,zuijia1,zuijia2,yazhi1,yazhi2,beiyazhi1,beiyazhi2)
    print(sql)
    mysqlClient.save(sql)

def get_hero():
    url = 'https://pvp.qq.com/web201605/js/herolist.json'
    response = requests.get(url)
    # print(response.text)
    json_obj = json.loads(response.text)
    for data in json_obj:
        print(data)
        hero_id = str(data['ename'])
        hero_name = str(data['cname'])
        hero_type = str(data['hero_type'])
        hero_skin_name = str(data['skin_name'])
        hero_title = str(data['title'])


        hero_url = 'https://pvp.qq.com/web201605/herodetail/{hero_id}.shtml'.format(hero_id=hero_id)

        img_url = 'http://game.gtimg.cn/images/yxzj/img201606/heroimg/{hero_id}/{hero_id}.jpg'
        img_start_url = img_url.format(hero_id=hero_id)
        filepath = os.path.join('heroImg', hero_id + '.jpg')
        urllib.request.urlretrieve(img_start_url, filepath)
        hero_img_path = filepath
        print(hero_img_path)
        sql = "insert into hero(hero_id,hero_name,hero_type,hero_skin_name,hero_title,hero_url,hero_img_path) values ('%s','%s','%s','%s','%s','%s','%s')" \
              % (hero_id,hero_name,hero_type,hero_skin_name,hero_title,hero_url,hero_img_path)
        print(sql)

        mysqlClient.save(sql)


def main():
    # get_weapon()
    # get_jineng()
    # get_hero()

    # sql = 'select * from hero'
    # results = mysqlClient.find_all(sql)
    # for res in results:
    #     print(res)
    #     get_hero_detail(res[1],res[7])

    # sql = 'select * from hero'
    # results = mysqlClient.find_all(sql)
    # get_video(results)

    sql = 'select * from heroVideo'
    results = mysqlClient.find_all(sql)
    get_video_url(results)

if __name__ == '__main__':
    mysqlClient = db.MysqlClient()
    main()