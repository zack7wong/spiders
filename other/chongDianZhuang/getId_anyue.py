#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
with open('anyueJson.json') as f:
    res= f.read()

json_obj = json.loads(res)
print(json_obj)
for data in json_obj['data']['stations']:
    print(data)
    id = data['id']
    with open('anyue.txt','a') as f:
        f.write(id+'\n')