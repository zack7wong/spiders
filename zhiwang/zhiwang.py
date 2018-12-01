#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     zhiwang
   Description :
   Author :        hayden_huang
   Date：          2018/12/1 17:58
-------------------------------------------------
"""
from urllib.parse import quote
import requests
from lxml.etree import HTML
headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Length': "7461",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cookie': "naviCollopseNodes=; navisel=A%2CB%2CC%2CD%2CE%2CF%2CG%2CH%2CI%2CJ; orderfield=; filtervalue1=; filtervalue=; ASP.NET_SessionId=yorw3rhuoxj5gjvdhjs4vfmp; RememberUserSelect=NOW; SID=016103; UM_distinctid=1676478be0c2f5-0526c1a052a80a-35627600-1fa400-1676478be1457; CNZZDATA1254645480=1779899039-1543578893-%7C1543653035; CurTop10KeyWord=%2c%u6b23%u6b23%u5411%u8363",
    'Host': "gongjushu20.cnki.net",
    'Origin': "http://gongjushu20.cnki.net",
    'Pragma': "no-cache",
    'Referer': "http://gongjushu20.cnki.net/refbook/Brief.aspx?ID=&SearchFor=&SearchType=SingleDBAdvance&classtype=&systemno=&NaviDatabaseName=&NaviField=",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "f1561fd2-f9cd-4add-9b75-8650d8e54fc6"
}

URL = 'http://gongjushu20.cnki.net/refbook/Brief.aspx?ID=&SearchFor=&SearchType=SingleDBAdvance&classtype=&systemno=&NaviDatabaseName=&NaviField='


def get_chengyu():
    chengyu_list = []
    with open('chengyu.txt') as f:
        results = f.readlines()
        for res in results:
            try:
                word = res.split(':')[0].strip()
                account_obj = {
                    'word': word,
                }
                chengyu_list.append(account_obj)
            except:
                print('该行文本格式有误')
                print(res)
                with open('failed.txt', 'a') as ff:
                    ff.write(res)

    return chengyu_list


def get_res(type):
    if type=='all':
        chengyu_list = get_chengyu()
    else:
        chengyu_list = [{'word':type}]

    for chengyu in chengyu_list:
        try:
            print('当前查询成语:'+chengyu['word'])
            start_url = URL
            chengyu_str = quote(chengyu['word'])
            body = '__VIEWSTATE=%2FwEPDwUKMTcxNzkyODMwNw9kFgICAQ9kFgQCAQ9kFgJmD2QWAgIBD2QWAmYPDxYCHgtOYXZpZ2F0ZVVybAUzaHR0cDovL215LmNua2kubmV0L2VsaWJyZWdpc3Rlci9Db21tb25SZWdpc3Rlci5hc3B4ZGQCBQ9kFgICAQ9kFgJmD2QWAgIBD2QWAgIBDxYCHgRUZXh0BfIHPHRhYmxlIGJvcmRlcj0wIGNlbGxwYWRkaW5nPSIwIiBjZWxsc3BhY2luZz0iMCIgPg0KICAgICAgICAgIDx0ciB2YWxpZ249ImJvdHRvbSIgc3R5bGU9J2hlaWdodDoyN3B4Oyc%2BDQogICAgICAgICAgICA8dGQgYmFja2dyb3VuZD0iSW1hZ2VzL2Fkdl9yaWdodF90YWJidXQxX2FjdGl2ZS5naWYiIHN0eWxlPSd3aWR0aDo1NHB4O3RleHQtYWxpZ246Y2VudGVyOyc%2BDQogICAgICAgICAgICAgICAgPGEgY2xhc3M9J2FkdlJpZ2h0VGFiQnV0QWN0aXZlJyBocmVmPSdBZHZTZWFyY2guYXNweD9JRD1DUkZEJmFtcDtTZWFyY2hGb3I9MSZhbXA7U2VhcmNoVHlwZT1TaW5nbGVEQkFkdmFuY2UnPuivjeadoTwvYT4NCiAgICAgICAgICAgIDwvdGQ%2BICAgICAgICAgICAgDQogICAgICAgICAgICA8dGQgd2lkdGg9IjQiPiZuYnNwOzwvdGQ%2BICAgICAgICAgICAgDQogICAgICAgICAgICA8dGQgYmFja2dyb3VuZD0iSW1hZ2VzL2Fkdl9yaWdodF90YWJidXQyX2RlZmF1bHQuZ2lmIiBzdHlsZT0nd2lkdGg6NjZweDt0ZXh0LWFsaWduOmNlbnRlcjsnPg0KICAgICAgICAgICAgICAgIDxhIGhyZWY9J0FkdlNlYXJjaC5hc3B4P0lEPUNSRkRCQVNFSU5GTyZhbXA7U2VhcmNoRm9yPTImYW1wO1NlYXJjaFR5cGU9U2luZ2xlREJBZHZhbmNlJz7lt6XlhbfkuaY8L2E%2BDQogICAgICAgICAgICA8L3RkPiAgICAgICAgICAgIA0KICAgICAgICAgICAgPHRkIHdpZHRoPSI0Ij4mbmJzcDs8L3RkPg0KICAgICAgICAgICAgPHRkIGJhY2tncm91bmQ9IkltYWdlcy9hZHZfcmlnaHRfdGFiYnV0MV9kZWZhdWx0LmdpZiIgc3R5bGU9J3dpZHRoOjU0cHg7dGV4dC1hbGlnbjpjZW50ZXI7Jz4NCiAgICAgICAgICAgICAgICA8YSBocmVmPSdBZHZTZWFyY2guYXNweD9JRD1DUkZET1RIRVJJTkZPJmFtcDtTZWFyY2hGb3I9MyZhbXA7U2VhcmNoVHlwZT1TaW5nbGVEQkFkdmFuY2UnPui%2BheaWhzwvYT4NCiAgICAgICAgICAgIDwvdGQ%2BICAgICAgICAgICAgDQogICAgICAgICAgPC90cj4NCiAgICAgICAgPC90YWJsZT5kGAEFG1RvcEhlYWRlclJlc3VsdDEkTXVsdGlWaWV3MQ8PZAIBZMP1lSAFG1fJhIEq1KXPpHKbaVtKbYw81%2B36M08cVDNE&username=&password=&NaviField=%E4%B8%93%E9%A2%98%E5%AD%90%E6%A0%8F%E7%9B%AE%E4%BB%A3%E7%A0%81&selectbox=A&selectbox=B&selectbox=C&selectbox=D&selectbox=E&selectbox=F&selectbox=G&selectbox=H&selectbox=I&selectbox=J&searchAttachCondition=&SearchQueryID=22&SearchFieldRelationDirectory=%E6%9D%A1%E7%9B%AE%E5%90%8D%E7%A7%B0%2F%5B%5D%2C%E6%9D%A1%E7%9B%AE%E9%87%8A%E6%96%87%2F%5B%5D%2C%E6%9D%A1%E7%9B%AE%E7%9A%84%E8%8B%B1%E6%96%87%2F%5B%5D%2C%E6%9D%A1%E7%9B%AE%E4%BD%9C%E8%80%85%2F%5BSYS_Author_Relevant&updateTempDB=0&bCurYearTempDB=1&fieldtips=%E7%AF%87%E5%90%8D%2F%5B%E5%9C%A8%E6%96%87%E7%8C%AE%E6%A0%87%E9%A2%98%E4%B8%AD%E6%A3%80%E7%B4%A2%E3%80%82%E5%AF%B9%E8%AF%A5%E6%A3%80%E7%B4%A2%E9%A1%B9%E7%9A%84%E6%A3%80%E7%B4%A2%E6%98%AF%E6%8C%89%E8%AF%8D%E8%BF%9B%E8%A1%8C%E7%9A%84%EF%BC%8C%E8%AF%B7%E5%B0%BD%E5%8F%AF%E8%83%BD%E8%BE%93%E5%85%A5%E5%AE%8C%E6%95%B4%E7%9A%84%E8%AF%8D%EF%BC%8C%E4%BB%A5%E9%81%BF%E5%85%8D%E6%BC%8F%E6%A3%80%E3%80%82%5D%2C%E5%85%B3%E9%94%AE%E8%AF%8D%2F%5B%E6%A3%80%E7%B4%A2%E6%96%87%E7%8C%AE%E7%9A%84%E5%85%B3%E9%94%AE%E8%AF%8D%E4%B8%AD%E6%BB%A1%E8%B6%B3%E6%A3%80%E7%B4%A2%E6%9D%A1%E4%BB%B6%E7%9A%84%E6%96%87%E7%8C%AE%E3%80%82%E5%AF%B9%E8%AF%A5%E6%A3%80%E7%B4%A2%E9%A1%B9%E7%9A%84%E6%A3%80%E7%B4%A2%E6%98%AF%E6%8C%89%E8%AF%8D%E8%BF%9B%E8%A1%8C%E7%9A%84%EF%BC%8C%E8%AF%B7%E5%B0%BD%E5%8F%AF%E8%83%BD%E8%BE%93%E5%85%A5%E5%AE%8C%E6%95%B4%E7%9A%84%E8%AF%8D%EF%BC%8C%E4%BB%A5%E9%81%BF%E5%85%8D%E6%BC%8F%E6%A3%80%E3%80%82%5D%2C%E7%AC%AC%E4%B8%80%E8%B4%A3%E4%BB%BB%E4%BA%BA%2F%5B%E8%AF%B7%E9%80%89%E6%8B%A9%E6%A3%80%E7%B4%A2%E9%A1%B9%E5%B9%B6%E6%8C%87%E5%AE%9A%E7%9B%B8%E5%BA%94%E7%9A%84%E6%A3%80%E7%B4%A2%E8%AF%8D%EF%BC%8C%E9%80%89%E6%8B%A9%E6%8E%92%E5%BA%8F%E6%96%B9%E5%BC%8F%E3%80%81%E5%8C%B9%E9%85%8D%E6%A8%A1%E5%BC%8F%E3%80%81%E6%96%87%E7%8C%AE%E6%97%B6%E9%97%B4%E7%AD%89%E9%99%90%E5%AE%9A%E6%9D%A1%E4%BB%B6%EF%BC%8C%E7%84%B6%E5%90%8E%E7%82%B9%E5%87%BB%E2%80%9C%E6%A3%80%E7%B4%A2%E2%80%9D%E3%80%82%5D%2C%E4%BD%9C%E8%80%85%2F%5B%E5%8F%AF%E8%BE%93%E5%85%A5%E4%BD%9C%E8%80%85%E5%AE%8C%E6%95%B4%E5%A7%93%E5%90%8D%EF%BC%8C%E6%88%96%E5%8F%AA%E8%BE%93%E5%85%A5%E8%BF%9E%E7%BB%AD%E7%9A%84%E4%B8%80%E9%83%A8%E5%88%86%E3%80%82%5D%2C%E6%9C%BA%E6%9E%84%2F%5B%E5%8F%AF%E8%BE%93%E5%85%A5%E5%AE%8C%E6%95%B4%E7%9A%84%E6%9C%BA%E6%9E%84%E5%90%8D%E7%A7%B0%EF%BC%8C%E6%88%96%E5%8F%AA%E8%BE%93%E5%85%A5%E8%BF%9E%E7%BB%AD%E7%9A%84%E4%B8%80%E9%83%A8%E5%88%86%E3%80%82%5D%2C%E4%B8%AD%E6%96%87%E6%91%98%E8%A6%81%2F%5B%E5%AF%B9%E8%AF%A5%E6%A3%80%E7%B4%A2%E9%A1%B9%E7%9A%84%E6%A3%80%E7%B4%A2%E6%98%AF%E6%8C%89%E8%AF%8D%E8%BF%9B%E8%A1%8C%E7%9A%84%EF%BC%8C%E8%AF%B7%E5%B0%BD%E5%8F%AF%E8%83%BD%E8%BE%93%E5%85%A5%E5%AE%8C%E6%95%B4%E7%9A%84%E8%AF%8D%EF%BC%8C%E4%BB%A5%E9%81%BF%E5%85%8D%E6%BC%8F%E6%A3%80%E3%80%82%5D%2C%E5%BC%95%E6%96%87%2F%5B%E8%AF%B7%E9%80%89%E6%8B%A9%E6%A3%80%E7%B4%A2%E9%A1%B9%E5%B9%B6%E6%8C%87%E5%AE%9A%E7%9B%B8%E5%BA%94%E7%9A%84%E6%A3%80%E7%B4%A2%E8%AF%8D%EF%BC%8C%E9%80%89%E6%8B%A9%E6%8E%92%E5%BA%8F%E6%96%B9%E5%BC%8F%E3%80%81%E5%8C%B9%E9%85%8D%E6%A8%A1%E5%BC%8F%E3%80%81%E6%96%87%E7%8C%AE%E6%97%B6%E9%97%B4%E7%AD%89%E9%99%90%E5%AE%9A%E6%9D%A1%E4%BB%B6%EF%BC%8C%E7%84%B6%E5%90%8E%E7%82%B9%E5%87%BB%E2%80%9C%E6%A3%80%E7%B4%A2%E2%80%9D%E3%80%82%5D%2C%E5%85%A8%E6%96%87%2F%E8%AF%B7%E9%80%89%E6%8B%A9%E6%A3%80%E7%B4%A2%E9%A1%B9%E5%B9%B6%E6%8C%87%E5%AE%9A%E7%9B%B8%E5%BA%94%E7%9A%84%E6%A3%80%E7%B4%A2%E8%AF%8D%EF%BC%8C%E9%80%89%E6%8B%A9%E6%8E%92%E5%BA%8F%E6%96%B9%E5%BC%8F%E3%80%81%E5%8C%B9%E9%85%8D%E6%A8%A1%E5%BC%8F%E3%80%81%E6%96%87%E7%8C%AE%E6%97%B6%E9%97%B4%E7%AD%89%E9%99%90%E5%AE%9A%E6%9D%A1%E4%BB%B6%EF%BC%8C%E7%84%B6%E5%90%8E%E7%82%B9%E5%87%BB%E2%80%9C%E6%A3%80%E7%B4%A2%E2%80%9D%E3%80%82%5D%2C%E5%9F%BA%E9%87%91%2F%5B%E6%A3%80%E7%B4%A2%E5%8F%97%E6%BB%A1%E8%B6%B3%E6%9D%A1%E4%BB%B6%E7%9A%84%E5%9F%BA%E9%87%91%E8%B5%84%E5%8A%A9%E7%9A%84%E6%96%87%E7%8C%AE%E3%80%82%5D%2C%E4%B8%AD%E6%96%87%E5%88%8A%E5%90%8D%2F%5B%E8%AF%B7%E8%BE%93%E5%85%A5%E9%83%A8%E5%88%86%E6%88%96%E5%85%A8%E9%83%A8%E5%88%8A%E5%90%8D%E3%80%82%5D%2CISSN%2F%5B%E8%AF%B7%E8%BE%93%E5%85%A5%E5%AE%8C%E6%95%B4%E7%9A%84ISSN%E5%8F%B7%E3%80%82%5D%2C%E5%B9%B4%2F%5B%E8%BE%93%E5%85%A5%E5%9B%9B%E4%BD%8D%E6%95%B0%E5%AD%97%E7%9A%84%E5%B9%B4%E4%BB%BD%E3%80%82%5D%2C%E6%9C%9F%2F%5B%E8%BE%93%E5%85%A5%E6%9C%9F%E5%88%8A%E7%9A%84%E6%9C%9F%E5%8F%B7%EF%BC%8C%E5%A6%82%E6%9E%9C%E4%B8%8D%E8%B6%B3%E4%B8%A4%E4%BD%8D%E6%95%B0%E5%AD%97%EF%BC%8C%E8%AF%B7%E5%9C%A8%E5%89%8D%E9%9D%A2%E8%A1%A5%E2%80%9C0%E2%80%9D%EF%BC%8C%E5%A6%82%E2%80%9C08%E2%80%9D%E3%80%82%5D%2C%E4%B8%BB%E9%A2%98%2F%5B%E4%B8%BB%E9%A2%98%E5%8C%85%E6%8B%AC%E7%AF%87%E5%90%8D%E3%80%81%E5%85%B3%E9%94%AE%E8%AF%8D%E3%80%81%E4%B8%AD%E6%96%87%E6%91%98%E8%A6%81%E3%80%82%E5%8F%AF%E6%A3%80%E7%B4%A2%E5%87%BA%E8%BF%99%E4%B8%89%E9%A1%B9%E4%B8%AD%E4%BB%BB%E4%B8%80%E9%A1%B9%E6%88%96%E5%A4%9A%E9%A1%B9%E6%BB%A1%E8%B6%B3%E6%8C%87%E5%AE%9A%E6%A3%80%E7%B4%A2%E6%9D%A1%E4%BB%B6%E7%9A%84%E6%96%87%E7%8C%AE%E3%80%82%E5%AF%B9%E4%B8%BB%E9%A2%98%E6%98%AF%E6%8C%89%E8%AF%8D%E6%A3%80%E7%B4%A2%E7%9A%84%EF%BC%8C%E8%AF%B7%E5%B0%BD%E5%8F%AF%E8%83%BD%E8%BE%93%E5%85%A5%E5%AE%8C%E6%95%B4%E7%9A%84%E8%AF%8D%EF%BC%8C%E4%BB%A5%E9%81%BF%E5%85%8D%E6%BC%8F%E6%A3%80%E3%80%82%5D&advancedfield1=%E8%AF%8D%E6%9D%A1&advancedvalue1={chengyu}&logical2=and&advancedfield2=%E8%AF%8D%E7%9B%AE&advancedvalue2=&logical3=and&advancedfield3=%E5%B7%A5%E5%85%B7%E4%B9%A6%E5%90%8D%E7%A7%B0&advancedvalue3=&searchFlag=1&imageField.x=18&imageField.y=6&RealYearStart=&RealYearEnd=&searchmatch=1&order=RELEVANT&RecordsPerPage=20&extension=1&hdnUSPSubDB=%E5%AA%92%E4%BD%93%E7%B1%BB%E5%9E%8B%2C%2B1%2B2%2B%2C2%2C2&TableType=PY&display=chinese&encode=gb&TablePrefix=CRFD&View=CRFD&yearFieldName=%E5%86%85%E5%AE%B9%E7%89%88%E6%9D%83%E6%97%A5%E6%9C%9F&userright=&VarNum=3&filtervalue1=*&filterfield=*&lastpage=255&RecordsPerPage2=10&systemno=%2F&classtype=%2F&QueryID=22&turnpage=&curpage=1&curpage1=1'\
                .format(chengyu=chengyu_str)
            response = requests.post(start_url,headers=headers,data=body,timeout=10)
            html = HTML(response.text)
            results = html.xpath('//div[@class="advbrieflist"]/div[@class="briefresult"]/dl/dd[1]/p[1]/text()[1]')
            origins = html.xpath('//div[@class="advbrieflist"]/div[@class="briefresult"]/dl/dd[1]/p/span/a/text()')
            for res,origin in zip(results,origins):
                save_res = chengyu['word']+','+ origin +','+res.replace('\n','').replace('\t','').replace('\r','').replace(',','，').strip()+'\n'
                print(save_res)
                with open('results.csv','a') as f:
                    f.write(save_res)
        except:
            print('未知错误')
            with open('failed.csv', 'a') as f:
                f.write(chengyu['word']+'\n')


if __name__ == '__main__':
    while True:
        type = input('请输入要查询的成语(如需批量请输入 all):')
        if type == 'all':
            get_res('all')
        else:
            get_res(type)


