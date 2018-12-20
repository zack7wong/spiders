#!/usr/bin/env python
# -*- coding:utf-8 -*-

def recur_fibo(n):
    if n <= 1:
        return n
    else:
        return (recur_fibo(n - 1) + recur_fibo(n - 2))

def get_num(num):
    for i in range(num):
        res = recur_fibo(i)
    return res

print('第十个斐波切数列的值为：')
print(get_num(10))