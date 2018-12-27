#!/usr/bin/env python
# -*- coding:utf-8 -*-

name_list = [{'key':'lebronjames-650','name':'詹姆斯原始数据.txt'},{'key':'kevindurant-1236','name':'杜兰特原始数据.txt'},{'key':'stephencurry-3311','name':'库里原始数据.txt'}]

for name_obj in name_list:
    filename = name_obj['name'].replace('原始','清洗后的').replace('txt','csv')
    with open(filename, 'w') as f:
        f.write('')

    with open(name_obj['name']) as f:
        results = f.readlines()

    year_list = eval(results[0].strip())
    changci_list = eval(results[1].strip())
    mingzhonglv_list = eval(results[2].strip())
    defen_list = eval(results[3].strip())
    pingjun_list = eval(results[4].strip())
    for i in range(0, 11):
        year_list[i] = int(year_list[i])
    for i in range(0,11):
        changci_list[i] = int(changci_list[i])
    for i in range(0,11):
        mingzhonglv_list[i] = float(mingzhonglv_list[i][:-1])
    for i in range(0,11):
        defen_list[i] = float(defen_list[i])
    for i in range(0,5):
        pingjun_list[i] = float(pingjun_list[i])

    print(changci_list)
    print(mingzhonglv_list)
    print(defen_list)
    print(pingjun_list)

    with open(filename,'a') as f:
        f.write(str(year_list).replace('[','').replace(']','')+'\n')
        f.write(str(changci_list).replace('[','').replace(']','')+'\n')
        f.write(str(mingzhonglv_list).replace('[','').replace(']','')+'\n')
        f.write(str(defen_list).replace('[','').replace(']','')+'\n')
        f.write(str(pingjun_list).replace('[','').replace(']','')+'\n')