#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
from fontTools.ttLib import TTFont
import base64
from io import BytesIO
import re
from lxml import etree


def make_font_file(base64_string: str):
    # 将base64编码的字体字符串解码成二进制编码
    bin_data = base64.decodebytes(base64_string.encode())
    return bin_data


def jiema(ziti, code_str):
    result = []
    code_ziti = []
    # ByteIO把一个二进制内存块当成文件来操作
    font = TTFont(BytesIO(make_font_file(code_str)))
    # 找出基础字形名称的列表，例如：uniE648，uniE183......
    c = font['cmap'].tables[0].ttFont.tables['cmap'].tables[1].cmap
    # for i in range(len(ziti)):
    #     # 找出每一个字对应的16进制编码
    #     print(ziti[i].encode("unicode-escape").decode()[-4:])
    #     code = int(ziti[i].encode("unicode-escape").decode()[-4:], 16)
    #     print(code)
    #     code_ziti.append(code)
    code = int(ziti, 16)
    code_ziti.append(code)
    for code in code_ziti:
        # 根据code键找出c字典中对应的值减一
        x = int(c[code][-2:]) - 1
        result.append(x)
    return result[0]

def parse(response,html):
    code_str = re.search("fangchan-secret';src:url\('data:application/font-ttf;charset=utf-8;base64,(.*?)'\) format\(",response.text, re.S)
    code_str = code_str.group(1)

    # 几室几厅
    roomSize_list = re.findall('<p class="room strongbox">(.*?)</p>', response.text)
    roomSizeEnd_list = []
    for roomSizeUnCode in roomSize_list:
        roomSizeStr = roomSizeUnCode.replace('&nbsp;', '').replace(' ', '')
        fourWord_list = re.findall('&#x(.*?);', roomSizeStr)
        end_Res = roomSizeStr
        for fourWord in fourWord_list:
            jiemaRes = str(jiema(fourWord, code_str))
            end_Res = end_Res.replace('&#x', '').replace(';', '').replace(fourWord, jiemaRes)
        # print(end_Res)
        roomSizeEnd_list.append(end_Res)
    # print(roomSizeEnd_list)
    # print(len(roomSizeEnd_list))

    # 价格
    price_list = re.findall('<div class="money">.*?<b class="strongbox">(.*?)</b>', response.text, re.S)
    priceEnd_list = []
    for priceUnCode in price_list:
        priceStr = priceUnCode.replace('&nbsp;', '').replace(' ', '')
        fourWord_list = re.findall('&#x(.*?);', priceStr)
        end_Res = priceStr
        for fourWord in fourWord_list:
            jiemaRes = str(jiema(fourWord, code_str))
            end_Res = end_Res.replace('&#x', '').replace(';', '').replace(fourWord, jiemaRes)
        # print(end_Res)
        end_Res = end_Res + '元/月'
        priceEnd_list.append(end_Res)
    # print(priceEnd_list)
    # print(len(priceEnd_list))

    # url
    url_list = html.xpath('//ul[@class="listUl"]/li/div[@class="des"]/h2/a[1]/@href')
    urlEnd_list = []
    for myurl in url_list:
        myurl = 'http:' + myurl
        urlEnd_list.append(myurl)
    # print(urlEnd_list)
    # print(len(urlEnd_list))

    # 地址
    addressTree_list = html.xpath('//ul[@class="listUl"]/li//p[@class="add"]')
    addressEnd_list = []
    for addressTree in addressTree_list:
        addressTreeStr = etree.tostring(addressTree)
        address_html = HTML(addressTreeStr)
        address = address_html.xpath('string(//a[2]/text())')
        addressEnd_list.append(address)
    # print(addressEnd_list)
    # print(len(addressEnd_list))

    for url, room, price, address in zip(urlEnd_list, roomSizeEnd_list, priceEnd_list, addressEnd_list):
        save_res = room + '||' + price + '||' + address + '||' + url + '\n'
        save_res = save_res.replace(',', '，').replace('||', ',')
        print(save_res)
        fileName = item.replace('/', '_') + '.csv'
        with open(fileName, 'a') as f:
            f.write(save_res)


def start(item):
    url = 'https://cs.58.com'+item
    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'cache-control': "no-cache,no-cache",
        # 'cookie': "f=n; commontopbar_new_city_info=414%7C%E9%95%BF%E6%B2%99%7Ccs; commontopbar_ipcity=sz%7C%E6%B7%B1%E5%9C%B3%7C0; userid360_xml=3F79B48D6FBF2536C92629D9B34B15CD; time_create=1549852360781; id58=c5/njVw2s+qIVcvtAx2tAg==; wmda_uuid=228387efd8cf697727cbeefaa09d67ee; wmda_new_uuid=1; wmda_visited_projects=%3B2385390625025; 58tj_uuid=3a94291f-dadc-427a-9f54-3169c434ea82; als=0; f=n; xxzl_deviceid=pzC1EHHY0LN6sMa2WeC8YtmMH1u%2Fz41XRoE0amTADixZAcv1s6e8gk8iJf7yQ7f%2B; wmda_session_id_2385390625025=1547293952159-934960d6-8052-b458; new_session=1; new_uv=3; utm_source=; spm=; init_refer=https%253A%252F%252Fdocs.qq.com%252Fscenario%252Flink.html%253Furl%253Dhttps%25253A%25252F%25252Fcs.58.com%25252Fyuelu%25252Fzufang%25252F%2526pid%253D300000000%2524XWiBkTFuGPzR%2526cid%253D59253687; xzfzqtoken=rbivvQf7bxLhe%2BLbmRLQCFvAkv1kKRfmPCucxbkKWJLR0%2F1NFk%2BN95ejao%2B1tZvIin35brBb%2F%2FeSODvMgkQULA%3D%3D",
        'pragma': "no-cache",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
    print(url)
    response = requests.get(url,headers=headers)
    # print(response.text)

    html = HTML(response.text)

    pageNum = int(html.xpath('string(//div[@class="pager"]/a[last()-1])'))

    parse(response,html)

    for i in range(2,pageNum+1):
        print('当前页：'+str(i))
        each_url = url+'pn'+str(i)
        print(each_url)
        response = requests.get(each_url,headers=headers)
        html = HTML(response.text)
        parse(response, html)


if __name__ == '__main__':
    item_list = []
    with open('地区.txt') as f:
        results = f.readlines()
        for res in results:
            item_list.append(res.strip())

    for item in item_list:
        start(item)