#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML

area_id_list = ['220','221','224','222','225','227','223','226','228','229']

def start():
    for area_id in area_id_list:
        print('area_id:'+area_id)
        url = 'http://wryfb.fjemc.org.cn/index.aspx?area_id={area_id}&PageNo=1'.format(area_id=area_id)
        response = requests.get(url)
        html = HTML(response.text)
        titles = html.xpath('//div[@class="rightBox"]/div[@class="content bottom10"]//tr/td[2]/a/text()')
        urls = html.xpath('//div[@class="rightBox"]/div[@class="content bottom10"]//tr/td[2]/a/@href')
        totalPage = int(html.xpath('string(//table[@id="Table_right$MyPaper2"]//td[last()-1])'))

        for title,url in zip(titles,urls):
            url = 'http://wryfb.fjemc.org.cn/'+url
            save_res = url.strip()+','+title.strip()+'\n'
            print(save_res)
            with open('fujian_id.txt','a') as f:
                f.write(save_res)

        for i in range(2,totalPage+1):
            print('当前页：'+str(i))
            url = 'http://wryfb.fjemc.org.cn/index.aspx?area_id={area_id}&PageNo={page}'.format(area_id=area_id,page=i)
            response = requests.get(url)
            html = HTML(response.text)
            titles = html.xpath('//div[@class="rightBox"]/div[@class="content bottom10"]//tr/td[2]/a/text()')
            urls = html.xpath('//div[@class="rightBox"]/div[@class="content bottom10"]//tr/td[2]/a/@href')

            for title, url in zip(titles, urls):
                url = 'http://wryfb.fjemc.org.cn/' + url
                save_res = url.strip() + ',' + title.strip() + '\n'
                print(save_res)
                with open('fujian_id.txt', 'a') as f:
                    f.write(save_res)

if __name__ == '__main__':
    start()