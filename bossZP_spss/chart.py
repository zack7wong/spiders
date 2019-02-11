#!/usr/bin/env python
# -*- coding:utf-8 -*-

import db
import matplotlib.pyplot as plt
import pandas as pd

def deal_chengshi(results):
    item_list = []
    account_list = []
    for res in results:
        if res[6] in account_list:
            for item in item_list:
                if item['key'] == res[6]:
                    item['value']+=1
                    break
        else:
            account_list.append(res[6])
            obj = {
                'key':res[6],
                'value':1
            }
            item_list.append(obj)

    item_list = sorted(item_list,key=lambda x:x['value'],reverse=True)
    name_list = []
    num_list = []
    for item in item_list[:10]:
        name_list.append(item['key'])
        num_list.append(item['value'])

    # plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.bar(range(len(num_list)), num_list, tick_label=name_list)
    plt.savefig("城市分布柱状图.jpg")
    plt.show()


    plt.pie(num_list, labels=name_list, autopct='%1.2f%%')  # 画饼图
    plt.savefig("城市分布饼图.jpg")
    plt.show()

def deal_chengshi_price(results):
    chengshi_list = []
    # price_list = []
    for res in results:
        # print(res)
        if res[6] == None:
            continue
        chengshi = res[6]
        price = ((int(res[9].split('-')[0].split('K')[0]) + int(res[9].split('-')[1].split('K')[0]))/2)*1000
        # print(price)
        obj = {
            'chengshi':chengshi,
            'price':price
        }
        chengshi_list.append(obj)
        # price_list.append(price)

    item_list = []
    account_list = []
    for res in chengshi_list:
        if res['chengshi'] in account_list:
            for item in item_list:
                if item['chengshi'] == res['chengshi']:
                    item['account'] += 1
                    item['price'] += res['price']
                    break
        else:
            account_list.append(res['chengshi'])
            obj = {
                'chengshi': res['chengshi'],
                'account': 1,
                'price': res['price'],
            }
            item_list.append(obj)
    print(item_list)

    name_list = []
    num_list = []
    for item in item_list:
        name_list.append(item['chengshi'])
        num_list.append(int(item['price']/item['account']))
    print(name_list)
    print(num_list)

    plt.bar(range(len(num_list)), num_list, tick_label=name_list)
    plt.savefig("薪资分布柱状图.jpg")
    plt.show()

def deal_xueli(results):
    item_list = []
    account_list = []
    for res in results:
        if res[8] in account_list:
            for item in item_list:
                if item['key'] == res[8]:
                    item['value'] += 1
                    break
        else:
            account_list.append(res[8])
            obj = {
                'key': res[8],
                'value': 1
            }
            item_list.append(obj)

    item_list = sorted(item_list, key=lambda x: x['value'], reverse=True)
    name_list = []
    num_list = []
    for item in item_list[:10]:
        name_list.append(item['key'])
        num_list.append(item['value'])

    # plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.bar(range(len(num_list)), num_list, tick_label=name_list)
    plt.savefig("学历分布柱状图.jpg")
    plt.show()

    plt.pie(num_list, labels=name_list, autopct='%1.2f%%')  # 画饼图
    plt.savefig("学历分布饼图.jpg")
    plt.show()


def main():
    sql = "select * from positions"
    results = mysqlCli.find_all(sql)

    # deal_chengshi(results)
    # deal_chengshi_price(results)
    deal_xueli(results)

if __name__ == '__main__':
    mysqlCli = db.MysqlClient()
    main()