#!/usr/bin/env python
# -*- coding:utf-8 -*-

x = int(input('请输入值：'))
ex = 0
p = 1
i = 0
while p > pow(10,-6):
    ex +=p
    i = i+1
    p = p*x/i
print('e的'+str(x)+'次方根为：'+str(ex))