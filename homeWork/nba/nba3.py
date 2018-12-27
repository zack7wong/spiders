#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pyecharts import Bar
from pyecharts import Line,configure
from pyecharts import Radar

name_list = [{'key':'lebronjames-650','name':'詹姆斯清洗后的数据.csv'},{'key':'kevindurant-1236','name':'杜兰特清洗后的数据.csv'},{'key':'stephencurry-3311','name':'库里清洗后的数据.csv'}]

for name_obj in name_list:
    with open(name_obj['name']) as f:
        results = f.readlines()

    year_list = results[0].strip().split(',')
    changci_list = results[1].strip().split(',')
    mingzhonglv_list = results[2].strip().split(',')
    defen_list = results[3].strip().split(',')
    pingjun_list = results[4].strip().split(',')

    # for i in range(0, 11):
    #     year_list[i] = int(year_list[i])
    for i in range(0,11):
        changci_list[i] = int(changci_list[i])
    for i in range(0,11):
        mingzhonglv_list[i] = float(mingzhonglv_list[i][:-1])
    for i in range(0,11):
        defen_list[i] = float(defen_list[i])
    for i in range(0,5):
        pingjun_list[i] = float(pingjun_list[i])

    print(year_list)
    print(changci_list)
    print(mingzhonglv_list)
    print(defen_list)
    print(pingjun_list)

    line_name = name_obj['name'].replace('清洗后的数据.csv','折线图')+'.html'
    line = Line('折线图', background_color='white', title_text_size=5, width=1500)
    line.add('场次', year_list, changci_list, mark_line=['average'], is_label_show=True)
    line.add('命中率', year_list, mingzhonglv_list, mark_line=['average'], is_label_show=True)
    line.add('得分', year_list, defen_list, mark_line=['average'], is_label_show=True)
    line.render(path=line_name)

    #雷达图
    # 2个系列的5个维度的数据
    value1 = [pingjun_list]

    # 用于调整雷达各维度的范围大小
    c_schema = [{"name": "篮板", "max": 10, "min": -1},
                {"name": "助攻", "max": 10, "min": -1},
                {"name": "抢断", "max": 10, "min": -1},
                {"name": "盖帽", "max": 10, "min": -1},
                {"name": "失误", "max": 10, "min": -1}]


    #画图
    rader_name = name_obj['name'].replace('清洗后的数据.csv', '雷达图') + '.html'
    radar = Radar()
    radar.config(c_schema=c_schema)
    radar.add("雷达图", value1)
    radar.render(rader_name)