#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import re
import os
import json

headers = {
    'Connection': "keep-alive",
    'Pragma': "no-cache",
    'Cache-Control': "no-cache",
    'Origin': "https://www.glerl.noaa.gov",
    'Upgrade-Insecure-Requests': "1",
    'Content-Type': "application/x-www-form-urlencoded",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Referer': "https://www.glerl.noaa.gov/res/HABs_and_Hypoxia/rtMonSQL.php",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cookie': "_ga=GA1.3.487511337.1551236073; _gid=GA1.3.1188586691.1551236073; _pk_ses.1.a466=*; _gat_GSA_ENOR0=1; _pk_id.1.a466=5d8d6793bd1b4b09.1551236074.2.1551263439.1551260758.",
    'cache-control': "no-cache",
}

def start():
    centerDateList = ['2014-7-01', '2014-8-01', '2014-9-01', '2014-10-01', '2014-11-01', '2014-12-01', '2015-1-01', '2015-2-01', '2015-3-01', '2015-4-01', '2015-5-01', '2015-6-01', '2015-7-01', '2015-8-01', '2015-9-01', '2015-10-01', '2015-11-01', '2015-12-01', '2016-1-01', '2016-2-01', '2016-3-01', '2016-4-01', '2016-5-01', '2016-6-01', '2016-7-01', '2016-8-01', '2016-9-01', '2016-10-01', '2016-11-01', '2016-12-01', '2017-1-01', '2017-2-01', '2017-3-01', '2017-4-01', '2017-5-01', '2017-6-01', '2017-7-01', '2017-8-01', '2017-9-01', '2017-10-01', '2017-11-01', '2017-12-01', '2018-1-01', '2018-2-01', '2018-3-01', '2018-4-01', '2018-5-01', '2018-6-01', '2018-7-01', '2018-8-01', '2018-9-01', '2018-10-01', '2018-11-01']
    centerDateList = ['2017-7-01', '2017-8-01', '2017-9-01', '2017-10-01', '2017-11-01', '2017-12-01', '2018-1-01', '2018-2-01', '2018-3-01', '2018-4-01', '2018-5-01', '2018-6-01', '2018-7-01', '2018-8-01', '2018-9-01', '2018-10-01', '2018-11-01']
    for centerDate in centerDateList:
        url = 'https://www.glerl.noaa.gov/res/HABs_and_Hypoxia/rtMonSQL.php'
        body = 'centerDate={centerDate}&pmDays={pmDays}'
        postdata = body.format(centerDate=centerDate,pmDays=15)
        response = requests.post(url, headers=headers, data=postdata)
        # print(response.text)
        searchRes1 = re.search('var rtData = (.*?);',response.text,re.S).group(1)
        searchRes2 = re.search('var rtQAQCData = (.*?);',response.text,re.S).group(1)
        json_obj1 = json.loads(searchRes1.replace('\'','"'))
        json_obj2 = json.loads(searchRes2.replace('\'','"'))
        print(json.dumps(json_obj1))
        print(json.dumps(json_obj2))

        for key1,key2 in zip(json_obj1,json_obj2):
            itemName = key1
            item1 = json_obj1[key1]
            item2 = json_obj2[key1]
            # print(item1)
            # print(item2)
            for smallkey1,smallkey12 in zip(item1,item2):
                typeName = smallkey1
                data1 = item1[smallkey1]
                data2 = item2[smallkey1]
                fileName = centerDate + '_' + itemName + '_' + typeName + '.txt'
                print(fileName)
                if data1 is not None:
                    for eachList1,eachList2 in zip(data1,data2):
                        saveTime = eachList1[0]
                        saveValue = str(eachList1[1])
                        saveNum = eachList2[1]
                        print(saveTime,saveValue,saveNum)

                        saveRes = saveTime+','+saveValue+','+saveNum+'\n'
                        saveFileName = os.path.join('txtDir',fileName)
                        with open(saveFileName,'a') as f:
                            f.write(saveRes)



if __name__ == '__main__':
    start()

