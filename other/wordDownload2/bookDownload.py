#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import os
import download
import redis
import json

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Cookie': "9090_2132_saltkey=u1d9pIe9; 9090_2132_lastvisit=1547367467; 9090_2132_pc_size_c=0; UM_distinctid=1684680b76e1f0-0cb0c6befd2c36-10376654-1fa400-1684680b77049; 9090_2132_atarget=1; 9090_2132_visitedfid=75; 9090_2132_st_p=0%7C1547373406%7Ce8ea5f3294b045519d7e072eb2c0ac17; 9090_2132_viewid=tid_10391; 9090_2132_sendmail=1; CNZZDATA1273035633=560660413-1547370433-%7C1547379344; 9090_2132_sid=jsmsBP; 9090_2132_ulastactivity=87acUG6QTTLwbMV8ILN7hZWFE8MKcsOoXew603uymJYkSDWL2vi%2B; 9090_2132_auth=99c2KOxym7hLmnorZIBxp0WCVFpmxBIuum7hrUt%2BEbILaouzdHbOrqqqqsP0DFaHrpiIk4ZGKGL3euxjmEfp5ncN; 9090_2132_lastcheckfeed=8929%7C1547380549; 9090_2132_checkfollow=1; 9090_2132_lip=119.78.130.216%2C1547380486; 9090_2132_security_cookiereport=dc640Qhp%2FctoSqbb6MRuhEWILWIOLO74sNRvJQM9onM4hWEY3JxG; 9090_2132_lastact=1547380552%09forum.php%09forumdisplay; 9090_2132_st_t=8929%7C1547380552%7C185616acb96445ea3c6b8d206ab820a7; 9090_2132_forum_lastvisit=D_75_1547380552",
    'Host': "www.gezhongshu.com",
    'Pragma': "no-cache",
    # 'Proxy-Authorization': "Basic SklBTllJSFRUMTpLSUZLT1lZODRK",
    # 'Proxy-Connection': "keep-alive",
    'Referer': "http://www.gezhongshu.com/forum.php?mod=forumdisplay&fid=75&page=42",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
}

def start():
    down = download.Download()

    item_list = []
    bookObjStr = myredisCli.lpop('bookObj_task')
    bookObj = json.loads(bookObjStr.decode())
    item_list.append(bookObj)

    # with open('results.csv') as f:
    #     results = f.readlines()
    #     for res in results:
    #         name = res.split(',')[0].replace('《','').replace('》','')
    #         fileType = res.split(',')[-2].strip()
    #         link = res.split(',')[-1].strip()
    #         if link == '' or name == '' or fileType == '':
    #             continue
    #         obj = {
    #             'name': name,
    #             'fileType': fileType,
    #             'link': link,
    #         }
    #         item_list.append(obj)

    for item in item_list:
        try:
            saveFileName = item['name'] + '.' + item['bookType']
            savePath = os.path.join('books', saveFileName)
            print(saveFileName)
            print(item['link'])

            response = down.get_html(item['link'],headers=headers)
            with open(savePath, 'wb') as file:
                file.write(response.content)
        except:
            print('出错。。'+str(item))
            with open('下载出错.txt','a') as f:
                f.write(str(item)+'\n')

if __name__ == '__main__':
    # 540529113@qq.co  xinfei123
    # 540529113@qq.co  xingqing111
    myredisCli = redis.Redis()
    start()