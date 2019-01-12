#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Cookie': "UM_distinctid=1683b5364a6549-048011d22fbc9f-10376654-1fa400-1683b5364a7519; Hm_lvt_d7b9f30d0142471285ea3cfcf5245fed=1547183548; membertype=0; CNZZDATA5937116=cnzz_eid%3D1053519608-1547181214-%26ntime%3D1547258616; Hm_lpvt_d7b9f30d0142471285ea3cfcf5245fed=1547258617; PHPSESSID=84b3mg8g3vo8j5nb84qne1s7h6; logined=1; logincode=84b3mg8g3vo8j5nb84qne1s7h6",
    'Host': "www.zhongtou8.cn",
    'Pragma': "no-cache",
    'Referer': "https://www.zhongtou8.cn/financing/investor/id/204209",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
}
with open('结果.csv','w') as f:
    f.write('标题,链接,约谈数,关注数,已获意向投资,剩余时间,预融资总额,百分比,阶段,地区,行业,起投金额,融资金额,出让股份,上线日期,领头方,投资金额,占股比例,项目问答数,跟投数,跟投详情' + '\n')

myurl = 'https://www.zhongtou8.cn/financing/index/page/{pageToken}/prov/0/indid/0/v/0/status/0'

for i in range(1,7):
    start_url = myurl.format(pageToken=i)
    print(start_url)
    response = requests.get(start_url)
    response.encoding = 'utf8'
    # print(response.text)
    html = HTML(response.text)
    urls = html.xpath('//div[@class="c1180"]/div[@class="mb30 bline boxsha brad fina-card mr20 fl"]/div/a/@href')
    titles = html.xpath('//div[@class="c1180"]/div[@class="mb30 bline boxsha brad fina-card mr20 fl"]/div/a/@title')

    for url,title in zip(urls,titles):
        link = 'https://www.zhongtou8.cn'+url
        # print(link)
        print(title)
        # detail_response = requests.get(link)
        # detail_response.encoding = 'utf8'
        # print(detail_response.text)

        mylink = link.replace('/detail/','/investor/')
        print(mylink)
        genTou_response = requests.get(mylink,headers=headers)
        genTou_response.encoding = 'utf8'
        # print(genTou_response.text)

        genTou_html = HTML(genTou_response.text)

        yuetan = genTou_html.xpath('string(//div[@class="fr mt10"]/a[@class="fbtn submit-intention"]/font[@class="red"])').replace('（','').replace('）','')
        guanzhu = genTou_html.xpath('string(//div[@class="fr mt10"]/a[@class="fbtn addguanzhu"]/font[@class="red"])').replace('（','').replace('）','')

        yixiangtouzi = genTou_html.xpath('string(//div[@class="fl mt15 ml25"]//li[1]//span)')
        shijian = genTou_html.xpath('string(//div[@class="fl mt15 ml25"]//li[2]//b[2])')
        rongzizonge = genTou_html.xpath('string(//div[@class="fl mt15 ml25"]//li[3]//span)')
        baifenbi = genTou_html.xpath('string(//div[@class="add-bar end"]/em)')

        jieduan = genTou_html.xpath('string(//div[@class="fr f-text"]/dl[2]/dd[1]/text())')
        diqu = genTou_html.xpath('string(//div[@class="fr f-text"]/dl[2]/dt[1]/text())')
        hangye = genTou_html.xpath('string(//div[@class="fr f-text"]/dl[2]/dd[2]/text())')
        qitoujine = genTou_html.xpath('string(//div[@class="fr f-text"]/dl[2]/dt[2]/text())')
        rongzijine = genTou_html.xpath('string(//div[@class="fr f-text"]/dl[2]/dd[3]/span/text())')
        churanggufen = genTou_html.xpath('string(//div[@class="fr f-text"]/dl[2]/dt[3]/span/text())')
        shangxianTime = genTou_html.xpath('string(//div[@class="fr f-text"]/dl[2]/dd[4]/span/text())').strip()

        lingtouFang = genTou_html.xpath('string(//div[@class="fr  w182"]/div[1]/text())')
        touzijine = genTou_html.xpath('string(//div[@class="fr  w182"]/div[2]/font/text())')
        zhanbigufen = genTou_html.xpath('string(//div[@class="fr  w182"]/div[3]/font/text())')

        xiangmuwenda = genTou_html.xpath('string(//div[@class="a2-nav"][2]/a/span)')
        gentourenNum = genTou_html.xpath('string(//div[@class="a2-nav"][3]/a/span)')

        gentouTime_list = genTou_html.xpath('//div[@class="gtf"]//li/p[2]/text()')
        gentouPrice_list = genTou_html.xpath('//div[@class="gtf"]//li/p[3]/font/text()')

        allStr = ''
        for gentouTime, gentouPrice in zip(gentouTime_list,gentouPrice_list):
            allStr +=gentouTime+'，'+gentouPrice+'||'

        save_res = title+'||'+mylink+'||'+yuetan+'||'+guanzhu+'||'+yixiangtouzi+'||'+shijian+'||'+rongzizonge+'||'+baifenbi+'||'+jieduan+'||'+diqu+'||'+hangye+'||'+qitoujine+'||'+rongzijine+'||'+churanggufen+'||'+shangxianTime+'||'+lingtouFang+'||'+touzijine+'||'+zhanbigufen+'||'+xiangmuwenda+'||'+gentourenNum+'||'+allStr+'\n'
        print(save_res)
        save_res = save_res.replace(',','，').replace('||',',')
        with open('结果.csv','a') as f:
            f.write(save_res)


