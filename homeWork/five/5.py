#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random

num_list = [i for i in range(100)]
results = random.sample(num_list,10)
print(results)
max = results[0]
max_index = 0
min = results[0]
min_index = 0
for res in results:
    if res > max:
       max = res
       max_index = results.index(res)

    if res < min:
        min = res
        min_index = results.index(res)

t = results[max_index]
results[max_index] =  results[min_index]
results[min_index] = t

print(results)