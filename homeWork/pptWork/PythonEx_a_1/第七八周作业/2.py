#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Manager():
    def __init__(self,name,pay,level='初级'):
        self.name = name
        self.pay = pay
        self.level = level

    def get_last_name(self):
        if len(self.name)>=4:
            return self.name[:2]
        return self.name[0]

    def pay_raise(self,addpay):
        if addpay>0:
            if self.level == '初级':
                self.pay += self.pay * addpay + 500
            else:
                self.pay += self.pay * addpay + 1000
        else:
            self.pay = self.pay - (self.pay * abs(addpay))
        return self.pay



if __name__=="__main__":
    LiSi=Manager('李四',12000,"初级")
    print(LiSi.get_last_name())
    LiSi.pay_raise(0.3)
    print(round(LiSi.pay))
    WangWu=Manager('王五',15000,"高级")
    print(WangWu.get_last_name())
    WangWu.pay_raise(0.2)
    print(round(WangWu.pay))


