#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import urllib.request
import os
import db

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


def main():
    # get_weapon()
    get_jineng()

if __name__ == '__main__':
    mysqlClient = db.MysqlClient()
    main()