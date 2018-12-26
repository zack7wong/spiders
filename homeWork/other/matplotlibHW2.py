#!/usr/bin/env python
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
# %matplotlib inline

import xlrd

def read_xls_file():
    data = xlrd.open_workbook('dangdang.xlsx')
    table = data.sheets()[0]  # 通过索引顺序获取
    # table = data.sheet_by_index(0)  # 通过索引顺序获取
    # table = data.sheet_by_name(u'Sheet1')  # 通过名称获取
    results = []
    for i in range(1,180):
        name = table.cell(i, 0).value
        xianjia = table.cell(i, 1).value
        yuanjia = table.cell(i, 2).value
        obj = {
            'name': name,
            'xianjia': xianjia,
            'yuanjia': yuanjia,
        }
        results.append(obj)
    return results
item_obj = read_xls_file()
print(item_obj)
name_list = []
xianjia_list = []
yuanjia_list = []
zhekou_list = []
for item in item_obj:
    name_list.append(item['name'])
    xianjia_list.append(float(item['xianjia']))
    yuanjia_list.append(float(item['yuanjia']))
    zhekou_list.append((float(item['yuanjia'])-float(item['xianjia']))/float(item['yuanjia']))

print(name_list)
print(xianjia_list)
print(yuanjia_list)
print(zhekou_list)

x = name_list[:10]
y1 = xianjia_list[:10]
y2 = yuanjia_list[:10]

plt.plot(x, y1, color='green', label='now')
plt.plot(x, y2, color='red', label='old')
plt.legend()
plt.show()

plt.scatter(yuanjia_list, zhekou_list, alpha=0.6)  # 绘制散点图，透明度为0.6（这样颜色浅一点，比较好看）
plt.show()



# es = Scatter('散点图',background_color = 'white',title_text_size = 5,width=1500)
# v11 = zhekou_list
# es.add('折扣', yuanjia_list,v11)
# es.render(path = '散点图.html')
#
