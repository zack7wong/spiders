#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json

with open('city.csv', 'w') as ff:
    ff.write('城市,经度,纬度\n')

with open('weixin_results.csv') as f:
    results = f.readlines()
    for res in results:
        try:
            city = res.split(',')[3]
            if city !='':
                url = 'http://api.map.baidu.com/geocoder?address={address}&output=json&key=37492c0ee6f924cb5e934fa08c6b1676'
                response = requests.get(url.format(address=city))
                json_obj = json.loads(response.text)
                lng = json_obj['result']['location']['lng']
                lat = json_obj['result']['location']['lat']
                with open('city.csv','a') as ff:
                    ff.write(city+','+str(lng)+','+str(lat)+'\n')
        except:
            pass