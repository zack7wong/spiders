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

all_list = []
exist_id = []

async def example():
    # for typeid in type_list:
    #     url_obj = GetterConfig.RAPIConfig(URL.format(typeid=typeid), filter_=func_creator(), max_limit=None)
    #     print(URL.format(typeid=typeid))
    #     URL_OBJ_LIST.append(url_obj)

    one = GetterConfig.RXLSXConfig('hainan.xlsx')
    one_getter = ProcessFactory.create_getter(one)

    two_config = GetterConfig.RXLSXConfig('hainan2.xlsx')
    two_getter = ProcessFactory.create_getter(two_config)

    three_config = GetterConfig.RXLSXConfig('hainan3.xlsx')
    three_getter = ProcessFactory.create_getter(three_config)

    four_config = GetterConfig.RXLSXConfig('hainan4.xlsx')
    four_getter = ProcessFactory.create_getter(four_config)

    async for items in one_getter:
        for item in items:
            all_list.append(item)

    async for items in two_getter:
        for item in items:
            all_list.append(item)

    async for items in three_getter:
        for item in items:
            all_list.append(item)

    async for items in four_getter:
        for item in items:
            all_list.append(item)


    xlsx_config = WriterConfig.WXLSXConfig("./hainan_all2.xlsx")
    with ProcessFactory.create_writer(xlsx_config) as xlsx_writer:
        item_copy = copy.copy(all_list)
        for item in all_list:
            if item['id'] in exist_id:
                print('del:' + str(item_copy[item_copy.index(item)]))
                del item_copy[item_copy.index(item)]
            else:
                exist_id.append(item['id'])
        # print(item_copy)
        xlsx_writer.write(item_copy)



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