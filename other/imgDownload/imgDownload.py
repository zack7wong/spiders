#!/usr/bin/env python
# -*- coding:utf-8 -*-

#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     imgDownload
   Description :
   Author :        hayden_huang
   Date：          2018/12/19 00:07
-------------------------------------------------
"""

import urllib.request
from collections import OrderedDict
from pyexcel_xls import get_data
from pyexcel_xls import save_data


filename = '图片链接.xlsx'
savename = 'img/'
retry_num = 0
max_num = 5
error_list = []
success_list = []


def download(url,x):
    print('正在下载:' + url)
    global retry_num
    if retry_num > max_num:
        return None
    try:
        save_filenmae = savename + '/%s.jpg' % x
        urllib.request.urlretrieve(url, save_filenmae)
        retry_num = 0
        with open('下载成功的图片链接.txt','a') as f:
            f.write(url+'\n')
        return True
    except:
        print('正在重试：'+str(retry_num)+' '+url)
        retry_num +=1
        download(url,x)



def start():
    print('当前文件：'+filename)
    global retry_num
    all_url_list = []
    try:
        with open('下载成功的图片链接.txt') as f:
            all_url = f.readlines()
            for res in all_url:
                all_url_list.append(res.strip())
    except:
        pass


    results = read_xls_file(filename)
    x = 1
    for res in results:
        if res['url'] in all_url_list:
            print('已下载：'+res['url'])
            continue

        downres = download(res['url'],x)
        if downres:
            x += 1
            retry_num = 0
        else:
            error_list.append(res['url'])
            retry_num = 0
            print("出错:"+res['url'])
    if len(error_list)>0:
        save_xls_file(error_list)
    print('下载完成')

def save_xls_file(results):
    data = OrderedDict()
    # sheet表的数据
    sheet_1 = []
    for res in results:
        row_2_data = [res]
        sheet_1.append(row_2_data)
    data.update({"失败url": sheet_1})

    # 保存成xls文件
    save_data('下载失败.xls', data)

def read_xls_file(filename):
    xls_data = get_data(filename)
    results = []
    for sheet_n in xls_data.keys():
        for item in xls_data[sheet_n]:
            # print(item)
            url = item[0]

            obj ={
                'url': url,
            }
            # print(obj)
            results.append(obj)
    return results


if __name__ == '__main__':
    # results = read_xls_file(filename)
    # print(results)
    # num = 1
    # for res in results:
    #     download(res['url'],num)
    #     num+=1

    start()