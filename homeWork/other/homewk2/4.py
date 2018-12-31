#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Air():
    def __init__(self,qifeishijian=None,mudidi=None,riqi=None,type=None,price=None,people=None,name=None):
        self.qifeishijian = qifeishijian
        self.mudidi = mudidi
        self.riqi = riqi
        self.type = type
        self.price = price
        self.people = people
        self.name = name

if __name__ == '__main__':
    myair = Air()
    myair.qifeishijian = '20190101'
    myair.mudidi = '北京'
    myair.riqi = '3天'
    myair.type = '经济舱'
    myair.price = '2100'
    myair.people = '1人'
    myair.name = '张三'