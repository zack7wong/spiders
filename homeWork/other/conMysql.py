#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymysql

host = 'localhost'
username = 'root'
password = 'root'
mydb = 'test'
db = pymysql.connect(host,username ,password, mydb)
cursor = db.cursor()

sql = "SELECT * FROM grade"
cursor.execute(sql)
results = cursor.fetchall()

grade_dic = [{"key":[0,59],"value":"不及格"},{"key":[60,69],"value":"及格"},{"key":[70,84],"value":"良好"},{"key":[85,100],"value":"优秀"}]

all_item = []

for row in results:
    name = row[0]
    liuchengtu = float(row[1])
    uml = float(row[2])
    php = float(row[3])

    avg = float("%.2f" % ((liuchengtu+uml+php)/3))
    for item in grade_dic:
        if avg >= item['key'][0] and avg <=item['key'][1]:
            grade = item['value']
            break
    print(name,avg,grade)

    obj ={
        'name':name,
        'avg':avg,
        'grade':grade,
    }
    all_item.append(obj)

print(all_item)
all_item = sorted(all_item,key=lambda x:x['avg'],reverse=True)
print(all_item)

num = 0
temp = ''
for item in all_item:
    if item['avg'] != temp:
        num +=1
        temp = item['avg']
    sql = "update grade set 平均分='%s',排名='%s',等级='%s' where 姓名='%s'"%(item['avg'],num,item['grade'],item['name'])
    print(sql)
    cursor.execute(sql)

db.close()