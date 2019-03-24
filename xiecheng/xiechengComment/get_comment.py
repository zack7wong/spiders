#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import time

def start():

    url = "https://m.ctrip.com/restapi/soa2/10491/json/GetCommentListAndHotTagList"

    querystring = {"_fxpcqlniredt": "09031124311689892108", "__gw_appid": "99999999", "__gw_ver": "1.0",
                   "__gw_from": "10320607254", "__gw_platform": "H5"}
    for i in range(1,300):
        payload = "{\"CommentResultInfoEntity\":{\"BusinessId\":\"62960\",\"BusinessType\":11,\"PoiId\":0,\"PageIndex\":"+str(i)+",\"PageSize\":10,\"TouristType\":0,\"SortType\":3,\"ImageFilter\":false,\"StarType\":0,\"CommentTagId\":0,\"ChannelType\":7,\"VideoImageWidth\":700,\"VideoImageHeight\":392},\"head\":{\"cid\":\"09031124311689892108\",\"ctok\":\"\",\"cver\":\"1.0\",\"lang\":\"01\",\"sid\":\"8888\",\"syscode\":\"09\",\"auth\":null,\"extension\":[{\"name\":\"protocal\",\"value\":\"https\"}]},\"contentType\":\"json\"}"
        headers = {
            'cookie': "_ga=GA1.2.1468470422.1544597242; _RSG=ofqh4E8mU94PI135JaMm68; _RDG=282d1e7556706a205711ccbaf3dcebdabe; _RGUID=425ec083-84af-4a72-81b0-5a44c50c1499; _abtest_userid=50e47641-24a2-4c05-9b58-91a8cf0b24e1; _gac_UA-3748357-1=1.1549955015.Cj0KCQiA14TjBRD_ARIsAOCmO9acD3tcgRG8VmAWMWoGffgzeod66TxnXAGf5HKnC6EKC3no0_Ib5nIaAohWEALw_wcB; _gcl_aw=GCL.1549955015.~Cj0KCQiA14TjBRD_ARIsAOCmO9acD3tcgRG8VmAWMWoGffgzeod66TxnXAGf5HKnC6EKC3no0_Ib5nIaAohWEALw_wcB; _gcl_dc=GCL.1549955015.Cj0KCQiA14TjBRD_ARIsAOCmO9acD3tcgRG8VmAWMWoGffgzeod66TxnXAGf5HKnC6EKC3no0_Ib5nIaAohWEALw_wcB; _HGUID=%3A8%3Bki6%3E93%3E%3Agl3%3Ag%3D83%3E7h63%3Bg%3A%3Ai%3B6i7%3A%3F%3F; hotelist=O%3DTk0MMjkTxMDkkwMzETxMjQzMTE2ODk4OTIxMDg%3D; fcerror=60.25263669146472; hotelpst=1552018668629; hotelust=1552018658965; __zpspc=9.17.1552982476.1552982476.1%233%7Cwww.google.com%7C%7C%7C%7C%23; MKT_Pagesource=PC; _jzqco=%7C%7C%7C%7C1552982476835%7C1.1932890010.1544597241403.1550755134425.1552982476671.1550755134425.1552982476671.undefined.0.0.83.83; GUID=09031124311689892108; Union=OUID=&AllianceID=66672&SID=1693366&SourceID=&AppID=&OpenID=&Expires=1553692424492; _bfa=1.1544597237868.2arur4.1.1552018688355.1553415246721.25.129.10320607254; Mkt_UnionRecord=%5B%7B%22aid%22%3A%2266672%22%2C%22timestamp%22%3A1553415246750%7D%5D; _gid=GA1.2.394221507.1553415247; _RF1=121.35.103.103",
            'origin': "https://m.ctrip.com",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.9",
            'authority': "m.ctrip.com",
            'x-requested-with': "XMLHttpRequest",
            'pragma': "no-cache",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            'content-type': "application/json",
            'accept': "application/json",
            'cache-control': "no-cache,no-cache",
            'x-ctrip-pageid': "10320607254",
            'referer': "https://m.ctrip.com/webapp/you/comment/district/62960-11.html?openapp=5&s_guid=8F6C9D3A-3501-46B4-8025-F407115358F0",
            'Postman-Token': "3c7ec4a2-1a6b-4b83-a2e6-cc89b964a40d"
        }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

        print(response.text)
        json_obj = json.loads(response.text)
        for data in json_obj['CommentResult']['CommentInfo']:
            Content = data['Content']
            print(Content)
            with open('comment.txt','a') as f:
                f.write(Content+'\n')

        time.sleep(2)



if __name__ == '__main__':
    start()