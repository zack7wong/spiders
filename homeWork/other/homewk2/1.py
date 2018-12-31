#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random

def gys(a,b):
    if b == 0:
        return '0没有最大公约数'
    a, b = (a, b) if a >=b else (b, a)
    if a%b == 0:
        return b
    else :
        return gys(b,a%b)


# 定义函数
def gbs(x, y):
    if x > y:
        greater = x
    else:
        greater = y

    while (True):
        if ((greater % x == 0) and (greater % y == 0)):
            lcm = greater
            break
        greater += 1

    return lcm

num1 = random.randint(0,100)
num2 = random.randint(0,100)
res1 = gys(num1,num2)
res2 = gbs(num1,num2)

print('随机数1：'+str(num1))
print('随机数2：'+str(num2))

print('最大公约数是：'+str(res1))
print('最小公倍数是：'+str(res2))