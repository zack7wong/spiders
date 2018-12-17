#!/usr/bin/env python
# -*- coding:utf-8 -*-
import turtle
import time

turtle.pensize(4)
turtle.pencolor("yellow") #画笔黄色
turtle.fillcolor("red") #内部填充红色

#绘制五角星#
turtle.begin_fill()
for _ in range(5): #重复执行5次
    turtle.forward(200) #向前移动200步
    turtle.right(144)  #向右移动144度，
turtle.end_fill() #结束填充红色
time.sleep(1)


turtle.mainloop()