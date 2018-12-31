#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Huanzhe():
    def __init__(self,id=None,name=None,sex=None,age=None,address=None,phone=None,birthday=None,shengao=None,tizhong=None):
#         ID号、姓名、性别、年龄、地址、电话号码、出生日期、身高和体重
        self.id=id
        self.name=name
        self.sex=sex
        self.age=age
        self.address=address
        self.phone=phone
        self.birthday=birthday
        self.shengao=shengao
        self.tizhong=tizhong

    def get(self,wordtype):
        returnRes = ''
        if wordtype == 'id':
            returnRes = self.id
        elif wordtype == 'name':
            returnRes = self.name
        elif wordtype == 'sex':
            returnRes = self.sex
        elif wordtype == 'age':
            returnRes = self.age
        elif wordtype == 'address':
            returnRes = self.address
        elif wordtype == 'phone':
            returnRes = self.phone
        elif wordtype == 'birthday':
            returnRes = self.birthday
        elif wordtype == 'tizhong':
            returnRes = self.tizhong
        return returnRes

    def set(self,wordtype,value):
        if wordtype == 'id':
            self.id = value
        elif wordtype == 'name':
            self.name = value
        elif wordtype == 'sex':
            self.sex = value
        elif wordtype == 'age':
            self.age = value
        elif wordtype == 'address':
            self.address = value
        elif wordtype == 'phone':
            self.phone = value
        elif wordtype == 'birthday':
            self.birthday = value
        elif wordtype == 'tizhong':
            self.tizhong = value


class Yisheng():
    def __init__(self,name=None,id=None,zhicheng=None,zhuanye=None,phone=None,time=None,address=None):
        # 姓名、ID、职称(DO或MD)、专业(外科医生、儿科医生等)、电话号码、办公时间、办公地点
        self.name = name
        self.id = id
        self.zhicheng = zhicheng
        self.zhuanye = zhuanye
        self.phone = phone
        self.time = time
        self.address = address

    def get(self,wordtype):
        returnRes = ''
        if wordtype == 'name':
            returnRes = self.name
        elif wordtype == 'id':
            returnRes = self.id
        elif wordtype == 'zhicheng':
            returnRes = self.zhicheng
        elif wordtype == 'zhuanye':
            returnRes = self.zhuanye
        elif wordtype == 'phone':
            returnRes = self.phone
        elif wordtype == 'time':
            returnRes = self.time
        elif wordtype == 'address':
            returnRes = self.address
        return returnRes

    def set(self,wordtype,value):
        if wordtype == 'id':
            self.id = value
        elif wordtype == 'name':
            self.name = value
        elif wordtype == 'zhicheng':
            self.zhicheng = value
        elif wordtype == 'zhuanye':
            self.zhuanye = value
        elif wordtype == 'phone':
            self.phone = value
        elif wordtype == 'time':
            self.time = value
        elif wordtype == 'address':
            self.address = value

class Bingli():
    def __init__(self,date=None,Yid=None,Hid=None,wenti=None,chufang=None,feiyong=None,baogao=None):
        # 检查的日期、医生的ID、患者的ID、患者健康问题列表、处方药品清单、检查费用、最后报告
        self.date = date
        self.Yid = Yid
        self.Hid = Hid
        self.wenti = wenti
        self.chufang = chufang
        self.feiyong = feiyong
        self.baogao = baogao

    def get(self,wordtype):
        returnRes = ''
        if wordtype == 'date':
            returnRes = self.date
        elif wordtype == 'Yid':
            returnRes = self.Yid
        elif wordtype == 'Hid':
            returnRes = self.Hid
        elif wordtype == 'wenti':
            returnRes = self.wenti
        elif wordtype == 'chufang':
            returnRes = self.chufang
        elif wordtype == 'feiyong':
            returnRes = self.feiyong
        elif wordtype == 'baogao':
            returnRes = self.baogao
        return returnRes

    def set(self,wordtype,value):
        if wordtype == 'date':
            self.date = value
        elif wordtype == 'Yid':
            self.Yid = value
        elif wordtype == 'Hid':
            self.Hid = value
        elif wordtype == 'wenti':
            self.wenti = value
        elif wordtype == 'chufang':
            self.chufang = value
        elif wordtype == 'feiyong':
            self.feiyong = value
        elif wordtype == 'baogao':
            self.baogao = value

if __name__ == '__main__':
    huanzhe = Huanzhe()
    huanzhe.name = '张三'
    print(huanzhe.get('name'))

    yisheng = Yisheng()
    yisheng.name = '李医生'
    print(yisheng.get('name'))

    bingli = Bingli()
    bingli.date = '20190101'
    print(bingli.get('date'))