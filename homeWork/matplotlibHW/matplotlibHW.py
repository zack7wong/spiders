#!/usr/bin/env python
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
from idataapi_transform import ProcessFactory, GetterConfig, WriterConfig

#!/usr/bin/env python
# -*- coding:utf-8 -*-


import asyncio
from idataapi_transform import ProcessFactory, GetterConfig, WriterConfig



async def example():

    name_list = []
    list_2012 = []
    list_2013 = []
    list_2014 = []
    list_2015 = []
    list_2016 = []
    list_2017 = []

    #读取数据
    xlsx_config =GetterConfig.RXLSXConfig('表格1.xlsx')
    getter = ProcessFactory.create_getter(xlsx_config)
    async for items in getter:
        for item in items:
            print(item)
            name_list.append(item['项目'])
            list_2012.append(item[2012])
            list_2013.append(item[2013])
            list_2014.append(item[2014])
            list_2015.append(item[2015])
            list_2016.append(item[2016])
            list_2017.append(item[2017])


    #画柱状图
    plt.rcParams['font.sans-serif'] = 'SimHei'
    total_width, n = 0.8, 6
    width = total_width / n
    x = list(range(len(name_list)))

    plt.bar(range(len(name_list)), list_2012, tick_label=name_list, width=width, label='2012')

    for i in range(len(name_list)):
        x[i] = x[i] + width
    plt.bar(x, list_2013, tick_label=name_list, width=width, label='2013')

    for i in range(len(name_list)):
        x[i] = x[i] + width
    plt.bar(x, list_2014, tick_label=name_list, width=width, label='2014')

    for i in range(len(name_list)):
        x[i] = x[i] + width
    plt.bar(x, list_2015, tick_label=name_list, width=width, label='2015')

    for i in range(len(name_list)):
        x[i] = x[i] + width
    plt.bar(x, list_2016, tick_label=name_list, width=width, label='2016')

    for i in range(len(name_list)):
        x[i] = x[i] + width
    plt.bar(x, list_2017, tick_label=name_list, width=width, label='2017')

    plt.legend()
    plt.savefig("柱状图.jpg")
    plt.show()


    #画折线图
    plt.plot(name_list, list_2012, label='2012')
    plt.plot(name_list, list_2013, label='2013')
    plt.plot(name_list, list_2014, label='2014')
    plt.plot(name_list, list_2015, label='2015')
    plt.plot(name_list, list_2016, label='2016')
    plt.plot(name_list, list_2017, label='2017')
    plt.legend()
    plt.savefig("折线图.jpg")
    plt.show()

    #画饼图
    plt.pie(list_2012, labels=name_list, autopct='%1.2f%%')  # 画饼图
    plt.savefig("饼图.jpg")
    plt.show()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(example())