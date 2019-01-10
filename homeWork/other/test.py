# -*- coding: utf-8 -*-

import time
import TencentYoutuyun

# AppID: 10163570
# SecretID: AKIDqUu4zefMr65pKaJNyJRKyPeeT6TaQ9Zj
# SecretKey: 61kGXYLvFKDtKWTBesrgV6RXO0MTN5Yl
# 应用平台: Web
# 应用类型: 娱乐
# 接入产品类型: FaceIn人脸核身
# 应用简介:
# tsesst

# pip install requests
# please get these values from http://open.youtu.qq.com
appid = '10163570'
secret_id = 'AKIDqUu4zefMr65pKaJNyJRKyPeeT6TaQ9Zj'
secret_key = '61kGXYLvFKDtKWTBesrgV6RXO0MTN5Yl'
userid = '123'

#choose a end_point
#end_point = TencentYoutuyun.conf.API_TENCENTYUN_END_POINT
#end_point = TencentYoutuyun.conf.API_YOUTU_VIP_END_POINT
end_point = TencentYoutuyun.conf.API_YOUTU_END_POINT

youtu = TencentYoutuyun.YouTu(appid, secret_id, secret_key, userid, end_point)

#两张人脸比对，返回相似度
#session_id = id
#ret = youtu.FaceCompare(img1,img2)
#print (ret)

#新建个体ID
# ret = youtu.NewPerson(person_id="person1",image_path="zyx.jpg",group_ids="Students", person_name= 'zyx', tag='', data_type = 0)
# print(ret)

ret = youtu.DetectFace(image_path="https://tvax1.sinaimg.cn/crop.0.0.1242.1242.180/9fd8f287ly8fwkveisgeaj20yi0yidkh.jpg",mode = 0,data_type =1)
print (ret)
#
for j in ret["face"]:
    if j["gender"] > 50:
        print("性别:男")
    else:
        print("性别:女")

    if j["expression"] >90:
        print("你在大笑")
    elif 50 <j["expression"] < 90:
        print("你在微笑")
    else:
        print("我没感觉你笑")
    if j["glass"]:
        print("你戴眼镜了")
    print("你的颜值:",j["beauty"])
    print("你的年龄:",j["age"])