#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests

from lxml.etree import HTML
import json
import re

headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "no-cache,no-cache",
    'content-length': "81",
    'content-type': "application/x-www-form-urlencoded",
    'cookie': "shshshfpb=123fc8850a4514deb95065e6264237302577525c0f3d7f9d45b0290e33; shshshfpa=49ce5a54-e294-dbf9-fddf-22048fd4cc85-1546068659; pinId=-4VoMXTn6w5Vtomoae4kcQ; pin=knight_HHH; unick=knight_HHH; _tp=k9O3f45yxfbvnPdRj9eRDQ%3D%3D; _pst=knight_HHH; ceshi3.com=000; user-key=3b5eb329-3c81-4b88-823d-f84082fcdd43; ipLoc-djd=19-1607-4773-0.640024593; ipLocation=%u5e7f%u4e1c; cn=5; __jdu=1545638699741749995634; shshshfp=c689212129632131a6fd355c84131a2a; wlfstk_smdl=vcalw9j4cqgyoogtlj83rpj7ibr6on7j; TrackID=1X8fkeQidzW6Z6ij_W7MPFdAgVS8JFOzuqJHu7Lqp_-zoqyFhNt33lPxC3SHU9JbYKfqibkKm_1vjm-QQyRELQL9MW-b5WBf5B9z0S7XVpaQ-kLoERih3hAkQWcZ5hhpf; 3AB9D23F7A4B3C9B=5NGY76XT6SFFOAOQR6PPQ7K33WKQF5UTNLOBKY53MBEVQKMXBJSIBBBUHOZ2GGSVAIA7BOETT3F4WHL7PR3K26KDZI; versionFlag=new; qd_uid=JR5V6NFP-VVXLG1GE3QYWCFI7F7PM; qd_fs=1548046950178; qd_ls=1548046950178; sec_flag=606758746e6900c0788603de5aae4347; _ga=GA1.3.1106338818.1548047573; sec_addr=c0a8017d; qd_ts=1549164828994; qd_sq=2; qd_sid=JR5V6NFP-VVXLG1GE3QYWCFI7F7PM-2; _jrda=2; __jdv=122270672|direct|-|none|-|1549164829842; _gid=GA1.3.2146171013.1549164830; qd_ad=-%7C-%7C-%7C-%7C0; _dc_gtm_UA-56485572-1=1; __jda=238784459.1545638699741749995634.1545638700.1548046950.1549164830.16; __jdb=238784459.3.1545638699741749995634|16.1549164830; __jdc=238784459; _jrdb=1549165058073",
    'origin': "https://z.jd.com",
    'pragma': "no-cache",
    'referer': "https://z.jd.com/bigger/search.html",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'Postman-Token': "7acff7d8-f671-41a8-b63e-58e4d8fee397"
    }

detail_headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "no-cache,no-cache",
    'cookie': "shshshfpb=123fc8850a4514deb95065e6264237302577525c0f3d7f9d45b0290e33; shshshfpa=49ce5a54-e294-dbf9-fddf-22048fd4cc85-1546068659; pinId=-4VoMXTn6w5Vtomoae4kcQ; pin=knight_HHH; unick=knight_HHH; _tp=k9O3f45yxfbvnPdRj9eRDQ%3D%3D; _pst=knight_HHH; ceshi3.com=000; user-key=3b5eb329-3c81-4b88-823d-f84082fcdd43; ipLoc-djd=19-1607-4773-0.640024593; ipLocation=%u5e7f%u4e1c; cn=5; __jdu=1545638699741749995634; shshshfp=c689212129632131a6fd355c84131a2a; wlfstk_smdl=vcalw9j4cqgyoogtlj83rpj7ibr6on7j; TrackID=1X8fkeQidzW6Z6ij_W7MPFdAgVS8JFOzuqJHu7Lqp_-zoqyFhNt33lPxC3SHU9JbYKfqibkKm_1vjm-QQyRELQL9MW-b5WBf5B9z0S7XVpaQ-kLoERih3hAkQWcZ5hhpf; 3AB9D23F7A4B3C9B=5NGY76XT6SFFOAOQR6PPQ7K33WKQF5UTNLOBKY53MBEVQKMXBJSIBBBUHOZ2GGSVAIA7BOETT3F4WHL7PR3K26KDZI; versionFlag=new; qd_uid=JR5V6NFP-VVXLG1GE3QYWCFI7F7PM; qd_fs=1548046950178; sec_flag=606758746e6900c0788603de5aae4347; _ga=GA1.3.1106338818.1548047573; sec_addr=c0a8017d; __jdv=122270672|direct|-|none|-|1549164829842; _gid=GA1.3.2146171013.1549164830; __jdc=238784459; recentbrowse=fca5d0a2415241f39111c2ae01d08f26; qd_ls=1549164828994; qd_ts=1549165074478; qd_sq=3; qd_ad=-%7C-%7C-%7C-%7C0; __jda=238784459.1545638699741749995634.1545638700.1549164830.1549172009.17; _jrda=3",
    'pragma': "no-cache",
    'referer': "https://z.jd.com/bigger/search.html",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'Postman-Token': "020642d0-6087-4646-96c3-91c776eb2640"
    }

count_headers = {
    'Pragma': "no-cache",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'Accept': "*/*",
    'Referer': "https://z.jd.com/project/details/109900.html",
    'Cookie': "shshshfpb=123fc8850a4514deb95065e6264237302577525c0f3d7f9d45b0290e33; shshshfpa=49ce5a54-e294-dbf9-fddf-22048fd4cc85-1546068659; pinId=-4VoMXTn6w5Vtomoae4kcQ; pin=knight_HHH; unick=knight_HHH; _tp=k9O3f45yxfbvnPdRj9eRDQ%3D%3D; _pst=knight_HHH; ceshi3.com=000; user-key=3b5eb329-3c81-4b88-823d-f84082fcdd43; ipLoc-djd=19-1607-4773-0.640024593; ipLocation=%u5e7f%u4e1c; cn=5; __jdu=1545638699741749995634; shshshfp=c689212129632131a6fd355c84131a2a; wlfstk_smdl=vcalw9j4cqgyoogtlj83rpj7ibr6on7j; TrackID=1X8fkeQidzW6Z6ij_W7MPFdAgVS8JFOzuqJHu7Lqp_-zoqyFhNt33lPxC3SHU9JbYKfqibkKm_1vjm-QQyRELQL9MW-b5WBf5B9z0S7XVpaQ-kLoERih3hAkQWcZ5hhpf; 3AB9D23F7A4B3C9B=5NGY76XT6SFFOAOQR6PPQ7K33WKQF5UTNLOBKY53MBEVQKMXBJSIBBBUHOZ2GGSVAIA7BOETT3F4WHL7PR3K26KDZI; versionFlag=new; qd_uid=JR5V6NFP-VVXLG1GE3QYWCFI7F7PM; qd_fs=1548046950178; __jdv=122270672|direct|-|none|-|1549164829842; __jdc=238784459; qd_ts=1549174655760; qd_ls=1549174655760; qd_sq=5; qd_sid=JR5V6NFP-VVXLG1GE3QYWCFI7F7PM-5; qd_ad=-%7C-%7Cdirect%7C-%7C0; _pcd_=d456f8491e591856accf708f5f994c85; ordDeviceType=pc; ordAppCode=6; ordSystemType=pc; __jda=238784459.1545638699741749995634.1545638700.1549177120.1549178990.20; __jdb=238784459.1.1545638699741749995634|20.1549178990; _jrda=6; _jrdb=1549178990621",
    'Connection': "keep-alive",
    'Cache-Control': "no-cache",
    'cache-control': "no-cache",
    'Postman-Token': "4a137c12-5b9f-4300-a454-d8c9de3f39f5"
    }

def start():
    for i in range(194,200):
        print('当前页：'+str(i))
        start_url = 'https://z.jd.com/bigger/search.html'
        body = 'status=&sort=&categoryId=&parentCategoryId=&sceneEnd=&productEnd=&keyword=&page='+str(i)

        response = requests.post(start_url, headers=headers,data=body)
        # print(response.text)
        html = HTML(response.text)
        urls = html.xpath('//div[@class="l-result"]//li/a/@href')

        print(len(urls))

        for url in urls:
            link = 'https://z.jd.com'+url
            print(link)
            try:
                response = requests.get(link,headers=detail_headers)
                id = re.search('https://z.jd.com/project/details/(\d+).html',link).group(1)

                html = HTML(response.text)
                title = html.xpath('string(//h1)').replace(',','，').strip()
                price = html.xpath('string(//p[@class="p-num"]/text())')
                yu_price = html.xpath('string(//p[@id="projectMessage"]/span[2]/text())')

                if 'video' in response.text:
                    has_video = '是'
                else:
                    has_video = '否'

                imgXpath = html.xpath('//div[@class="tab-div tab-current"]//p/img')
                img_len = str(len(imgXpath))

                # like = html.xpath('string(//span[@id="praisCount"])').replace('(','').replace(')','')
                # guanzhu = html.xpath('string(//span[@id="focusCount"])').replace('(','').replace(')','')

                contentlist = html.xpath('//div[@id="proList"]//text()')
                content = ''.join(contentlist)
                content = content.replace(' ','').replace('\t','').replace('\n',' ').replace('\r',' ').replace(',','，').strip()


                count_url = 'https://sq.jr.jd.com/cm/getCount?key=1000&systemId='+id
                count_response = requests.get(count_url,headers=count_headers)
                print(count_response.text)
                json_obj = json.loads(count_response.text.replace('(','').replace(')',''))
                like = str(json_obj['data']['praise'])
                guanzhu = str(json_obj['data']['focus'])


                save_res = id+','+link+','+title+','+price+','+yu_price+','+has_video+','+img_len+','+content+','+like+','+guanzhu+'\n'
                print(save_res)
                with open('结果.csv','a',encoding='gbk',errors='ignore') as f:
                    f.write(save_res)
            except:
                continue



if __name__ == '__main__':
    # with open('结果.csv','w',encoding='gbk') as f:
    #     f.write('id,链接,标题,众筹金额,融资目标金额,有无视频,图片数量,项目情况,点赞数,关注数\n')
    start()