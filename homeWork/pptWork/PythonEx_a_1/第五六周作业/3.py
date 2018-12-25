#!/usr/bin/env python
# -*- coding:utf-8 -*-

def fib(max):
    # 默认input是str类型
    max = int(max)
    n,a,b = 1,0,1
    # max：求几个斐波那契数
    while(n <= max):
        yield b
        # 这一步很关键   f(n) = f(n-1) + f(n-2)
        # 1 1 2 3 5 8
        a,b = b,a+b
        n += 1
    return 'done'

max = '10'
g = fib(max)
print('前10个斐波那契数列为：')
for n in g:
    print(n)