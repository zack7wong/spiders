#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import requests
from lxml.etree import HTML
import json
import time

common_headers = {
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    # 'Cookie': "u=344146sc; visitedfid=19139; pcLocate=%7B%22proCode%22%3A%22440000%22%2C%22pro%22%3A%22%E5%B9%BF%E4%B8%9C%E7%9C%81%22%2C%22cityCode%22%3A%22440300%22%2C%22city%22%3A%22%E6%B7%B1%E5%9C%B3%E5%B8%82%22%2C%22dataType%22%3A%22ipJson%22%2C%22expires%22%3A1549415840240%7D; pcautoLocate=%7B%22proId%22%3A5%2C%22cityId%22%3A4%2C%22url%22%3A%22%2F%2Fm.pcauto.com.cn%2Fx%2Fqcbj%2Fsz%2F%22%2C%22dataTypeAuto%22%3A%22region_ipArea%22%7D; PClocation=4; u4ad=343dhgtfo; __vfe51ad09f7aed1d067bdc0457b9d99ac=d8b1113c2e8fa58eb65922dd82ae824f; __va8195693074b53da7be71124f2488e55=d8b1113c2e8fa58eb65922dd82ae824f; __v502633=d8b1113c2e8fa58eb65922dd82ae824f; __v6582107fa894c80957eddd66ae60c68e=d8b1113c2e8fa58eb65922dd82ae824f; __v501902=d8b1113c2e8fa58eb65922dd82ae824f; __v882a81bf1abecefbc2b577ba0c2d83b0=d8b1113c2e8fa58eb65922dd82ae824f; __v606ef359c0dc2f064ef92f8f313fc0cc=d8b1113c2e8fa58eb65922dd82ae824f; __v83a312512a0fbe9b58eac1706c6962a5=d8b1113c2e8fa58eb65922dd82ae824f; __v502559=d8b1113c2e8fa58eb65922dd82ae824f; pcsuv=1548119848674.a.989280604; __vf864130f0db87de822311d6717a6f126=d8b1113c2e8fa58eb65922dd82ae824f; __v501960=d8b1113c2e8fa58eb65922dd82ae824f; __v50090b044ce9ed3e576389d2e5b3fb20=d8b1113c2e8fa58eb65922dd82ae824f; __v8322304853fa33e7667ac3e09d7c7a6c=d8b1113c2e8fa58eb65922dd82ae824f; __v502168=d8b1113c2e8fa58eb65922dd82ae824f; __v501997=d8b1113c2e8fa58eb65922dd82ae824f; __vc4ffbac63734fd17fe0d17058479c8e4=d8b1113c2e8fa58eb65922dd82ae824f; __v502453=d8b1113c2e8fa58eb65922dd82ae824f; __veab8b16d80b310b890fccf8dea2c09d7=d8b1113c2e8fa58eb65922dd82ae824f; __v502580=d8b1113c2e8fa58eb65922dd82ae824f; __v70ecd6348913f930c52e54f451f979da=d8b1113c2e8fa58eb65922dd82ae824f; __v502620=d8b1113c2e8fa58eb65922dd82ae824f; __v502624=d8b1113c2e8fa58eb65922dd82ae824f; __v502613=d8b1113c2e8fa58eb65922dd82ae824f; __v502621=d8b1113c2e8fa58eb65922dd82ae824f; __v502610=d8b1113c2e8fa58eb65922dd82ae824f; __v502625=d8b1113c2e8fa58eb65922dd82ae824f; __v502616=d8b1113c2e8fa58eb65922dd82ae824f; __v502618=d8b1113c2e8fa58eb65922dd82ae824f; __vbf65b25699efbca214c253fa75f5892c=d8b1113c2e8fa58eb65922dd82ae824f; __v502628=d8b1113c2e8fa58eb65922dd82ae824f; __v502617=d8b1113c2e8fa58eb65922dd82ae824f; __v502611=d8b1113c2e8fa58eb65922dd82ae824f; __v502561=d8b1113c2e8fa58eb65922dd82ae824f; __v502615=d8b1113c2e8fa58eb65922dd82ae824f; __v502622=d8b1113c2e8fa58eb65922dd82ae824f; __v502626=d8b1113c2e8fa58eb65922dd82ae824f; __v502623=d8b1113c2e8fa58eb65922dd82ae824f; __ve50af8f660c9b49c23ae5d3d6b084e8d=d8b1113c2e8fa58eb65922dd82ae824f; __va9c6f8abab3105bd120f4d24162d9530=d8b1113c2e8fa58eb65922dd82ae824f; __v502563=d8b1113c2e8fa58eb65922dd82ae824f; __v502614=d8b1113c2e8fa58eb65922dd82ae824f; __va3e0d37c4338fbd25a973c97e63855a7=d8b1113c2e8fa58eb65922dd82ae824f; __v502612=d8b1113c2e8fa58eb65922dd82ae824f; __v501753=d8b1113c2e8fa58eb65922dd82ae824f; __v502609=d8b1113c2e8fa58eb65922dd82ae824f; __v502619=d8b1113c2e8fa58eb65922dd82ae824f; pcuvdata=lastAccessTime=1548122008360|visits=3; channel=6609",
    'Host': "bbs.pcauto.com.cn",
    'Pragma': "no-cache",
    'Referer': "https://bbs.pcauto.com.cn/forum-19139-2.html",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
}

def start():
    for i in range(1,535):
        print('当前页：'+str(i))
        start_url = 'https://bbs.pcauto.com.cn/forum-19139-{pageToken}.html'.format(pageToken=i)
        print(start_url)
        try:
            response = requests.get(start_url,headers=common_headers,timeout=10)
            # print(response.text)
            html = HTML(response.text)

            tbody_list = html.xpath('//div[@id="topic_list"]//table//tbody')
            # print(len(tbody_list))
            id_list = []
            obj_list = []
            for tbody in tbody_list[1:]:
                title = tbody.xpath('string(./tr//span[@class="checkbox_title"]/a/text())').strip()
                url = 'https:'+tbody.xpath('string(./tr//span[@class="checkbox_title"]/a/@href)').strip()
                id = re.search('https://bbs\.pcauto\.com\.cn/topic-(\d+)\.html',url)
                if id:
                    id = id.group(1)
                else:
                    continue
                userName = tbody.xpath('string(./tr//td[@class="author"]/cite/a/text())').strip()
                publishDateStr = '20'+tbody.xpath('string(./tr//td[@class="author"]/em/text())').strip()
                replyCount = tbody.xpath('string(./tr//td[@class="nums"]/cite/text())').strip()
                jinghuaStr = tbody.xpath('string(./tr//span/a[@class="a-pick1"]/@title)').strip()
                if jinghuaStr =='精华':
                    jinghua = '是'
                else:
                    jinghua = '否'

                obj = {
                    'id':id,
                    'url':url,
                    'userName':userName,
                    'title':title,
                    'jinghua':jinghua,
                    'replyCount':replyCount,
                    'publishDateStr':publishDateStr,
                }
                id_list.append(id)
                obj_list.append(obj)

            clickCount_url = 'https://bbs.pcauto.com.cn/forum/loadStaticInfos.ajax?isBrandForum=true&tids='+','.join(id_list)+'&fid=19139'
            # print(clickCount_url)
            headers = {
                'Accept': "application/json, text/javascript, */*; q=0.01",
                'Accept-Encoding': "gzip, deflate, br",
                'Accept-Language': "zh-CN,zh;q=0.9",
                'Cache-Control': "no-cache",
                'Connection': "keep-alive",
                # 'Cookie': "u=344146sc; visitedfid=19139; pcLocate=%7B%22proCode%22%3A%22440000%22%2C%22pro%22%3A%22%E5%B9%BF%E4%B8%9C%E7%9C%81%22%2C%22cityCode%22%3A%22440300%22%2C%22city%22%3A%22%E6%B7%B1%E5%9C%B3%E5%B8%82%22%2C%22dataType%22%3A%22ipJson%22%2C%22expires%22%3A1549415840240%7D; pcautoLocate=%7B%22proId%22%3A5%2C%22cityId%22%3A4%2C%22url%22%3A%22%2F%2Fm.pcauto.com.cn%2Fx%2Fqcbj%2Fsz%2F%22%2C%22dataTypeAuto%22%3A%22region_ipArea%22%7D; PClocation=4; u4ad=343dhgtfo; __vfe51ad09f7aed1d067bdc0457b9d99ac=d8b1113c2e8fa58eb65922dd82ae824f; __va8195693074b53da7be71124f2488e55=d8b1113c2e8fa58eb65922dd82ae824f; __v502633=d8b1113c2e8fa58eb65922dd82ae824f; __v6582107fa894c80957eddd66ae60c68e=d8b1113c2e8fa58eb65922dd82ae824f; __v501902=d8b1113c2e8fa58eb65922dd82ae824f; __v882a81bf1abecefbc2b577ba0c2d83b0=d8b1113c2e8fa58eb65922dd82ae824f; __v606ef359c0dc2f064ef92f8f313fc0cc=d8b1113c2e8fa58eb65922dd82ae824f; __v83a312512a0fbe9b58eac1706c6962a5=d8b1113c2e8fa58eb65922dd82ae824f; __v502559=d8b1113c2e8fa58eb65922dd82ae824f; pcsuv=1548119848674.a.989280604; __vf864130f0db87de822311d6717a6f126=d8b1113c2e8fa58eb65922dd82ae824f; __v501960=d8b1113c2e8fa58eb65922dd82ae824f; __v50090b044ce9ed3e576389d2e5b3fb20=d8b1113c2e8fa58eb65922dd82ae824f; __v8322304853fa33e7667ac3e09d7c7a6c=d8b1113c2e8fa58eb65922dd82ae824f; __v502168=d8b1113c2e8fa58eb65922dd82ae824f; __v501997=d8b1113c2e8fa58eb65922dd82ae824f; __vc4ffbac63734fd17fe0d17058479c8e4=d8b1113c2e8fa58eb65922dd82ae824f; __v502453=d8b1113c2e8fa58eb65922dd82ae824f; __veab8b16d80b310b890fccf8dea2c09d7=d8b1113c2e8fa58eb65922dd82ae824f; __v502580=d8b1113c2e8fa58eb65922dd82ae824f; __v70ecd6348913f930c52e54f451f979da=d8b1113c2e8fa58eb65922dd82ae824f; __v502620=d8b1113c2e8fa58eb65922dd82ae824f; __v502624=d8b1113c2e8fa58eb65922dd82ae824f; __v502613=d8b1113c2e8fa58eb65922dd82ae824f; __v502621=d8b1113c2e8fa58eb65922dd82ae824f; __v502610=d8b1113c2e8fa58eb65922dd82ae824f; __v502625=d8b1113c2e8fa58eb65922dd82ae824f; __v502616=d8b1113c2e8fa58eb65922dd82ae824f; __v502618=d8b1113c2e8fa58eb65922dd82ae824f; __vbf65b25699efbca214c253fa75f5892c=d8b1113c2e8fa58eb65922dd82ae824f; __v502628=d8b1113c2e8fa58eb65922dd82ae824f; __v502617=d8b1113c2e8fa58eb65922dd82ae824f; __v502611=d8b1113c2e8fa58eb65922dd82ae824f; __v502561=d8b1113c2e8fa58eb65922dd82ae824f; __v502615=d8b1113c2e8fa58eb65922dd82ae824f; __v502622=d8b1113c2e8fa58eb65922dd82ae824f; __v502626=d8b1113c2e8fa58eb65922dd82ae824f; __v502623=d8b1113c2e8fa58eb65922dd82ae824f; __ve50af8f660c9b49c23ae5d3d6b084e8d=d8b1113c2e8fa58eb65922dd82ae824f; __va9c6f8abab3105bd120f4d24162d9530=d8b1113c2e8fa58eb65922dd82ae824f; __v502563=d8b1113c2e8fa58eb65922dd82ae824f; __v502614=d8b1113c2e8fa58eb65922dd82ae824f; __va3e0d37c4338fbd25a973c97e63855a7=d8b1113c2e8fa58eb65922dd82ae824f; __v502612=d8b1113c2e8fa58eb65922dd82ae824f; __v501753=d8b1113c2e8fa58eb65922dd82ae824f; __v502609=d8b1113c2e8fa58eb65922dd82ae824f; __v502619=d8b1113c2e8fa58eb65922dd82ae824f; pcuvdata=lastAccessTime=1548122008360|visits=3; channel=6609",
                'Host': "bbs.pcauto.com.cn",
                'Pragma': "no-cache",
                'Referer': "https://bbs.pcauto.com.cn/forum-19139-2.html",
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                'X-Requested-With': "XMLHttpRequest",
                'cache-control': "no-cache",
                'Postman-Token': "34494394-e4c0-4211-b887-9e229e38ad48"
            }

            clickCount_response = requests.get(clickCount_url,headers=headers)
            # print(clickCount_response.text)
            json_obj = json.loads(clickCount_response.text)

            for item in obj_list:
                for data in json_obj['topicViews']:
                    if item['id'] == str(data['tid']):
                        item['clickCount'] = str(data['view'])
                        break

            for item in obj_list:
                print('\n'+str(item))
                response = requests.get(item['url'],headers=common_headers,timeout=10)
                response.encoding = 'GBK'
                html = HTML(response.text)
                content = html.xpath('string(//div[@class="normal_msg"]//div[@class="post_msg replyBody"]|//div[@class="post-text"])').replace('\n','').replace('\r','').strip()
                print(content)

                comment_list = html.xpath('//div[@class="normal_msg"]//div[@class="post_msg replyBody"]/text()|//div[@class="cmtListItem-wrap"]//div[@class="cmtList-detail-commment"]/text()')
                commentStr_list = []
                for comment in comment_list[1:]:
                    appenRes = comment.replace('\n','').replace('\r','').strip()
                    if appenRes == '':
                        continue
                    commentStr_list.append(appenRes)
                commentStr = '-----'.join(commentStr_list)
                print(commentStr)

                if content == '' and commentStr=='' and '抱歉，你访问的页面暂时无法打开' in response.text:
                    continue
                # 写入
                save_res = item['id'] + '||' + item['url'] + '||' + item['userName'] + '||' + item['title'] + '||' + item['jinghua'] + '||' + item['clickCount'] + '||' + item['replyCount'] + '||' + content + '||' + item['publishDateStr'] + '||'
                save_res = save_res.replace(',', '，').replace('\n', ' ').replace('\r', ' ').replace('||',',').strip() + commentStr + '\n'
                with open('pcauto.csv', 'a', encoding='gbk', errors='ignore') as f:
                    f.write(save_res)
                time.sleep(1)
        except:
            print('出错：'+str(start_url))
            with open('失败.txt','a') as f:
                f.write(start_url+'\n')


if __name__ == '__main__':
    with open('pcauto.csv','w',encoding='gbk') as f:
        f.write('id,url,用户名,标题,是否精华,点击数,回复数,内容,发布时间,评论内容\n')
    start()