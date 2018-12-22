#!/usr/bin/env python
# -*- coding:utf-8 -*-

import download
from lxml.etree import HTML
from lxml import etree
from urllib.parse import quote
import time
import json
import xlwt
import xlrd
import requests
from hashlib import md5


city_list = [{'city':'东明石化1','id':'1668'},{'city':'东明石化2','id':'1696'},{'city':'东明中油燃料石化有限公司','id':'14095'}]

headers = {
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Length': "293",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    # 'Cookie': "autoLogin=null; user=null; pwd=null; ASP.NET_SessionId=mgo1ur55g1yfwvqjpz251hb4",
    'Host': "219.146.175.226:8406",
    'Origin': "http://219.146.175.226:8406",
    'Pragma': "no-cache",
    'Referer': "http://219.146.175.226:8406/webs/WasteWater/QueryAnalysis/HistoryReportQUIDYN/HistoryReport.aspx",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest",
    'cache-control': "no-cache",
    'Postman-Token': "3b25e77b-5ae3-47b5-82dc-f867322366a1"
    }

feiqi_url = 'http://219.146.175.226:8406/webs/ajax/WasteGas/QueryAnalysis/HistoryReportQUIDYN/HistoryReport.ashx'
feiqi_body = 'Method=QueryHistoryReport&subid={subid}&subname={subname}&start={start}&end={end}&index=1&sort=1&YWGS=&showValidate=0&multiCode=201%2C203%2C207%2C205%2C210&codes=201%2C203%2C207%2C209%2C525%2C210%2C545%2C546%2C205%2C221&showUpload=0&page=1&rows=20'

#东明石化集团 1671
feishui_url = 'http://219.146.175.226:8406/webs/ajax/WasteWater/QueryAnalysis/HistoryReportQUIDYN/HistoryReport.ashx'
feishui_body = 'Method=QueryHistoryReport&subid=1671&subname=%E4%B8%9C%E6%98%8E%E7%9F%B3%E5%8C%96%E9%9B%86%E5%9B%A2&start={start}&end={end}&index=1&sort=1&showValidate=0&multiCode=311%2C313%2C316%2C466%2C494&showUpload=0&YWGS=&codes=302%2C311%2C316%2C494%2C495&page=1&rows=20'


class RClient(object):
    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password.encode()).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('captcha.png', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers,
                          timeout=30)
        return r.json()

    def rk_report_error(self, im_id):
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers, timeout=30)
        return r.json()

def init_xls_file():
    a = 9
    b = 18
    c = 27
    # 写入excel
    # 参数对应 行, 列, 值
    # worksheet.write(0, 0, label='this is test')

    #1
    sheet.write_merge(0, 0, 0, 6, '东明石化1',style)
    sheet.write_merge(1, 3,0,0, '时间',style)
    sheet.write_merge(1, 1, 1, 3, '二氧化硫', style)
    sheet.write_merge(1, 1, 4, 6, '氮氧化物', style)
    sheet.write(2, 1, '实测浓度', style)
    sheet.write(2, 2, '折算浓度', style)
    sheet.write(2, 3, '排放量', style)
    sheet.write(2, 4, '实测浓度', style)
    sheet.write(2, 5, '折算浓度', style)
    sheet.write(2, 6, '排放量', style)
    sheet.write(3, 1, '(mg/M3)', style)
    sheet.write(3, 2, '(mg/M3)', style)
    sheet.write(3, 3, '(kg)', style)
    sheet.write(3, 4, '(mg/M3)', style)
    sheet.write(3, 5, '(mg/M3)', style)
    sheet.write(3, 6, '(kg)', style)

    sheet.write_merge(5, 7,0,0, '时间',style)
    sheet.write_merge(5, 5, 1, 3, '颗粒物', style)
    sheet.write(6, 1, '实测浓度', style)
    sheet.write(6, 2, '折算浓度', style)
    sheet.write(6, 3, '排放量', style)
    sheet.write(5, 4, '氧含量', style)
    sheet.write(5, 5, '烟气温度', style)
    sheet.write(5, 6, '废气排放量', style)
    sheet.write(7, 1, '(mg/M3)', style)
    sheet.write(7, 2, '(mg/M3)', style)
    sheet.write(7, 3, '(kg)', style)
    sheet.write(6, 4, '（%）', style)
    sheet.write(6, 5, '（C°）', style)
    sheet.write(6, 6, '(m3/h)', style)


    #2
    sheet.write_merge(0+a, 0+a, 0, 6, '东明石化2',style)
    sheet.write_merge(1+a, 3+a,0,0, '时间',style)
    sheet.write_merge(1+a, 1+a, 1, 3, '二氧化硫', style)
    sheet.write_merge(1+a, 1+a, 4, 6, '氮氧化物', style)
    sheet.write(2+a, 1, '实测浓度', style)
    sheet.write(2+a, 2, '折算浓度', style)
    sheet.write(2+a, 3, '排放量', style)
    sheet.write(2+a, 4, '实测浓度', style)
    sheet.write(2+a, 5, '折算浓度', style)
    sheet.write(2+a, 6, '排放量', style)
    sheet.write(3+a, 1, '(mg/M3)', style)
    sheet.write(3+a, 2, '(mg/M3)', style)
    sheet.write(3+a, 3, '(kg)', style)
    sheet.write(3+a, 4, '(mg/M3)', style)
    sheet.write(3+a, 5, '(mg/M3)', style)
    sheet.write(3+a, 6, '(kg)', style)


    sheet.write_merge(5+a, 7+a,0,0, '时间',style)
    sheet.write_merge(5+a, 5+a, 1, 3, '颗粒物', style)
    sheet.write(6+a, 1, '实测浓度', style)
    sheet.write(6+a, 2, '折算浓度', style)
    sheet.write(6+a, 3, '排放量', style)
    sheet.write(5+a, 4, '氧含量', style)
    sheet.write(5+a, 5, '烟气温度', style)
    sheet.write(5+a, 6, '废气排放量', style)
    sheet.write(7+a, 1, '(mg/M3)', style)
    sheet.write(7+a, 2, '(mg/M3)', style)
    sheet.write(7+a, 3, '(kg)', style)
    sheet.write(6+a, 4, '（%）', style)
    sheet.write(6+a, 5, '（C°）', style)
    sheet.write(6+a, 6, '(m3/h)', style)

    #3
    sheet.write_merge(0+b, 0+b, 0, 6, '东明中油燃料石化有限公司（催化车间）',style)
    sheet.write_merge(1+b, 3+b,0,0, '时间',style)
    sheet.write_merge(1+b, 1+b, 1, 3, '二氧化硫', style)
    sheet.write_merge(1+b, 1+b, 4, 6, '氮氧化物', style)
    sheet.write(2+b, 1, '实测浓度', style)
    sheet.write(2+b, 2, '折算浓度', style)
    sheet.write(2+b, 3, '排放量', style)
    sheet.write(2+b, 4, '实测浓度', style)
    sheet.write(2+b, 5, '折算浓度', style)
    sheet.write(2+b, 6, '排放量', style)
    sheet.write(3+b, 1, '(mg/M3)', style)
    sheet.write(3+b, 2, '(mg/M3)', style)
    sheet.write(3+b, 3, '(kg)', style)
    sheet.write(3+b, 4, '(mg/M3)', style)
    sheet.write(3+b, 5, '(mg/M3)', style)
    sheet.write(3+b, 6, '(kg)', style)


    sheet.write_merge(5+b, 7+b,0,0, '时间',style)
    sheet.write_merge(5+b, 5+b, 1, 3, '颗粒物', style)
    sheet.write(6+b, 1, '实测浓度', style)
    sheet.write(6+b, 2, '折算浓度', style)
    sheet.write(6+b, 3, '排放量', style)
    sheet.write(5+b, 4, '氧含量', style)
    sheet.write(5+b, 5, '烟气温度', style)
    sheet.write(5+b, 6, '废气排放量', style)
    sheet.write(7+b, 1, '(mg/M3)', style)
    sheet.write(7+b, 2, '(mg/M3)', style)
    sheet.write(7+b, 3, '(kg)', style)
    sheet.write(6+b, 4, '（%）', style)
    sheet.write(6+b, 5, '（C°）', style)
    sheet.write(6+b, 6, '(m3/h)', style)


    #4
    sheet.write_merge(0 + c, 0 + c, 0, 6, '东明石化集团（废水总排口）', style)
    sheet.write_merge(1 + c, 3 + c, 0, 0, '时间', style)
    sheet.write_merge(1 + c, 1 + c, 1, 2, '化学需氧量', style)
    sheet.write_merge(1 + c, 1 + c, 3, 4, '氨氮', style)
    sheet.write_merge(1 + c, 1 + c, 5, 5, '小时流量', style)
    sheet.write_merge(1 + c, 3 + c, 6, 6, 'PH', style)
    sheet.write(2 + c, 1, '浓度', style)
    sheet.write(2 + c, 2, '排放量', style)
    sheet.write(2 + c, 3, '浓度', style)
    sheet.write(2 + c, 4, '排放量', style)
    sheet.write(2 + c, 5, '(m³/h)', style)
    sheet.write(3+c, 1, '（mg/l)', style)
    sheet.write(3+c, 2, '(kg)', style)
    sheet.write(3+c, 3, '（mg/l)', style)
    sheet.write(3+c, 4, '(kg)', style)



def read():
    data = xlrd.open_workbook('res.xls')
    table = data.sheets()[0]  # 通过索引顺序获取
    # table = data.sheet_by_index(0)  # 通过索引顺序获取
    # table = data.sheet_by_name(u'Sheet1')  # 通过名称获取
    shihua1Date = table.cell(4, 0).value
    print(data)

def save_old(name,i):
    print(name + ' 暂无新数据，使用上一次的数据显示')
    sheet.write(4+i, 0, table.cell(4+i, 0).value, styleRes)
    sheet.write(4+i, 1, table.cell(4+i, 1).value, styleRes)
    sheet.write(4+i, 2, table.cell(4+i, 2).value, styleRes)
    sheet.write(4+i, 3, table.cell(4+i, 3).value, styleRes)
    sheet.write(4+i, 4, table.cell(4+i, 4).value, styleRes)
    sheet.write(4+i, 5, table.cell(4+i, 5).value, styleRes)
    sheet.write(4+i, 6, table.cell(4+i, 6).value, styleRes)

    sheet.write(8+i, 0, table.cell(8+i, 0).value, styleRes)
    sheet.write(8+i, 1, table.cell(8+i, 1).value, styleRes)
    sheet.write(8+i, 2, table.cell(8+i, 2).value, styleRes)
    sheet.write(8+i, 3, table.cell(8+i, 3).value, styleRes)
    sheet.write(8+i, 4, table.cell(8+i, 4).value, styleRes)
    sheet.write(8+i, 5, table.cell(8+i, 5).value, styleRes)
    sheet.write(8+i, 6, table.cell(8+i, 6).value, styleRes)

def save_old_feishui(name):
    print(name+' 暂无新数据，使用上一次的数据显示')
    sheet.write(31, 0, table.cell(31, 0).value, styleRes)
    sheet.write(31, 1, table.cell(31, 1).value, styleRes)
    sheet.write(31, 2, table.cell(31, 2).value, styleRes)
    sheet.write(31, 3, table.cell(31, 3).value, styleRes)
    sheet.write(31, 4, table.cell(31, 4).value, styleRes)
    sheet.write(31, 5, table.cell(31, 5).value, styleRes)
    sheet.write(31, 6, table.cell(31, 6).value, styleRes)


def get_cookie():
    #18853011144

    login_index_url = 'http://219.146.175.226:8406/webs/Login.aspx'
    response = down.get_html(login_index_url)
    if response:
        cookie_dic = response.cookies.get_dict()
        cookie_str = 'ASP.NET_SessionId='+cookie_dic['ASP.NET_SessionId']
        print(cookie_str)

        img_url = 'http://219.146.175.226:8406/webs/Ajax/ValidCodeImg.ashx'
        imgheaders = {
            'Accept': "image/webp,image/apng,image/*,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
            # 'Cookie': "ASP.NET_SessionId=4qllke34x3umw1mccodtmje0",
            'Host': "219.146.175.226:8406",
            'Pragma': "no-cache",
            'Referer': "http://219.146.175.226:8406/webs/Login.aspx",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            'cache-control': "no-cache",
            'Postman-Token': "eabc84d0-2ead-43b0-93d1-89ac770380fa"
        }
        imgheaders['Cookie'] = cookie_str
        img_response = down.get_html(img_url,headers=imgheaders)
        if img_response:
            with open('captcha.png','wb') as f:
                f.write(img_response.content)
            print('正在请求打码。。')
            rc = RClient('18853011144', 'cui885210.0', '118600', 'c82240332c0d42bb84c770c68dbc5686')
            with open('captcha.png', 'rb') as f:
                im = f.read()
            captcha_res = rc.rk_create(im, 7100)
            print(captcha_res)
            captcha_res = captcha_res['Result']

            loginUrl = 'http://219.146.175.226:8406/webs/Ajax/Login.ashx?Method=G3_Login&loginname=hb&password=1703&validcode='+captcha_res
            loginheaders = {
                'Accept': "text/plain, */*; q=0.01",
                'Accept-Encoding': "gzip, deflate",
                'Accept-Language': "zh-CN,zh;q=0.9",
                'Cache-Control': "no-cache",
                'Connection': "keep-alive",
                # 'Cookie': "ASP.NET_SessionId=4qllke34x3umw1mccodtmje0",
                'Host': "219.146.175.226:8406",
                'Pragma': "no-cache",
                'Referer': "http://219.146.175.226:8406/webs/Login.aspx",
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
                'X-Requested-With': "XMLHttpRequest",
                'cache-control': "no-cache",
            }
            loginheaders['Cookie']=cookie_str
            login_response = down.get_html(loginUrl,headers=loginheaders)
            if login_response:
                print(login_response.text)
                if login_response.text=='ok':
                    with open('cookie.txt','w') as f:
                        f.write(cookie_str)




def start():
    start_date = time.strftime('%Y-%m-%d+%H:00:00', time.localtime(time.time()-3600))
    end_date = time.strftime('%Y-%m-%d+%H:59:59', time.localtime(time.time()-3600))
    print(start_date)
    # start_date='2018-12-21+10:00:00'
    # end_date='2018-12-21+10:59:59'

    # save_res = '公司,时间点,二氧化硫实测浓度,二氧化硫折算浓度,二氧化硫排放量,氮氧化物实测浓度,氮氧化物折算浓度,氮氧化物排放量,颗粒物实测浓度,颗粒物折算浓度,颗粒物排放量,氧含量,烟气温度,废气排放量\n'
    # with open('结果.csv','w') as f:
    #     f.write(save_res)
    with open('cookie.txt') as f:
        cookie = f.read()
    headers['Cookie'] = cookie.strip()

    i = 0
    print('正在请求废气数据')
    for city in city_list:
        data = feiqi_body.format(subid=city['id'],subname=quote(city['city']),start=start_date,end=end_date)
        response = down.get_html(feiqi_url,method='post',headers=headers,data=data)
        if response:
            if response.text == '':
                print('登录失效，重新登录中..')
                get_cookie()
                return False
            json_obj = json.loads(response.text)
            if len(json_obj['rows'])>0:
                val_201 = json_obj['rows'][0]['val_201']
                cvt_201 = json_obj['rows'][0]['cvt_201']
                ex_201 = json_obj['rows'][0]['ex_201']

                val_203 = json_obj['rows'][0]['val_203']
                cvt_203 = json_obj['rows'][0]['cvt_203']
                ex_203 = json_obj['rows'][0]['ex_203']

                val_207 = json_obj['rows'][0]['val_207']
                cvt_207 = json_obj['rows'][0]['cvt_207']
                ex_207 = json_obj['rows'][0]['ex_207']

                val_209 = json_obj['rows'][0]['val_209']
                val_525 = json_obj['rows'][0]['val_525']
                val_210 = json_obj['rows'][0]['val_210']

                save_res = city['city']+','+str(start_date)+','+val_201+','+cvt_201+','+ex_201+','+val_203+','+cvt_203+','+ex_203+','+val_207+','+cvt_207+','+ex_207+','+val_209+','+val_525+','+val_210+'\n'
                print(save_res)

                sheet.write(4+i, 0, str(start_date).replace('+',' ').replace(':00:00',''), styleRes)
                sheet.write(4+i, 1, val_201, styleRes)
                sheet.write(4+i, 2, cvt_201, styleRes)
                sheet.write(4+i, 3, ex_201, styleRes)
                sheet.write(4+i, 4, val_203, styleRes)
                sheet.write(4+i, 5, cvt_203, styleRes)
                sheet.write(4+i, 6, ex_203, styleRes)

                sheet.write(8+i, 0, str(start_date).replace('+',' ').replace(':00:00',''), styleRes)
                sheet.write(8+i, 1, val_207, styleRes)
                sheet.write(8+i, 2, cvt_207, styleRes)
                sheet.write(8+i, 3, ex_207, styleRes)
                sheet.write(8+i, 4, val_209, styleRes)
                sheet.write(8+i, 5, val_525, styleRes)
                sheet.write(8+i, 6, val_210, styleRes)
                i+=9
                # with open('结果.csv','a') as f:
                #     f.write(save_res)
            else:
                save_old(city['city'],i)
                i += 9
        else:
            save_old(city['city'],i)
            i += 9

    #废水
    # with open('结果.csv', 'a') as f:
    #     f.write('\n公司,时间点,化学需氧量浓度,化学需氧量排放量,氨氮浓度,氨氮排放量,小时流量,PH\n')

    print('正在请求废水数据')
    data = feishui_body.format(start=start_date, end=end_date)
    response = down.get_html(feishui_url, method='post', headers=headers, data=data)
    if response:
        json_obj = json.loads(response.text)
        if len(json_obj['rows']) > 0:
            val_316 = json_obj['rows'][0]['val_316']
            flow_316 = json_obj['rows'][0]['flow_316']

            val_311 = json_obj['rows'][0]['val_311']
            flow_311 = json_obj['rows'][0]['flow_311']

            val_494 = json_obj['rows'][0]['val_494']
            PH = ''

            save_res = '东明石化集团（废水总排口）' + ',' + str(start_date) + ',' + val_316 + ',' + flow_316 + ',' + val_311 + ',' + flow_311+','+val_494+','+PH+'\n'
            print(save_res)
            # with open('结果.csv', 'a') as f:
            #     f.write(save_res)

            sheet.write(31, 0, str(start_date).replace('+',' ').replace(':00:00',''), styleRes)
            sheet.write(31, 1, val_316, styleRes)
            sheet.write(31, 2, flow_316, styleRes)
            sheet.write(31, 3, val_311, styleRes)
            sheet.write(31, 4, flow_311, styleRes)
            sheet.write(31, 5, val_494, styleRes)
        else:
            save_old_feishui('东明石化集团（废水总排口）')
    else:
        save_old_feishui('东明石化集团（废水总排口）')


    # 保存
    workbook.save('res.xls')
    return True

if __name__ == '__main__':
    #hb 1703
    down = download.Download()
    while True:
        # 创建一个workbook 设置编码
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建一个worksheet
        sheet = workbook.add_sheet('My Worksheet')

        data = xlrd.open_workbook('res.xls')
        table = data.sheets()[0]  # 通过索引顺序获取

        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.height = 24 * 12
        # font.colour_index = 0x4
        font.colour_index = xlwt.Style.colour_map['dark_green_ega']

        #列宽
        sheet.col(0).width = 256 * 20
        sheet.col(1).width = 256 * 15
        sheet.col(2).width = 256 * 15
        sheet.col(3).width = 256 * 15
        sheet.col(4).width = 256 * 15
        sheet.col(5).width = 256 * 15
        sheet.col(6).width = 256 * 15

        #边框
        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        borders.bottom_colour = 0x3A

        # colorstyle = "font:colour_index dark_green_ega;"
        # red_style = xlwt.easyxf(colorstyle)

        al = xlwt.Alignment()
        al.horz = 0x02  # 设置水平居中
        al.vert = 0x01  # 设置垂直居中
        style.alignment = al
        style.font = font
        style.borders = borders

        #数据样式
        styleRes = xlwt.XFStyle()
        fontRes = xlwt.Font()
        fontRes.height = 24 * 14
        fontRes.colour_index = xlwt.Style.colour_map['dark_green_ega']
        alRes = xlwt.Alignment()
        alRes.horz = 0x02  # 设置水平居中
        alRes.vert = 0x01  # 设置垂直居中
        styleRes.alignment = alRes
        styleRes.font = fontRes
        styleRes.borders = borders


        init_xls_file()

        try:
            start_res = start()
        except:
            start_res = False

        timeNum = 29
        if start_res:
            print('本时段数据获取完毕，30分钟后获取下一时段数据')
            while True:
                if (int(time.time()) % 60) == 0:
                    print('本时段数据获取完毕，'+str(timeNum)+'分钟后获取下一时段数据')
                    timeNum -=1
                    time.sleep(2)
                if timeNum==0:
                    break
            # time.sleep(60*20)
        else:
            print('当前出错，重新开始')
