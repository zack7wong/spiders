#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json

headers = {
    'accept': "*/*",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "no-cache,no-cache",
    'content-length': "269",
    'content-type': "application/json",
    'cookie': "_ga=GA1.2.1468470422.1544597242; _RSG=ofqh4E8mU94PI135JaMm68; _RDG=282d1e7556706a205711ccbaf3dcebdabe; _RGUID=425ec083-84af-4a72-81b0-5a44c50c1499; GUID=09031124311689892108; _abtest_userid=50e47641-24a2-4c05-9b58-91a8cf0b24e1; StartCity_Pkg=PkgStartCity=30; _gac_UA-3748357-1=1.1549955015.Cj0KCQiA14TjBRD_ARIsAOCmO9acD3tcgRG8VmAWMWoGffgzeod66TxnXAGf5HKnC6EKC3no0_Ib5nIaAohWEALw_wcB; _gcl_aw=GCL.1549955015.~Cj0KCQiA14TjBRD_ARIsAOCmO9acD3tcgRG8VmAWMWoGffgzeod66TxnXAGf5HKnC6EKC3no0_Ib5nIaAohWEALw_wcB; _gcl_dc=GCL.1549955015.Cj0KCQiA14TjBRD_ARIsAOCmO9acD3tcgRG8VmAWMWoGffgzeod66TxnXAGf5HKnC6EKC3no0_Ib5nIaAohWEALw_wcB; HotelCityID=375split%E5%AE%81%E6%B3%A2splitNingbosplit2019-02-20split2019-02-21split0; Session=smartlinkcode=U135371&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Mkt_UnionRecord=%5B%7B%22aid%22%3A%224899%22%2C%22timestamp%22%3A1550755134398%7D%5D; _jzqco=%7C%7C%7C%7C1550755057188%7C1.1932890010.1544597241403.1550755127895.1550755134425.1550755127895.1550755134425.undefined.0.0.82.82; __zpspc=9.16.1550755056.1550755134.5%233%7Cwww.google.com%7C%7C%7C%7C%23; appFloatCnt=18; _HGUID=%3A8%3Bki6%3E93%3E%3Agl3%3Ag%3D83%3E7h63%3Bg%3A%3Ai%3B6i7%3A%3F%3F; _RF1=121.35.102.137; hotelist=O%3DTk0MMjkTxMDkkwMzETxMjQzMTE2ODk4OTIxMDg%3D; fcerror=60.25263669146472; hotelpst=1552018668629; hotelust=1552018658965; _bfa=1.1544597237868.2arur4.1.1550659465135.1552018688355.22.124.228032",
    'cookieorigin': "https://m.ctrip.com",
    'origin': "https://m.ctrip.com",
    'pragma': "no-cache",
    'referer': "https://m.ctrip.com/webapp/hotel/hoteldetail/dianping/994291.html?&fr=detail&atime=20190308&days=1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    'Postman-Token': "489dde21-3d86-4f73-8e2d-9ba1c6c5d832"
    }

url = 'https://m.ctrip.com/restapi/soa2/14605/gethotelcomment?_fxpcqlniredt=09031124311689892108'

for i in range(1,20):
    data = {"hotelId":994291,"pageIndex":i,"tagId":0,"pageSize":10,"groupTypeBitMap":2,"needStatisticInfo":0,"order":0,"basicRoomName":"","travelType":-1,"head":{"cid":"09031124311689892108","ctok":"","cver":"1.0","lang":"01","sid":"8888","syscode":"09","auth":"","extension":[]}}

    response = requests.post(url,headers=headers,data=json.dumps(data))
    json_obj = json.loads(response.text)
    for obj in json_obj['othersCommentList']:
        print(obj['content'])
        with open('结果.txt','a') as f:
            f.write(obj['content'])
