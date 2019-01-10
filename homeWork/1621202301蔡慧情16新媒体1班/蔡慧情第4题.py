#1621202301 蔡慧情 16新媒体1班  第4题 2018年12月18日 15:18

import random

item_list = []
while True:
    res = random.randint(10, 50)
    item_list.append(res)
    if len(item_list) == 100:
        break

num = 1
for i in item_list:
    print(str(i)+'\t',end='')
    if num%10==0:
        print('\n')
    num+=1

a_list = []
b_list = []
for res in item_list:
    if res in a_list:
        for b in b_list:
            if res in b.keys():
                b[res]+=1
    else:
        a_list.append(res)
        obj = {
            res:1
        }
        b_list.append(obj)

for res in b_list:
    listRes = list(res.keys())
    print('数字'+str(listRes[0])+'出现次数为：'+str(res[listRes[0]]))
