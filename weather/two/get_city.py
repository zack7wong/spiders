#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     get_city
   Description :
   Author :        hayden_huang
   Date：          2018/12/19 15:38
-------------------------------------------------
"""
import requests
import json

headers = {
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Length': "71",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    # 'Cookie': "PHPSESSID=t5i9fvrkj5h6jspjsma0230gl0; pgv_pvi=2796649472; pgv_si=s8206772224; Hm_lvt_d9508cf73ee2d3c3a3f628fe26bd31ab=1545033840; login_id_chat=0; degrDiCookie2=1; userLoginKey=8753b00096a88b57f63f6d0c3f4a75a2; trueName=%E9%BB%84%E5%AA%9B; userName=CC95032D68D56568231F2E619CA12094; login_name_chat=0; Hm_lpvt_d9508cf73ee2d3c3a3f628fe26bd31ab=1545203415",
    'Host': "data.cma.cn",
    'Origin': "http://data.cma.cn",
    'Pragma': "no-cache",
    'Referer': "http://data.cma.cn/dataService/cdcindex/datacode/A.0012.0001/show_value/normal.html",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest",
    'cache-control': "no-cache",
}

city_list = [{'provinceID': '110', 'city': '北京市'}, {'provinceID': '120', 'city': '天津市'}, {'provinceID': '130', 'city': '河北省'}, {'provinceID': '140', 'city': '山西省'}, {'provinceID': '150', 'city': '内蒙古自治区'}, {'provinceID': '210', 'city': '辽宁省'}, {'provinceID': '220', 'city': '吉林省'}, {'provinceID': '230', 'city': '黑龙江省'}, {'provinceID': '310', 'city': '上海市'}, {'provinceID': '320', 'city': '江苏省'}, {'provinceID': '330', 'city': '浙江省'}, {'provinceID': '340', 'city': '安徽省'}, {'provinceID': '350', 'city': '福建省'}, {'provinceID': '360', 'city': '江西省'}, {'provinceID': '370', 'city': '山东省'}, {'provinceID': '410', 'city': '河南省'}, {'provinceID': '420', 'city': '湖北省'}, {'provinceID': '430', 'city': '湖南省'}, {'provinceID': '440', 'city': '广东省'}, {'provinceID': '450', 'city': '广西壮族自治区'}, {'provinceID': '460', 'city': '海南省'}, {'provinceID': '500', 'city': '重庆市'}, {'provinceID': '510', 'city': '四川省'}, {'provinceID': '520', 'city': '贵州省'}, {'provinceID': '530', 'city': '云南省'}, {'provinceID': '540', 'city': '西藏自治区'}, {'provinceID': '610', 'city': '陕西省'}, {'provinceID': '620', 'city': '甘肃省'}, {'provinceID': '630', 'city': '青海省'}, {'provinceID': '640', 'city': '宁夏回族自治区'}, {'provinceID': '650', 'city': '新疆维吾尔自治区'}, {'provinceID': '710', 'city': '台湾省'}, {'provinceID': '810', 'city': '香港特别行政区'}, {'provinceID': '820', 'city': '澳门特别行政区'}, {'provinceID': '900', 'city': '极地'}]

all_list = []
for city_obj in city_list:
    url = 'http://data.cma.cn/dataService/ajax.html'
    data = 'act=getStationsByProvinceID&provinceID={provinceID}&dataCode=A.0012.0001&type=se'

    numid = city_obj['provinceID']
    city = city_obj['city']
    body = data.format(provinceID=numid)
    response = requests.post(url,data=body,headers=headers)
    json_obj = json.loads(response.text)
    all_obj = {}
    item_list = []
    for data in json_obj['stations']:
        name = data['CNAME']
        quid = data['StationID']
        obj = {
            'name':name,
            'quid':quid,
        }
        item_list.append(obj)
    all_obj['city'] = city
    all_obj['provinceID'] = numid
    all_obj['quxian'] = item_list
    print(all_obj)
    all_list.append(all_obj)
print(all_list)

# import requests
# from lxml.etree import HTML
# headers = {
#     'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     'Accept-Encoding': "gzip, deflate",
#     'Accept-Language': "zh-CN,zh;q=0.9",
#     'Cache-Control': "no-cache",
#     'Connection': "keep-alive",
#     'Cookie': "PHPSESSID=t5i9fvrkj5h6jspjsma0230gl0; pgv_pvi=2796649472; pgv_si=s8206772224; Hm_lvt_d9508cf73ee2d3c3a3f628fe26bd31ab=1545033840; login_id_chat=0; degrDiCookie2=1; userLoginKey=8753b00096a88b57f63f6d0c3f4a75a2; trueName=%E9%BB%84%E5%AA%9B; userName=CC95032D68D56568231F2E619CA12094; login_name_chat=0; Hm_lpvt_d9508cf73ee2d3c3a3f628fe26bd31ab=1545206408",
#     'Host': "data.cma.cn",
#     'Pragma': "no-cache",
#     'Referer': "http://data.cma.cn/data/detail/dataCode/A.0012.0001.html",
#     'Upgrade-Insecure-Requests': "1",
#     'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
#     'cache-control': "no-cache",
#     'Postman-Token': "1d6497de-bb0f-4f43-b8f1-e7968504945b"
#     }
# response = requests.get('http://data.cma.cn/dataService/cdcindex/datacode/A.0012.0001/show_value/normal.html',headers=headers)
# response.encoding = 'utf8'
# html = HTML(response.text)
# names = html.xpath('//dl[@id="citySelect"]/dd/@alt')
# ids = html.xpath('//dl[@id="citySelect"]/dd/@data')
# item_list = []
# for name,id in zip(names,ids):
#     obj = {
#         'city': name,
#         'provinceID': id
#     }
#     item_list.append(obj)
# print(item_list)