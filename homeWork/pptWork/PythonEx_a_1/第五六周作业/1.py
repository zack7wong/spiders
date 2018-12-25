#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time

def which_day(year, month, day):
    list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    whichday = 0
    if (year % 4) == 0 and (year % 100) != 0 or (year % 400) == 0:
        list[1] = 29
    for i in range(1, month):
        if month == 1:
            print('当前天数是：'+str(day))
        whichday = whichday + list[i - 1]
    whichday = whichday + day
    print('当前天数是：'+str(whichday))


if __name__ == "__main__":
    year = int(time.strftime('%Y',time.localtime()))
    month = int(time.strftime('%m',time.localtime()))
    day = int(time.strftime('%d',time.localtime()))
    which_day(year, month, day)