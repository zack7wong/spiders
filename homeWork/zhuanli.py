#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import pymysql
from lxml.etree import HTML

#mysql配置
MYSQL_HOST = 'localhost'
MYSQL_DB = 'zhuanli'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
MYSQL_CHARSET = 'utf8'

class MysqlClient(object):
    def __init__(self, host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB,charset=MYSQL_CHARSET):
        self.client = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        self.cursor = self.client.cursor()

    def save(self, sql):
        try:
            self.cursor.execute(sql)
            self.client.commit()
            print('存储成功')
        except:
            print('存储失败')
            self.client.rollback()

    def find_all(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except:
            print("Error: unable to fetch data")
            return None

    def find_one(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchone()
            return results
        except:
            print("Error: unable to find_one  data")
            return None

mysql_client = MysqlClient()
headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Cookie': "_ga=GA1.2.368630649.1544678356",
    'Host': "patft.uspto.gov",
    'Pragma': "no-cache",
    'Referer': "http://patft.uspto.gov/netahtml/PTO/search-adv.htm",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'cache-control': "no-cache",
    }

host_url = 'http://patft.uspto.gov'
start_url = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&Query=ISD%2F1%2F1%2F2013-%3E12%2F31%2F2013&d=PTXT'
response = requests.get(start_url,headers=headers)

html = HTML(response.text)
urls = html.xpath('//table//tr/td[4]/a/@href')
for url in urls:
    try:
        link = host_url+url
        detail_response = requests.get(link,headers=headers)
        detail_html = HTML(detail_response.text)

        title = detail_html.xpath('string(//font[@size="+1"])').replace(',',' ').replace('\n',' ').replace('\r',' ').strip()
        date = detail_html.xpath('string(//table//tr[2]/td[2])').replace(',',' ').replace('\n',' ').replace('\r',' ').strip()
        bianhao = detail_html.xpath('string(//table[2]//tr[1]/td[2])').replace(',',' ').replace('\n',' ').replace('\r',' ').strip()
        abstract = detail_html.xpath('string(//p)').replace(',',' ').replace('\n',' ').replace('\r',' ').strip()
        Inventors = detail_html.xpath('string(//table[3]//tr[1]/td[1])').replace(',',' ').replace('\n',' ').replace('\r',' ').strip()
        Applicant = detail_html.xpath('string(//table[3]//tr[2]/td[1])').replace(',',' ').replace('\n',' ').replace('\r',' ').strip()
        Assignee = detail_html.xpath('string(//table[3]//tr[3]/td[1])').replace(',',' ').replace('\n',' ').replace('\r',' ').strip()
        Family = detail_html.xpath('string(//table[3]//tr[4]/td[1])').replace(',',' ').replace('\n',' ').replace('\r',' ').strip()
        Appl = detail_html.xpath('string(//table[3]//tr[5]/td[1])').replace(',',' ').replace('\n',' ').replace('\r',' ').strip()
        Filed = detail_html.xpath('string(//table[3]//tr[6]/td[1])').replace(',',' ').replace('\n',' ').replace('\r',' ').strip()
        save_res = link+','+title+','+date+','+bianhao+','+abstract+','+Inventors+','+Applicant+','+Assignee+','+Family+','+Appl+','+Filed+'\n'
        print(save_res)

        sql = "insert into results(title,url,date,bianhao,abstract,Inventors,Applicant,Assignee,Family,Appl,Filed) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') "\
              %(title,link,date,bianhao,abstract,Inventors,Applicant,Assignee,Family,Appl,Filed)
        mysql_client.save(sql)

        with open('results.csv','a') as f:
            f.write(save_res)
    except:
        pass


