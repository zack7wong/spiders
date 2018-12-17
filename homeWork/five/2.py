#!/usr/bin/env python
# -*- coding:utf-8 -*-

import turtle, datetime
def drawGap(): #绘制数码管间隔
    turtle.penup()
    turtle.fd(5)
def drawLine2(draw):   #绘制单段数码管
    drawGap()
    turtle.pendown() if draw else turtle.penup()
    turtle.fd(40)
    drawGap()
    turtle.right(90)
def drawDigit2(d): #根据数字绘制七段数码管
    drawLine2(True) if d in [2,3,4,5,6,8,9] else drawLine2(False)
    drawLine2(True) if d in [0,1,3,4,5,6,7,8,9] else drawLine2(False)
    drawLine2(True) if d in [0,2,3,5,6,8,9] else drawLine2(False)
    drawLine2(True) if d in [0,2,6,8] else drawLine2(False)
    turtle.left(90)
    drawLine2(True) if d in [0,4,5,6,8,9] else drawLine2(False)
    drawLine2(True) if d in [0,2,3,5,6,7,8,9] else drawLine2(False)
    drawLine2(True) if d in [0,1,2,3,4,7,8,9] else drawLine2(False)
    turtle.left(180)
    turtle.penup()
    turtle.fd(20)
def drawDate2(date):
    turtle.pencolor("red")
    for i in date:
        if i == '-':
            turtle.write(':',font=("Arial", 18, "normal"))
            turtle.pencolor("green")
            turtle.fd(40)
        elif i == '=':
            turtle.write(':',font=("Arial", 18, "normal"))
            turtle.pencolor("blue")
            turtle.fd(40)
        elif i == '+':
            turtle.write('',font=("Arial", 18, "normal"))
        else:
            drawDigit2(eval(i))
def main2():
    turtle.setup(800, 350, 200, 200)
    turtle.penup()
    turtle.fd(-350)
    turtle.pensize(5)
    drawDate2(datetime.datetime.now().strftime('%H-%M=%S+'))
    turtle.hideturtle()
main2()