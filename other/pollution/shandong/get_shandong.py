#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import math
import db

headers = {
    'Accept': "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Length': "157",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Cookie': "ASP.NET_SessionId=c4xqr445yr2n1pyx10pjiq55",
    'Pragma': "no-cache",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest",
    'cache-control': "no-cache",
    }

get_headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Cookie': "ASP.NET_SessionId=l2xvgnyqpsfv1s45yd2j0m55",
    'Host': "221.214.107.80:8403",
    'Pragma': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "80fbcb4f-7bfd-4794-9c58-9d15fce4e734"
    }

def start():
    item_list = []
    with open('shandong_id3.txt') as f:
        results = f.readlines()
        for res in results:
            ip = res.split(',')[0]
            entCode = res.split(',')[5]
            name = res.split(',')[6]
            EntTypeName = res.split(',')[7].strip()
            obj ={
                'ip':ip,
                'entCode':entCode,
                'name':name,
                'EntTypeName':EntTypeName,
            }
            item_list.append(obj)

    for item in item_list:
        try:
            print(item)
            url = 'http://{ip}/ajax/npublic/NData.ashx'
            body = 'Method=GetMonitorDataList&entCode={entCode}&subType=&subID=&year=2019&itemCode=&dtStart=2014-01-01&dtEnd=2019-02-26&monitoring=&bReal=false&page={pageToken}&rows=1000'

            #获取第一页
            start_url = url.format(ip=item['ip'])
            data = body.format(entCode=item['entCode'],pageToken=1)

            get_start_url = 'http://{ip}/ajax/npublic/NData.ashx?Method=GetMonitorDataList&entCode={entCode}&subType=&subID=&year=2019&itemCode=&dtStart=2014-01-01&dtEnd=2019-02-26&monitoring=&bReal=false&page={pageToken}&rows=1000'
            get_start_url = get_start_url.format(ip=item['ip'], entCode=item['entCode'],pageToken=1)
            print(get_start_url)
            try:
                response = requests.get(get_start_url,headers=get_headers,timeout=15)
                print(response.text[:100])
            except:
                continue


            if '无法找到资源' in response.text:
                try:
                    response = requests.post(start_url, headers=headers, data=data, timeout=15)
                    print(start_url)
                    print(data)
                    print(response.text[:100])
                except:
                    continue

            try:
                if response.text[0] == '(' and response.text[-1] == ')':
                    json_obj = json.loads(response.text[1:-1])
                else:
                    json_obj = json.loads(response.text)
            except:
                continue



            if json_obj['total'] == 0:
                print('无数据')
                continue

            # 处理第一页
            #企业名称、污染源类型（废水、废气）、监测站点、监测项目、监测时间、监测类型、监测频次、监测值、执行标准、超标倍数
            # title, EntTypeName, jiancedianName, jianceProject, jianceTime, jianceType, jiancePinci, jianceValue, zhixingbiaozhun, chaobiaobeishu
            for each_data in json_obj['rows']:
                title = item['name']
                EntTypeName = item['EntTypeName']
                jiancedianName = each_data['Subname']
                jianceProject = each_data['Itemname']
                jianceTime = each_data['Ac005_datetime']
                jianceType = each_data['Typecode']
                jiancePinci = each_data['Mfrequency']
                jianceValue = each_data['Ac005_value']
                zhixingbiaozhun = each_data['Stander']
                chaobiaobeishu = each_data['Ac005_cbbs']

                print(title, EntTypeName, jiancedianName, jianceProject, jianceTime, jianceType, jiancePinci, jianceValue, zhixingbiaozhun, chaobiaobeishu)

                sql = "insert into shandong(title, EntTypeName, jiancedianName, jianceProject, jianceTime, jianceType, jiancePinci, jianceValue, zhixingbiaozhun, chaobiaobeishu)" \
                          " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s')" \
                          % (title, EntTypeName, jiancedianName, jianceProject, jianceTime, jianceType, jiancePinci,
                             jianceValue, zhixingbiaozhun, chaobiaobeishu)+"ON DUPLICATE KEY UPDATE title='%s'"%(title)
                dbclient.save(sql)


            # 获取总页数
            totalPage = math.ceil(json_obj['total'] / 1000)
            print('总页数:'+str(totalPage))

            # 处理剩余页数
            for i in range(2, totalPage + 1):
                print('当前页：'+str(i))
                start_url = url.format(ip=item['ip'])
                data = body.format(entCode=item['entCode'], pageToken=i)

                get_start_url = 'http://{ip}/ajax/npublic/NData.ashx?Method=GetMonitorDataList&entCode={entCode}&subType=&subID=&year=2019&itemCode=&dtStart=2014-01-01&dtEnd=2019-02-26&monitoring=&bReal=false&page={pageToken}&rows=1000'
                get_start_url = get_start_url.format(ip=item['ip'],entCode=item['entCode'], pageToken=i)
                print(get_start_url)
                try:
                    response = requests.get(get_start_url, headers=get_headers, timeout=15)
                    print(response.text[:100])
                except:
                    continue

                if '无法找到资源' in response.text:
                    try:
                        response = requests.post(start_url, headers=headers, data=data, timeout=15)
                        print(start_url)
                        print(data)
                        print(response.text[:100])
                    except:
                        continue

                try:
                    if response.text[0] == '(' and response.text[-1] == ')':
                        json_obj = json.loads(response.text[1:-1])
                    else:
                        json_obj = json.loads(response.text)
                except:
                    continue


                for each_data in json_obj['rows']:
                    title = item['name']
                    EntTypeName = item['EntTypeName']
                    jiancedianName = each_data['Subname']
                    jianceProject = each_data['Itemname']
                    jianceTime = each_data['Ac005_datetime']
                    jianceType = each_data['Typecode']
                    jiancePinci = each_data['Mfrequency']
                    jianceValue = each_data['Ac005_value']
                    zhixingbiaozhun = each_data['Stander']
                    chaobiaobeishu = each_data['Ac005_cbbs']

                    print(title, EntTypeName, jiancedianName, jianceProject, jianceTime, jianceType, jiancePinci,
                          jianceValue, zhixingbiaozhun, chaobiaobeishu)

                    sql = "insert into shandong(title, EntTypeName, jiancedianName, jianceProject, jianceTime, jianceType, jiancePinci, jianceValue, zhixingbiaozhun, chaobiaobeishu)" \
                          " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s')" \
                          % (title, EntTypeName, jiancedianName, jianceProject, jianceTime, jianceType, jiancePinci,
                             jianceValue, zhixingbiaozhun, chaobiaobeishu)+"ON DUPLICATE KEY UPDATE title='%s'"%(title)
                    dbclient.save(sql)
        except:
            continue




if __name__ == '__main__':
    dbclient = db.MysqlClient()
    start()