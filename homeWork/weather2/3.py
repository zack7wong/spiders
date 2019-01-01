#!/usr/bin/env python
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
# res = 10 % 12+1
# print(res)

my_data_list = []
max_list = []
min_list = []
with open('塔城2017.csv') as f:
    results = f.readlines()
    for res in results:
        if res.split(',')[0][:7] == '2017-11':
            my_data = res.split(',')[0][8:]
            my_max = int(res.split(',')[1])
            my_min = int(res.split(',')[2])
            my_data_list.append(my_data)
            max_list.append(my_max)
            min_list.append(my_min)

print(max_list)
print(min_list)

plt.plot(my_data_list,max_list, 'r', linewidth=2)
plt.plot(my_data_list,min_list, 'g', linewidth=2)
plt.savefig('折线图.png')
plt.show()