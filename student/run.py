#!/usr/bin/env python
# -*- coding:utf-8 -*-


import student
import math
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.font_manager import FontProperties

grades = {'优秀':{"min":90,"max":100},'良好':{"min":80,"max":90},'中等':{"min":70,"max":80},'及格':{"min":60,"max":70},'不及格':{"min":0,"max":60}}

def read():
    obj_list = []
    with open('student.csv') as f:
        results = f.readlines()
        flag = 0
        for ress in results:
            res = ress.split(',')
            stu = student.Student()
            stu.num = res[0]
            stu.name = res[1]
            stu.className = res[2]
            stu.usualGrades = res[3]
            stu.practiceGrades = res[4]
            stu.jianmo = res[5]
            stu.sheji = res[6]
            stu.tiaoshi = res[7]
            stu.zhuanxie = res[8]
            # print(stu.name)
            obj_list.append(stu)

            flag+=1
            if flag>2:
                break

    return obj_list

def add(obj_list):
    for obj in obj_list:
        print('当前学生：'+obj.name)
        obj.dazuoye = input('请输入该学生的大作业成绩：')
        obj.zongGrades = float(obj.usualGrades) + float(obj.practiceGrades)*0.4 + float(obj.dazuoye)*0.5
        print('总成绩为：'+str(obj.zongGrades))
        for key in grades.keys():
            if obj.zongGrades >= grades[key]['min'] and obj.zongGrades < grades[key]['max']:
                print("等级为："+key)
                obj.gradesName = key
                print('\n')
                break

def get_one(obj_list):
    name = input('请输入学生姓名:')
    flag = False
    for stu in obj_list:
        if stu.name == name:
            print(stu.name, stu.num, stu.className, stu.usualGrades, stu.practiceGrades, stu.jianmo, stu.sheji,
                  stu.tiaoshi, stu.zhuanxie, stu.zongGrades, stu.gradesName)
            flag = True
            break
        if flag:
            print('系统不存在该学生')

def get_all(obj_list):
    total = 0
    for stu in obj_list:
        print(stu.name, stu.num, stu.className, stu.usualGrades, stu.practiceGrades, stu.jianmo, stu.sheji, stu.tiaoshi,
              stu.zhuanxie, stu.zongGrades, stu.gradesName)
        total += stu.zongGrades
    avg = total / len(obj_list)
    print('班级平均分为：' + str(avg))

    fangcha = 0
    for stu in obj_list:
        fangcha += (stu.zongGrades - avg) * (stu.zongGrades - avg)
    biaozhuncha = fangcha / len(obj_list)
    biaozhuncha = math.sqrt(biaozhuncha)
    print('标准差为：' + str(biaozhuncha))

def chart(obj_list):
    # font = FontProperties(fname=r"/System/Library/Fonts/PingFang.ttc", size=12)
    font = FontProperties(fname=r'C:/Windows/Fonts/msyh.ttf', size=12)
    data = []
    name = []
    for stu in obj_list:
        name.append(stu.name)
        data.append(stu.zongGrades)
    plt.bar(name, data)

    plt.xticks(range(len(data)), name,fontproperties=font)
    plt.show()

if __name__ =='__main__':
    print('系统正在初始化。。。')
    print('=================')
    obj_list = read()
    while True:
        type = input('请输入您要执行的操作([1]录入学生成绩，[2]查询某学生成绩，[3]查询班级成绩分布，[4]图表展示)：')
        if type == '1':
            add(obj_list)
        elif type == '2':
            get_one(obj_list)
        elif type == '3':
            get_all(obj_list)
        elif type == '4':
            chart(obj_list)
        else:
            print('输入有误')
