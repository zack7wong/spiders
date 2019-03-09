#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML

headers = {
    'Accept': "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    # 'Content-Length': "87",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Cookie': "JSESSIONID=826D2A7E0181ECF27408998076F23D16; __jsluid=bfeecb1efc40c0fe752d047b5a50c150; _va_ses=*; _va_id=bd80155dc5a6e1d3.1552123717.1.1552123896.1552123717.",
    'Host': "ghgtw.beijing.gov.cn",
    'Origin': "http://ghgtw.beijing.gov.cn",
    'Pragma': "no-cache",
    'Referer': "http://ghgtw.beijing.gov.cn/sjzy/front/project/landdeal/list.do",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest",
    'cache-control': "no-cache",
    'Postman-Token': "8cc73ab9-e937-45ed-a817-e45a64057467"
    }

def start():
    for i in range(14):
        startrecord = i*100+1
        endrecord = startrecord+99
        url = 'http://ghgtw.beijing.gov.cn/sjzy/front/project/landdeal/dataproxy.do?startrecord={startrecord}&endrecord={endrecord}&perpage=20'.format(startrecord=startrecord,endrecord=endrecord)
        print(url)
        data = 'typeid=1%2C2%2C3%2C10&purposeid=0&groupid=&str=&districtid=&blockid=&isend=&isIntranet='
        response = requests.post(url,headers=headers,data=data)
        print(response.text)
        html = HTML(response.text)
        tr_list = html.xpath('//tr')
        for tr in tr_list:
            bianhao = tr.xpath('string(./td[1]/text())')
            name = tr.xpath('string(./td[2]/a/text())')
            mianji = tr.xpath('string(./td[3]/text())')
            fangshi = tr.xpath('string(./td[4]/text())')
            yongtu = tr.xpath('string(./td[5]/text())')

            link = tr.xpath('string(./td[2]/a/@href)')
            start_link = 'http://ghgtw.beijing.gov.cn/sjzy/front/project/landdeal'+link[1:]
            print(start_link)

            new_response = requests.get(start_link,headers=headers)
            new_html = HTML(new_response.text)
            times = new_html.xpath('string(//span[@id="tradetime"])').strip()
            price = new_html.xpath('string(//span[@id="tradeprice"])').replace('\n','').replace('\r','').replace('\t','').replace(' ','').strip()


            save_res = start_link+'||'+bianhao+'||'+name+'||'+mianji+'||'+fangshi+'||'+yongtu+'||'+times+'||'+price
            print(save_res)
            save_res = save_res.replace(',','，').replace('\n','').replace('\r','').replace('||',',').strip()+'\n'
            with open('结果.csv','a',encoding='gbk',errors='ignore') as f:
                f.write(save_res)



if __name__ == '__main__':
    start()