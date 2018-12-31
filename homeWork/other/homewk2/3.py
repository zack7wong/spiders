#!/usr/bin/env python
# -*- coding:utf-8 -*-

a = int(input('请输入值：'))
x = a
while True:
    x1 = (x+a/x)/2
    x2 = x - x1
    if (abs(x2) < pow(10,-5)):
        break
    x = x1
print(x1)