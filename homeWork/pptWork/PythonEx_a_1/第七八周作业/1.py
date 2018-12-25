#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Employee():
    def __init__(self,name,pay):
        self.name = name
        self.pay = pay

    def get_last_name(self):
        if len(self.name)>=4:
            return self.name[:2]
        return self.name[0]

    def pay_raise(self,addpay):
        if addpay>0:
            self.pay += self.pay * addpay
        else:
            self.pay = self.pay - (self.pay * abs(addpay))
        return self.pay



if __name__=="__main__":
    ZhangSan=Employee('张三',8000)
    print(ZhangSan.get_last_name())
    ZhangSan.pay_raise(0.1)
    print(ZhangSan.pay)
    Dongfangbubai=Employee('东方不败',5000)
    print(Dongfangbubai.get_last_name())
    Dongfangbubai.pay_raise(-0.2)
    print(Dongfangbubai.pay)

