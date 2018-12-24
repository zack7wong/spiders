#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
import json
import time

headers = {
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    # 'Cookie': "p_phone_400=4007-999-999; p_phone_level=0; p_global_phone=%2B0086-25-8685-9999; _tacau=MCwxM2EwNGYwOC03MzE2LTY0NjAtYjNiZS1lOWFiZTE2MjhmMjAs; _tact=NTlhNDVjNmQtZTZiMC0xMThmLTQxMDMtMmI5MjRmZmM1Y2Qz; tuniuuser_citycode=NDE0; __ozlvd1940=1545219622; MOBILE_APP_SETTING_STATE-128=CLOSE; isHaveShowPriceTips=1; __utma=1.2029902434.1545219587.1545219587.1545219587.1; __utmz=1.1545219587.1.1.utmcsr=google|utmgclid=CjwKCAiA9efgBRAYEiwAUT-jtOFrIsPdlwB7CZ15DjzVowBnI9tsQH1oqo3EJOZ9G8avaroI-zyGABoCNXwQAvD_BwE|utmccn=SE|utmcmd=cpc|utmctr=(not%20provided); UM_distinctid=167c64cf96716e-054d90c0305d93-35627600-1fa400-167c64cf96878f; fp_ver=4.5.2; BSFIT_EXPIRATION=1545274154372; BSFIT_OkLJUJ=FFJ6TJ1gA4af5iC5FTvAKZVfM54iBmJQ; BSFIT_DEVICEID=WgifWmj64PdH_yrWKLE3B47kiomiJ2-gKNy6h4_MwrpyfmZgangTHCD5SG025LTaNtkVE111kVvo5nz5yG2qBqnMm43LVg2fBRRhV7jYdbDpaucDpz4FkmB8k-vrxEi22_Bx1qWHD0AipcrhkpNOnqYX5hbA2Lro; PageSwitch=1%2C213612736; MOBILE_APP_SETTING_OPEN-128=1; search_keyword=%E6%80%9D%E6%98%8E%E5%8C%BA%E9%85%92%E5%BA%97; tuniuuser_ip_citycode=NDE0; tuniu_searched=a%3A3%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A7%3A%22keyword%22%3Bs%3A6%3A%22%E9%85%92%E5%BA%97%22%3Bs%3A4%3A%22link%22%3Bs%3A23%3A%22http%3A%2F%2Fhotel.tuniu.com%2F%22%3B%7Di%3A1%3Ba%3A2%3A%7Bs%3A7%3A%22keyword%22%3Bs%3A15%3A%22%E6%80%9D%E6%98%8E%E5%8C%BA%E9%85%92%E5%BA%97%22%3Bs%3A4%3A%22link%22%3Bs%3A65%3A%22http%3A%2F%2Fs.tuniu.com%2Fsearch_complex%2Fhotel-xm-0-%E6%80%9D%E6%98%8E%E5%8C%BA%2F%3Fjump%3Dauto%22%3B%7Di%3A2%3Ba%3A2%3A%7Bs%3A7%3A%22keyword%22%3Bs%3A9%3A%22%E6%80%9D%E6%98%8E%E5%8C%BA%22%3Bs%3A4%3A%22link%22%3Bs%3A52%3A%22http%3A%2F%2Fwww.tuniu.com%2Fg40956%2Fwhole-xm-0%2Flist-h0-j0_0%2F%22%3B%7D%7D; hotel_view_history_new_guid=E2C35335-6B21-162E-AB59-7DCA8D39DC6A; tuniu_partner=MTU1OSwwLCw0MWJmNjc1OGFhOWU5ZGMwNDBkZDc2YTJhMDRkMjM2Mg%3D%3D; _tacz2=taccsr%3Dgoogle%7Ctacccn%3D%28cpc%29%7Ctaccmd%3DSE%7Ctaccct%3D%28none%29%7Ctaccrt%3D%7Bkeywordid%7D_192211557056; _taca=1545219586906.1545568035636.1545638582551.3; _tacb=MDAyZGI5NzMtYThkNS1jODAxLTY1ZDMtYTZjNWVlZDExOGNk; _tacc=1; __utmc=1; Hm_lvt_51d49a7cda10d5dd86537755f081cc02=1545219587,1545219999,1545568038,1545638583; OLBSESSID=uaosjdvdjgtucutm231alogio4; __xsptplusUT_352=1; __xsptplus352=352.4.1545638587.1545638587.1%231%7Cgoogle%7Ccpc%7CSE%7C%7C%23%23gC699atYSS2FYfo9QfH2ut5GxN-sE8dG%23; clickCache=%5B%7B%22key%22%3A1545638582430%2C%22url%22%3A%22http%3A%2F%2Fwww.tuniu.com%2F%3Fp%3D1559%26utm_source%3Dgoogle%26utm_medium%3Dcpc%26utm_campaign%3DSE%26kw%3D%7Bkeywordid%7D_192211557056%26gclid%3DCj0KCQiApILhBRD1ARIsAOXWTzt61e7uEcB4n6LpUhnY7ZI5qt_FUNPhTl0PQnz1gKcZrA390rExbFQaAlRtEALw_wcB%22%2C%22pageName%22%3A%22%E5%BA%A6%E5%81%87%3A%E5%8E%A6%E9%97%A8%3A%E9%A6%96%E9%A1%B5%3Axm%22%2C%22referer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22events%22%3A%5B%7B%22text%22%3A%22%E5%87%BA%E7%8E%B0_%E9%9D%9E%E6%B4%BB%E5%8A%A8%E5%BA%95%E9%80%9A_%E8%87%AA%E5%8A%A8%E5%BC%B9%E5%87%BA%22%2C%22x%22%3A0%2C%22y%22%3A0%2C%22lg%22%3A1545638588440%7D%5D%7D%5D; tuniu_zeus=M18yXzNfMV8xXzE6Omh0dHA6Ly94bS50dW5pdS5jb20vOjoyMDE4LTEyLTE5IDE5OjQwOjIx%2CM18zXzFfMV8xXzI6Omh0dHA6Ly93d3cudHVuaXUuY29tLz9wPTE1NTkmdXRtX3NvdXJjZT1nb29nbGUmdXRtX21lZGl1bT1jcGMmdXRtX2NhbXBhaWduPVNFJmt3PXtrZXl3b3JkaWR9XzE5MjIxMTU1NzA1MyZnY2xpZD1FQUlhSVFvYkNoTUlxYTJ3eXZtMTN3SVZFQ1FyQ2gwVzFnUWlFQUFZQVNBQUVnTGxUUERfQndFOjoyMDE4LTEyLTIzIDIwOjMwOjA4%2CM18zXzFfMV8xXzI6Omh0dHA6Ly93d3cudHVuaXUuY29tLz9wPTE1NTkmdXRtX3NvdXJjZT1nb29nbGUmdXRtX21lZGl1bT1jcGMmdXRtX2NhbXBhaWduPVNFJmt3PXtrZXl3b3JkaWR9XzE5MjIxMTU1NzA1NiZnY2xpZD1DajBLQ1FpQXBJTGhCUkQxQVJJc0FPWFdUenQ2MWU3dUVjQjRuNkxwVWhuWTdaSTVxdF9GVU5QaFRsMFBRbnoxZ0tjWnJBMzkwckV4YkZRYUFsUnRFQUx3X3djQjo6MjAxOC0xMi0yNCAxNjowMzowOQ%3D%3D; __utma=1.2029902434.1545219587.1545219587.1545219587.1; __utmz=1.1545219587.1.1.utmcsr=google|utmgclid=CjwKCAiA9efgBRAYEiwAUT-jtOFrIsPdlwB7CZ15DjzVowBnI9tsQH1oqo3EJOZ9G8avaroI-zyGABoCNXwQAvD_BwE|utmccn=SE|utmcmd=cpc|utmctr=(not%20provided); hotel_index_search_history=eyJfNDE0Ijp7ImNoZWNraW5kYXRlIjoiMjAxOC0xMi0yNSIsImNoZWNrb3V0ZGF0ZSI6IjIwMTgtMTItMjYiLCJjaXR5X2lkIjoiNDE0IiwiY2l0eV9uYW1lIjoi5Y6m6ZeoIn19; __utmb=1.4.9.1545638596870; hotel_checkindate=2018-12-25; hotel_checkoutdate=2018-12-26; hotel_order_begin_date=2018-12-25; hotel_order_end_date=2018-12-26; __utmc=1; __utmb=1.5.9.1545638596870; CNZZDATA5726564=cnzz_eid%3D1844074705-1545217794-http%253A%252F%252Fwww.tuniu.com%252F%26ntime%3D1545633927; _pzfxuvpc=1545219587200%7C1429496485756268080%7C10%7C1545638599104%7C3%7C1441768881743744674%7C9782968928123106294; _pzfxsvpc=9782968928123106294%7C1545638582586%7C3%7Chttps%3A%2F%2Fwww.google.com%2F; Hm_lpvt_51d49a7cda10d5dd86537755f081cc02=1545638599; rg_entrance=010000%2F003001%2F000013%2F000000",
    'Host': "hotel.tuniu.com",
    'Pragma': "no-cache",
    'Referer': "http://hotel.tuniu.com/",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest",
    'cache-control': "no-cache",
    'Postman-Token': "de7e6a9c-4d60-46c8-b5f1-1c77cfb6b6a1"
    }

url = 'http://hotel.tuniu.com/ajax/list?search%5BcityCode%5D=414&search%5BcheckInDate%5D={sdate}&search%5BcheckOutDate%5D={edate}&search%5Bkeyword%5D=&suggest=&sort%5Bfirst%5D%5Bid%5D=recommend&sort%5Bfirst%5D%5Btype%5D=&sort%5Bsecond%5D=&sort%5Bthird%5D=cash-back-after&page={page}&returnFilter=0'

num = 1
for i in range(1,6):
    try:
        sdate = time.strftime('%Y-%m-%d',time.localtime())
        edate = time.strftime('%Y-%m-%d',time.localtime(int(time.time())+60*60*24))
        start_url = url.format(sdate=sdate,edate=edate,page=str(i))
        response = requests.get(start_url,headers=headers)
        print(response.text)
        json_obj = json.loads(response.text)

        for data in json_obj['data']['list']:
            name = data['name']
            address = data['address']
            decorateYear = data['decorateYear']
            startPrice = str(data['startPrice'])
            remarkScore = str(data['remarkScore'])
            remarkCount = str(data['remarkCount'])

            res = str(num)+','+name+','+address+','+decorateYear+','+startPrice+','+remarkScore+','+remarkCount+'\n'
            print(res)
            with open('results.csv','a',encoding='utf8') as f:
                f.write(res)
            num+=1
    except:
        continue