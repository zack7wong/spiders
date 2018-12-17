#!/usr/bin/env python
# -*- coding:utf-8 -*-

for i in range(2,1000):
     l1 = []
     for j in range(1,i):
         if i%j==0:
             l1.append(j)
     num = sum(l1)
     if num == i:
         print ("%d"%i)