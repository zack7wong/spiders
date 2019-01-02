#!/usr/bin/env python
# -*- coding:utf-8 -*-

import TencentYoutuyun
import matplotlib.pyplot as plt

item_list = []
with open('results.csv') as f:
    results = f.readlines()
    for res in results:
        img_url = res.split(',')[6]
        item_list.append(img_url)
# print(item_list)


appid = '10163570'
secret_id = 'AKIDqUu4zefMr65pKaJNyJRKyPeeT6TaQ9Zj'
secret_key = '61kGXYLvFKDtKWTBesrgV6RXO0MTN5Yl'
userid = '123'

end_point = TencentYoutuyun.conf.API_YOUTU_END_POINT

youtu = TencentYoutuyun.YouTu(appid, secret_id, secret_key, userid, end_point)

unkonw = 0
man = 0
woman = 0
for item in item_list:
    try:
        print(item)
        ret = youtu.DetectFace(image_path=item,mode = 0,data_type =1)
        print (ret)
        if len(ret["face"]) > 0:
            for j in ret["face"]:
                if j["gender"] > 50:
                    print("性别:男")
                    man+=1
                else:
                    print("性别:女")
                    woman+=1
        else:
            unkonw+=1
    except:
        continue

print(unkonw)
print(man)
print(woman)

labels = ['man', 'woman','other']
X = [man, woman,unkonw]
fig = plt.figure()

plt.pie(X, labels=labels, autopct='%1.2f%%')  # 画饼图

plt.savefig("头像性别分析.jpg")
plt.show()