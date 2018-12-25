#!/usr/bin/env python
# -*- coding:utf-8 -*-

def get_huiwen(a):
    x = str(a)
    flag = True

    for i in range(int(len(x) / 2)):
        if x[i] != x[-i - 1]:
            flag = False
            break
    if flag:
        return True

for x in range(9,10):
    myx = x * 100000
    for y in range(0,10):
        for a in range(1000,9999):
            res = get_huiwen(a)
            myy = y * 10000
            wanwei = myy+a+1
            qianwanwei = myx + wanwei+1
            for_qianwanwei = int(str(qianwanwei)[1:-1])
            # print(wanwei)
            if res and get_huiwen(wanwei) and get_huiwen(for_qianwanwei):
                print('初始里程表的值是：'+qianwanwei-2)