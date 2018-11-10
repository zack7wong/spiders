#!/usr/bin/env python
# -*- coding:utf-8 -*-

import download
import json
import re
import os
import train
import config
import time
import calculation


if __name__ == '__main__':
    if config.SPIDER == True:
        tra = train.Train()
        sql_results = tra.get_site()
        results = tra.judge(sql_results)
        print(results)
        for start in results:
            for end in results:
                if start[3] == end[3]:
                    continue

                for datetime in config.TIME_LIST:
                    start_url = config.START_URL.format(start=start[3], end=end[3], datetime=datetime)
                    print(start[2] + ' to ' + end[2] + ' time: ' + datetime)
                    print(start_url)
                    tra.get_results(start_url,start,end,datetime)
                    time.sleep(1)
    elif config.Calculation == True:
        cal = calculation.Calculation()
        cal.start()