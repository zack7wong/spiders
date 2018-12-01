#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     csv_deal
   Description :
   Author :        hayden_huang
   Date：          2018/12/1 13:05
-------------------------------------------------
"""

#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     api2xlsx_weixin
   Description :
   Author :        hayden_huang
   Date：          2018/11/23 11:27
-------------------------------------------------
"""

import asyncio
import copy
import re
from idataapi_transform import ProcessFactory, GetterConfig, WriterConfig

type_list = ['1']
del_LIST = ['description','imageUrls']
URL = 'http://api02.bitspaceman.com:8000/house/anjuke?cityid=322&type={typeid}&apikey=fAV2GSoZ4OY0IoIyRZQdnB4bLcB2fyDe4DwIRkX1pAQuKbu1qcaNHPuOMV5J70N1'
URL_OBJ_LIST = []
all_id = []

#过滤器，这里处理字段
def func_creator():
    def parse_item(item):
        for key in list(item.keys()):
            if key in del_LIST:
                del (item[key])
            else:
                pass
        return item
    return parse_item

jiaqi_list = []
kongqi_list = []
qiwen_list = []

async def example():
    # for typeid in type_list:
    #     url_obj = GetterConfig.RAPIConfig(URL.format(typeid=typeid), filter_=func_creator(), max_limit=None)
    #     print(URL.format(typeid=typeid))
    #     URL_OBJ_LIST.append(url_obj)

    jiaqi_config = GetterConfig.RCSVConfig('jiaqi.csv')
    jiaqi_getter = ProcessFactory.create_getter(jiaqi_config)

    kongqi_config = GetterConfig.RCSVConfig('kongqi_all.csv')
    kongqi_getter = ProcessFactory.create_getter(kongqi_config)

    qiwen_config = GetterConfig.RCSVConfig('qiwen.csv')
    qiwen_getter = ProcessFactory.create_getter(qiwen_config)

    async for items in jiaqi_getter:
        for item in items:
            jiaqi_list.append(item)

    async for items in kongqi_getter:
        for item in items:
            kongqi_list.append(item)

    async for items in qiwen_getter:
        for item in items:
            qiwen_list.append(item)

    print(len(jiaqi_list))
    print(len(kongqi_list))
    print(len(qiwen_list))

    all_res_list = []
    xlsx_config = WriterConfig.WXLSXConfig("./all_results.xlsx")
    with ProcessFactory.create_writer(xlsx_config) as xlsx_writer:
        for kongqi in kongqi_list:
            for qiwen in qiwen_list:
                if qiwen['城市'] == kongqi['城市'] and qiwen['日期'] == kongqi['日期']:
                    for jiaqi in jiaqi_list:
                        if jiaqi['日期'] == kongqi['日期']:
                            save_res = {**kongqi, **qiwen,**jiaqi}
                            # print(save_res)
                            all_res_list.append(save_res)

        xlsx_writer.write(all_res_list)



    #
    #
    # xlsx_config = WriterConfig.WXLSXConfig("./all_results.xlsx")
    #     with ProcessFactory.create_writer(xlsx_config) as xlsx_writer:
    #         async for items in getter:
    #             for item in items:
    #                 print(item)
    #             xlsx_writer.write(items)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(example())