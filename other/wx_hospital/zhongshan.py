#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import time

headers = {
    'Host': "sp.yx129.cn",
    # 'Content-Length': "422",
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Origin': "http://sp.yx129.cn",
    'X-Requested-With': "XMLHttpRequest",
    'User-Agent': "Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044506 Mobile Safari/537.36 MMWEBID/6924 MicroMessenger/7.0.3.1400(0x2700033B) Process/tools NetType/4G Language/zh_CN",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Referer': "http://sp.yx129.cn/mobileApp/register/branchDeptes",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,en-US;q=0.9",
    'Cookie': "selectDeptCode=1000004; acw_tc=7819730715522289482596685e78dbaf0df1daf502e2c9cd4a4c7fac70fbfc; Hm_lvt_5d2c204f0385209d909fc75ce81345d1=1552228957; JSESSIONID=1AE676198B0AE9C68D16828673810C95; Hm_lpvt_5d2c204f0385209d909fc75ce81345d1=1552916237",
    'Connection': "keep-alive",
    'cache-control': "no-cache",
}

catId_list ={"catId":"100001","catName":"特诊医疗"},{"catId":"1000001","catName":"内科"},{"catId":"1000002","catName":"外科"},{"catId":"1000003","catName":"神经科"},{"catId":"1000004","catName":"感染病科(肝脏内科)"},{"catId":"1000005","catName":"妇产科"},{"catId":"1000006","catName":"儿科"},{"catId":"1000007","catName":"儿童发育行为中心"},{"catId":"1000008","catName":"耳鼻喉科"},{"catId":"1000009","catName":"口腔科"},{"catId":"10000010","catName":"眼科"},{"catId":"10000011","catName":"精神（心理）科"},{"catId":"10000012","catName":"中医科"},{"catId":"10000013","catName":"针灸科"},{"catId":"10000014","catName":"康复科"},{"catId":"10000015","catName":"皮肤科"},{"catId":"10000016","catName":"不育与性医学科"},{"catId":"10000017","catName":"生殖医学中心"},{"catId":"10000018","catName":"预防保健科"},{"catId":"10000019","catName":"麻醉科"},{"catId":"10000020","catName":"疼痛科"},{"catId":"10000021","catName":"放射科"},{"catId":"10000022","catName":"放射治疗科"},{"catId":"10000024","catName":"核医学科"},{"catId":"10000025","catName":"超声科"},{"catId":"10000023","catName":"病理科"},{"catId":"10000026","catName":"营养科"},{"catId":"10000027","catName":"药学门诊"},{"catId":"10000028","catName":"造口科"},{"catId":"10000030","catName":"全科医学门诊"},{"catId":"10000029","catName":"静脉导管门诊"},

def start():
    date_list = []

    for i in range(10):
        addTime = i * 3600 * 24
        userTime = time.strftime('%Y-%m-%d', time.localtime(time.time() + addTime))
        date_list.append(userTime)
    print(date_list)

    start_url = 'http://sp.yx129.cn/mobileApp/register/querySubDepts'
    body = 'openId=oAFPxs9TbnwSPQO9l6iyq76Je6O4&appCode=wechat&appId=wx0de227fe13646a00&hospitalId=441fb80035b2440086507e04afb784ca&hospitalCode=zsdxdsfsyy&hospitalName=%E4%B8%AD%E5%B1%B1%E5%A4%A7%E5%AD%A6%E9%99%84%E5%B1%9E%E7%AC%AC%E4%B8%89%E5%8C%BB%E9%99%A2&branchHospitalId=cd63b140c0ee4444a2f8509d806b971b&branchHospitalCode=2&branchHospitalName=%E5%A4%A9%E6%B2%B3%E9%99%A2%E5%8C%BA&regType=&deptCode={catId}&deptName=&doctorCode='

    for date in date_list:
        with open(date + '.csv', 'w', encoding='gbk') as f:
            pass
        print(date)
        for catObj in catId_list:
            print(catObj)
            data = body.format(catId=catObj['catId'])
            response = requests.post(start_url, data=data, headers=headers)
            # print(response.text)
            json_obj = json.loads(response.text)
            for subcatObj in json_obj['message']['subDepts']:
                deptCode = subcatObj['deptCode']
                print(subcatObj['deptName'])
                detail_url = 'http://sp.yx129.cn//mobileApp/register/doctor/queryDoctorList'
                detail_body = 'openId=oAFPxs9TbnwSPQO9l6iyq76Je6O4&showDays=8&appCode=wechat&appId=wx0de227fe13646a00&hospitalId=441fb80035b2440086507e04afb784ca&hospitalCode=zsdxdsfsyy&hospitalName=%E4%B8%AD%E5%B1%B1%E5%A4%A7%E5%AD%A6%E9%99%84%E5%B1%9E%E7%AC%AC%E4%B8%89%E5%8C%BB%E9%99%A2&branchHospitalId=cd63b140c0ee4444a2f8509d806b971b&branchHospitalCode=2&branchHospitalName=%E5%A4%A9%E6%B2%B3%E9%99%A2%E5%8C%BA&regType=&deptCode={deptCode}&deptName=%E5%91%BC%E5%90%B8%E5%86%85%E7%A7%91%E9%97%A8%E8%AF%8A&doctorCode=&selectRegDate={date}&category=&isHasDutyReg=1&nextDay={date}&isSearchDoctor=&isHasAppointmentReg=1&doctorPic=&personalAccountFee=&overallPlanFee=&regChannel='

                detail_data = detail_body.format(deptCode=deptCode, date=date)
                detail_response = requests.post(detail_url, headers=headers, data=detail_data)
                # print(detail_response.text)
                detail_json_obj = json.loads(detail_response.text)
                if isinstance(detail_json_obj['message']['doctors'],list):
                    for detail_data in detail_json_obj['message']['doctors']:
                        if detail_data['titleNo'] !=999:
                            save_deptName = detail_data['deptName']
                            save_doctorName = detail_data['doctorName']
                            if save_doctorName:
                                save_res = save_deptName + ',' + save_doctorName + '\n'
                                print(save_res)
                                with open(date + '.csv', 'a', encoding='gbk') as f:
                                    f.write(save_res)

                print('暂停10秒')
                time.sleep(10)
            print('暂停10秒')
            time.sleep(10)


if __name__ == '__main__':
    start()