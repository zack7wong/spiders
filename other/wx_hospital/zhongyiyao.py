#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import re
import time
import json

# response = requests.get('http://111.230.204.215/html/aa.html')
# response.encoding = 'utf8'
# html = HTML(response.text)
# divs = html.xpath('//div[@class="list-right icon-arrow"]/ul')
#
# catDic = []
# for div in divs:
#     lis = div.xpath('./li/a/@href')
#     print(lis)
#     for li in lis:
#         pid= re.search("javascript:toSelDoctor\('(\d+)','(.*?)','','(\d+)'\)",li).group(1)
#         catName = re.search("javascript:toSelDoctor\('(\d+)','(.*?)','','(\d+)'\)",li).group(2)
#         catId = re.search("javascript:toSelDoctor\('(\d+)','(.*?)','','(\d+)'\)",li).group(3)
#
#         obj = {
#             'pid':pid,
#             'catName':catName,
#             'catId':catId,
#         }
#         catDic.append(obj)
# print(catDic)


headers = {
    'Host': "hw29.yx129.net",
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Origin': "http://hw29.yx129.net",
    'X-Requested-With': "XMLHttpRequest",
    'User-Agent': "Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044506 Mobile Safari/537.36 MMWEBID/6924 MicroMessenger/7.0.3.1400(0x2700033B) Process/tools NetType/WIFI Language/zh_CN",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Referer': "http://hw29.yx129.net/register/doctor?register.appid=wxa18bac0f1c686d63&register.openId=oQqyat_r0ysQxWxwTyz3s4tewbXQ&register.deptCode=0004000&register.deptName=%25E5%25BF%2583%25E8%25A1%2580%25E7%25AE%25A1%25E7%25A7%2591%25E9%2597%25A8%25E8%25AF%258A&register.doctorCode=&register.childDeptCode=0027000",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,en-US;q=0.9",
    'Connection': "keep-alive",
    'cache-control': "no-cache",
}


def get_detail(pid,catId,doctorCode,date):
    headers['cookie'] = 'wxa18bac0f1c686d63_openId=oQqyat_r0ysQxWxwTyz3s4tewbXQ; Hm_lvt_5d2c204f0385209d909fc75ce81345d1=1552227976; dept=0004000; JSESSIONID=12F0A8B7D071D0AA9FB9BB1A4B9094D4; SPRINGSECURITY_SESSION_wxa18bac0f1c686d63="PT49Ij85Ij08PiI0P2NdfXVteFN+PHV/XXRbdHtYdXY/fzh4aXtuVF1TXllTRU5DQw=="; Hm_lpvt_5d2c204f0385209d909fc75ce81345d1=1552815627'
    url = 'http://hw29.yx129.net/register/timeInterval'
    body = 'register.appid=wxa18bac0f1c686d63&register.deptCode={pid}&register.childDeptCode={catId}&register.doctorCode={doctorCode}&register.regTime={date}&register.timeFlagSet=%5B1%5D'
    data = body.format(pid=pid,catId=catId,doctorCode=doctorCode,date=date)
    # print(data)
    response = requests.post(url,headers=headers,data=data)
    # print(response.text)

    json_obj = json.loads(response.text)
    if len(json_obj['content']['doctor']['listTi']) == 0:
        return ''

    maxTime = 0
    for data in json_obj['content']['doctor']['listTi']:
        beginTime = data['beginTime']
        endTime = int(data['endTime'].split(':')[0])
        if endTime > maxTime:
            maxTime = endTime

    del headers['cookie']

    if maxTime>12:
        return '下午'
    else:
        return '上午'

def start():
    date_list = []

    for i in range(10):
        addTime = i*3600*24
        userTime = time.strftime('%Y-%m-%d', time.localtime(time.time()+addTime))
        date_list.append(userTime)
    print(date_list)



    catId_list = [{'pid': '0000006', 'catId': '0000006', 'catName': '岭南名医门诊'}, {'pid': '0004000', 'catId': '0004000', 'catName': '内科门诊'}, {'pid': '0004000', 'catId': '0027000', 'catName': '心血管科门诊'}, {'pid': '0004000', 'catId': '0028000', 'catName': '脾胃病科门诊'}, {'pid': '0004000', 'catId': '0029000', 'catName': '肾病科门诊'}, {'pid': '0004000', 'catId': '0030000', 'catName': '脑病科门诊'}, {'pid': '0004000', 'catId': '0031000', 'catName': '呼吸科门诊'}, {'pid': '0004000', 'catId': '0032000', 'catName': '内分泌科门诊'}, {'pid': '0004000', 'catId': '0033000', 'catName': '血液科门诊'}, {'pid': '0004000', 'catId': '0037000', 'catName': '风湿病科门诊'}, {'pid': '0004000', 'catId': '0034000', 'catName': '普通内科门诊'}, {'pid': '0004000', 'catId': '0039000', 'catName': '中医内科门诊'}, {'pid': '0004100', 'catId': '0004100', 'catName': '内科夜诊'}, {'pid': '0017000', 'catId': '0017000', 'catName': '心理咨询室'}, {'pid': '0025000', 'catId': '0025000', 'catName': '肝炎肠道门诊'}, {'pid': '0012000', 'catId': '0012000', 'catName': '肿瘤科门诊'}, {'pid': '0005000', 'catId': '0005000', 'catName': '外科门诊'}, {'pid': '0005000', 'catId': '0005010', 'catName': '泌尿外科门诊'}, {'pid': '0005000', 'catId': '0005060', 'catName': '胃肠甲状腺外科门诊'}, {'pid': '0005000', 'catId': '0005070', 'catName': '肝胆外科门诊'}, {'pid': '0005000', 'catId': '0005030', 'catName': '心胸血管外科门诊'}, {'pid': '0005000', 'catId': '0005020', 'catName': '普通外科门诊'}, {'pid': '0005000', 'catId': '0018000', 'catName': '男性专科门诊'}, {'pid': '0005000', 'catId': '0005080', 'catName': '外科专家门诊'}, {'pid': '0005090', 'catId': '0005090', 'catName': '生殖医学科门诊(1)'}, {'pid': '0005091', 'catId': '0005091', 'catName': '生殖医学科门诊(2)'}, {'pid': '0005100', 'catId': '0005100', 'catName': '生育力评估门诊'}, {'pid': '0005040', 'catId': '0005040', 'catName': '乳腺科门诊'}, {'pid': '0010000', 'catId': '0010000', 'catName': '皮肤科门诊'}, {'pid': '0020000', 'catId': '0020000', 'catName': '美容室'}, {'pid': '0011000', 'catId': '0011000', 'catName': '肛肠科门诊'}, {'pid': '0024000', 'catId': '0024000', 'catName': '痛症门诊'}, {'pid': '0013000', 'catId': '0013000', 'catName': '妇科门诊'}, {'pid': '0001310', 'catId': '0001310', 'catName': '产科门诊'}, {'pid': '0013100', 'catId': '0013100', 'catName': '妇科夜诊'}, {'pid': '0014000', 'catId': '0014000', 'catName': '儿科门诊'}, {'pid': '0014000', 'catId': '0001410', 'catName': '新生儿科门诊'}, {'pid': '0014300', 'catId': '0014300', 'catName': '儿童治未病门诊'}, {'pid': '0014200', 'catId': '0014200', 'catName': '儿童保健门诊'}, {'pid': '0001410', 'catId': '0001410', 'catName': '新生儿科门诊'}, {'pid': '0014100', 'catId': '0014100', 'catName': '儿科夜诊'}, {'pid': '0006000', 'catId': '0006010', 'catName': '创伤骨科门诊'}, {'pid': '0006000', 'catId': '0006020', 'catName': '脊柱骨科门诊'}, {'pid': '0006000', 'catId': '0006030', 'catName': '关节骨科门诊'}, {'pid': '0006000', 'catId': '0006060', 'catName': '普通骨科门诊'}, {'pid': '0006000', 'catId': '0006070', 'catName': '骨科专家门诊'}, {'pid': '0006050', 'catId': '0006050', 'catName': '颅脑科门诊'}, {'pid': '0007000', 'catId': '0007000', 'catName': '眼科门诊'}, {'pid': '0008000', 'catId': '0008000', 'catName': '耳鼻喉科门诊'}, {'pid': '0015100', 'catId': '0015100', 'catName': '康复中心'}, {'pid': '0009000', 'catId': '0009000', 'catName': '针灸科门诊'}, {'pid': '0015000', 'catId': '0015000', 'catName': '推拿门诊'}, {'pid': '0016000', 'catId': '0016000', 'catName': '口腔科门诊'}, {'pid': '0005110', 'catId': '0005110', 'catName': '外科护理门诊'}, {'pid': '0005120', 'catId': '0005120', 'catName': '乳腺护理门诊'}, {'pid': '0012090', 'catId': '0012090', 'catName': '肿瘤护理门诊'}, {'pid': '0015200', 'catId': '0015200', 'catName': '神经康复门诊'}, {'pid': '0005130', 'catId': '0005130', 'catName': '肺小结节专病门诊'}, {'pid': '0015600', 'catId': '0015600', 'catName': '内科手法调理门诊'}, {'pid': '0015500', 'catId': '0015500', 'catName': '小儿推拿门诊'}, {'pid': '0022000', 'catId': '0022000', 'catName': '治未病门诊'}, {'pid': '0038000', 'catId': '0038000', 'catName': '流感预防门诊'}, {'pid': '0015400', 'catId': '0015400', 'catName': '产后手法康复门诊'}, {'pid': '0290000', 'catId': '0290000', 'catName': '药学门诊'}, {'pid': '0015300', 'catId': '0015300', 'catName': '颈腰关节痛症门诊'}, {'pid': '0004400', 'catId': '0004400', 'catName': '介入门诊'}, {'pid': '0005160', 'catId': '0005160', 'catName': '造口慢性伤口护理门诊'}, {'pid': '0006080', 'catId': '0006080', 'catName': '儿童骨科专科门诊'}, {'pid': '0005150', 'catId': '0005150', 'catName': '漏斗胸鸡胸专病门诊'}, {'pid': '0014400', 'catId': '0014400', 'catName': '儿科（新生儿）护理专科门诊'}, {'pid': '0024010', 'catId': '0024010', 'catName': '骨科护理门诊'}, {'pid': '0039200', 'catId': '0039200', 'catName': '中医特色治疗门诊'}, {'pid': '0005140', 'catId': '0005140', 'catName': '手汗症专病门诊'}]

    url = "http://hw29.yx129.net/register/ajax?act=getRDoctors"

    payload = "register.appid=wxa18bac0f1c686d63&register.deptCode={pid}&register.childDeptCode={catId}&register.doctorCode=&register.beginDate={date}&register.regTime={date}"


    for date in date_list:
        with open(date + '.csv', 'w', encoding='gbk') as f:
            pass
        print(date)
        for catObj in catId_list:
            print(catObj['catName'])
            data = payload.format(pid=catObj['pid'], catId=catObj['catId'],date=date)
            # print(data)
            # data = 'register.appid=wxa18bac0f1c686d63&register.openId=oQqyat_r0ysQxWxwTyz3s4tewbXQ&register.deptCode=0000006&register.childDeptCode=0000006&register.deptName=%25E5%25B2%25AD%25E5%258D%2597%25E5%2590%258D%25E5%258C%25BB%25E9%2597%25A8%25E8%25AF%258A&register.doctorCode=&register.beginDate=2019-03-18&register.regTime=2019-03-18'
            try:
                response = requests.request("POST", url, data=data, headers=headers,timeout=10)
            except:
                print('error')
                continue

            # print(response.text)

            json_obj = json.loads(response.text)

            for data in json_obj['doctors']:
                name = data['doctorName']
                if name:
                    save_res = catObj['catName']+','+name+'\n'
                    print(save_res)
                    with open(date+'.csv', 'a', encoding='gbk') as f:
                        f.write(save_res)

                # if data['leftCount']>0:
                #     print(data)
                #     name = data['doctorName']
                #     deptName = data['deptName']
                #     doctorCode = data['doctorCode']
                #
                #     allStr = get_detail(catObj['pid'],catObj['catId'],doctorCode,date)
                #     if allStr !='':
                #
                #         save_res = name+','+deptName+','+date+','+allStr+'\n'
                #         print(save_res)
                #         with open('结果.csv','a',encoding='gbk') as f:
                #             f.write(save_res)




if __name__ == '__main__':
    start()