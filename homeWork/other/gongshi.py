#!/usr/bin/env python
# -*- coding:utf-8 -*-


import numpy as np
import math

#被积函数
def f(x):
    return x*x - 3*x + 2

def sanjiao(x):
    return math.sin(x)

def zhishu(x):
    return  math.exp(x)

def tixing(f,a,b,n=100):
    f = np.vectorize(f) #对函数进行矢量转换
    h = float(b - a)/n
    arr = f(np.linspace(a,b,n+1))  #linspace生成等-1 到 2 的间隔的数列，共101份
    res = (h/2.)*(2*arr.sum() - arr[0] - arr[-1])  #第一个和最后一个不用乘以2，要减去
    return res


def simpson(f, a, b, n):
    h = (b - a) / (2 * n)  #n是分成几份，a是积分下线，b是积分上线
    s1 = 0
    s2 = 0
    for k in range(1,n+1):
        x = a + h * (2 * k -1)
        s1 = s1 + f(x)      #计算 y1+y3+...+y2n-1的值
    for k in range(1,n):
        x = a + h * 2 * k
        s2 = s2 + f(x)     #计算 y2+y4+...+y2n-2的值
    res = h * (f(a) + f(b) + 4 * s1 + 2 * s2) / 3
    return res




if __name__ == '__main__':
    while True:
        use_fun = input('请输入要实现的公式[1]梯形公式，[2]辛普森公式：')
        if use_fun =='1':
            type = input('请输入积分函数【1】多项式函数(x*x-3*x+2)，【2】三角函数(sin(x))，【3】指数函数(x^a)：')
            a = int(input('请输入积分下限：'))
            b = int(input('请输入积分上限：'))
            if type=='1':
                f = f
            elif type =='2':
                f = sanjiao
            elif type == '3':
                f = zhishu
            res = tixing(f, a, b)
            print('结果是：' + str(res))
        elif use_fun == '2':
            type = input('请输入积分函数【1】多项式函数(x*x-3*x+2)，【2】三角函数(sin(x))，【3】指数函数(x^a)：')
            a = int(input('请输入积分下限：'))
            b = int(input('请输入积分上限：'))
            n = int(input('请输入切割份数：'))
            if type == '1':
                f = f
            elif type == '2':
                f = sanjiao
            elif type == '3':
                f = zhishu

            res = simpson(f, a, b, n)
            print('结果是：'+str(res))



