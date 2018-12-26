#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pyecharts import Bar
from pyecharts import Line,configure

jiuyue_list = []
shiyue_list = []
shiyiyue_list = []
shieryue_list = []

# res_list = []
# for i in range(1,32):
#     res_list.append(str(i))
# print(res_list)
riqi_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']

with open('三亚清洗数据.csv') as f:
    results = f.readlines()
    for res in results:
        mydate = res.split(',')[0]
        zuidi_qiwen = int(res.split(',')[2])
        zuigao_qiwen = int(res.split(',')[3].strip())
        if '09月' in mydate:
            jiuyue_list.append(zuidi_qiwen)
        elif '10月' in mydate:
            shiyue_list.append(zuidi_qiwen)
        elif '11月' in mydate:
            shiyiyue_list.append(zuidi_qiwen)
        elif '12月' in mydate:
            shieryue_list.append(zuidi_qiwen)


line =Line('折线图',background_color = 'white',title_text_size = 5,width=1500)
attr = riqi_list
v9 = jiuyue_list[:30]
v10 = shiyue_list[:30]
v11 = shiyiyue_list[:30]
# v12 = shieryue_list[:30][:30]

line.add('9月',attr,v9,mark_line=['average'],is_label_show = True)
line.add('10月',attr,v10,mark_line=['average'],is_label_show = True)
line.add('11月',attr,v11,mark_line=['average'],is_label_show = True)
# line.add('12月',attr,v12,mark_line=['average'],is_label_show = True)
line.render(path = '三亚气温.html')
