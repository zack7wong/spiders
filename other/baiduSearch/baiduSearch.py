#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import requests
from lxml import etree
from lxml.etree import HTML
import re

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Cookie': "BD_UPN=123253; MSA_WH=360_640; BAIDUID=3624F2E236BFAA62193EC627B00269EF:FG=1; PSTM=1547282038; BIDUPSID=DCAE3195BFEA154D50EA26B9F9412D65; H_PS_PSSID=1429_28395_21096_28328; BDUSS=jMtNDVralp5OFJFcEFRN3Z-TFluSDN0VHp5TnJxeVhvcVVNR1ZidGhkWnc5M0ZjQVFBQUFBJCQAAAAAAAAAAAEAAAAVrzREZGZpdDQxOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHBqSlxwakpcZ; H_WISE_SIDS=126886_125817_127694_114552_129069_114744_127483_128452_120191_122158_118881_118874_118855_118818_118804_128039_128457_107313_126996_129179_127772_127404_129087_127768_128449_117435_128450_128820_128402_129079_129037_127027_128790_129008_128967_128247_128805_127797_114819_126720_129028_128932_124030_128707_128343_110085_123290_127675_128763_127225_128200_129251_128962; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598",
    'Host': "www.baidu.com",
    'Pragma': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "4cb35454-00c1-4856-9b5c-246b9643e317"
}

def datetime2timestamp(dt):
    if dt is not None:
        try:
            struct_time = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
            return int(time.mktime(struct_time))
        except ValueError:
            return None
    else:
        return None

def deal(div,rank):
    # 处理标题
    nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    title_list = div.xpath('.//h3/a//text()')
    title = ''.join(title_list).replace(',', '，').replace('\n', '').replace('\r', '').replace('\t', '').strip()
    # print(111)
    # print(title)

    # 处理飘红标题
    font_list1 = div.xpath('.//h3/a/font[@color="#CC0000"]/text()')
    font_list2 = div.xpath('.//h3/a/em/text()')
    font_list = font_list1 + font_list2
    # print(font_list)
    font = '/'.join(font_list).replace(',', '，').replace('\n', '').replace('\r', '').replace('\t', '').strip()
    # print(font)

    # 处理描述
    description_list = div.xpath(
        './/div[@class="c-abstract"]//text() | .//div[@class="c-span18 c-span-last"]//div//text() | .//div[@class="c-abstract ec_desc ec_font_small "]//div//text()')
    description = ''.join(description_list).replace(',', '，').replace('\n', '').replace('\r', '').replace('\t','').strip()
    # print(description)

    # 处理飘红描述
    piaohong_xpath_list = [
        './/div[@class="c-abstract"]//font[@color="#CC0000"]/text()',
        './/div[@class="c-abstract"]//em/text()',
        './/div[@class="c-span18 c-span-last"]//div//font[@color="#CC0000"]/text() ',
        './/div[@class="c-span18 c-span-last"]//div//em/text() ',
        './/div[@class="c-abstract ec_desc ec_font_small "]//div//font[@color="#CC0000"]/text()',
        './/div[@class="c-abstract ec_desc ec_font_small "]//div//em/text()',
    ]
    description_font_list = div.xpath('|'.join(piaohong_xpath_list))
    description_font = '/'.join(description_font_list).replace(',', '，').replace('\n', '').replace('\r', '').replace('\t', '').strip()
    # print(description_font)

    url = div.xpath('string(.//span[@class="ec_url"]|.//div[@class="f13"]/a/text()|.//span[@class="c-showurl"])')
    # print(url)

    saveRes = nowTime + ',' + kw + ',' + title + ',' + font+','+description+','+description_font+','+url+','+str(rank)+'\n'
    print(saveRes)

    with open('结果.csv', 'a', encoding='gbk', errors='ignore') as f:
        f.write(saveRes)

def get_objects(keyword, pageToken):
    # kw = keyword + '%20site:news.163.com'
    kw = keyword

    SEARCH_URL = 'https://www.baidu.com/s?wd={kw}&pn={pageToken}&rn=10&oq={kw}'
    url = SEARCH_URL.format(kw=kw, pageToken=pageToken)
    print(url)

    try:
        search_response = requests.get(url,headers=headers,verify=False)
    except:
        return

    # print(search_response.text)
    html = HTML(search_response.text)
    # with open('aa.txt') as f:
    #     aa = f.read()
    # html = HTML(aa)

    div_list = html.xpath('//div[@id="content_left"]/div')

    rank = 1

    for div in div_list:
        if re.search('class="EC_newppim',etree.tostring(div,encoding='utf8').decode('utf8')):
            eachItem_list = div.xpath('./div')
            for eachItem in eachItem_list:
                deal(eachItem,rank)
                rank+=1
        else:
            deal(div,rank)
            rank+=1

    # # 获取真实url
    # for site in site_list:
    #     t = site.xpath('h3/a')[0]
    #     link = t.get("href")
    #
    #     title = site.xpath('h3/a//text()')
    #     title = ''.join(title)
    #
    #     publishDateStr = site.xpath('string(div//span[@class=" newTimeFactor_before_abs m"])').replace('-','').strip()
    #
    #     save_res = title+'||'+link+'||'+publishDateStr
    #     save_res = save_res.replace('\n','').replace('\r','').replace(',','，').replace('||',',') + '\n'
    #     print(save_res)
    #     with open('结果.csv','a',encoding='gbk',errors='ignore') as f:
    #         f.write(save_res)



    page = html.xpath('//div[@id="page"]')
    if page:
        if u"下一页" in etree.tostring(page[0], encoding="utf-8", method="text").decode("utf-8"):
            pageToken = int(pageToken) + 10
        else:
            pageToken = False

    return pageToken


if __name__ == '__main__':

    item_list = []
    with open('keyword.txt') as f:
        results = f.readlines()
        for res in results:
            item_list.append(res.strip())

    with open('结果.csv', 'w',encoding='gbk') as f:
        f.write('时间,关键词,标题,飘红标题,描述,描述飘红,广告主,排名\n')

    for kw in item_list:

        pageToken = '0'
        num = 1
        # while pageToken:
        for i in range(0,11):
            try:
                pageToken = str(i)
                print('当前页：'+str(num))
                pageToken = get_objects(kw,pageToken)
                if pageToken == False:
                    print('已结束')
                    break
                num+=1
                print('暂停3秒')
                time.sleep(3)
            except:
                continue