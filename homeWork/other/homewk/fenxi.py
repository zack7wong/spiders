#!/usr/bin/env python
# -*- coding:utf-8 -*-

item_list = []
with open('results.csv') as f:
    results = f.readlines()
    for res in results[1:]:
        price = float(res.split(',')[2].replace('¥',''))
        comment = int(res.split(',')[3].replace('条评论','').strip())
        obj = {
            'price':price,
            'comment':comment,
        }
        item_list.append(obj)


#计算最大最小值
price_max=sorted(item_list,key=lambda x:x['price'],reverse=True)
comment_max=sorted(item_list,key=lambda x:x['comment'],reverse=True)

price_min=sorted(item_list,key=lambda x:x['price'],reverse=False)
comment_min=sorted(item_list,key=lambda x:x['comment'],reverse=False)
print('价格最大值是：'+str(price_max[0]['price']))
print('价格最小值是：'+str(price_min[0]['price']))

print('评论最大值是：'+str(comment_max[0]['comment']))
print('评论最小值是：'+str(comment_min[0]['comment']))