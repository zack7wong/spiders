#!/usr/bin/env python
# -*- coding:utf-8 -*-

while True:
    print('用户信息管理系统')
    print(' 1.显示全部已注册用户')
    print(' 2.查找/修改/删除用户信息')
    print(' 3.添加新用户')
    print(' 4.保存用户数据')
    print(' 5.退出系统')
    print('请输入序号选择对应菜单：',end='')
    mytype = input('')

    if mytype == '1':
        try:
            with open('user.csv') as f:
                results = f.readlines()
                if len(results) <= 0:
                    print('该系统暂无用户\n')
                    input('按Enter键继续......')
                else:
                    print('当前已注册用户信息如下：')
                    for res in results:
                        uname = res.split(',')[0]
                        pwd = res.split(',')[1].strip()
                        obj = {
                            'uname':uname,
                            'pwd':pwd,
                        }
                        print(obj)

        except:
            print('该系统暂无用户\n')
            input('按Enter键继续......')

    if mytype == '2':
        item_list= []
        find_name = input('请输入要查找的用户名：')
        try:
            with open('user.csv') as f:
                results = f.readlines()
                if len(results) <= 0:
                    print(find_name + ' 不存在！\n')
                    input('按Enter键继续......')

                flag = True
                for res in results:
                    uname = res.split(',')[0]
                    pwd = res.split(',')[1].strip()
                    if uname == find_name:
                        flag = False
                        print(find_name + ' 已经注册！')
                        print('请选择操作：')
                        print(' 1.修改用户')
                        print(' 2.删除用户')
                        caozuoType = input('请输入序号选择对应操作：')
                        if caozuoType == '1':
                            uname = input('请输入新的用户名：')
                            pwd = input('请输入新用户登录密码：')
                            pwd = pwd.strip()
                            print('\n 已成功修改用户！\n')
                            input('按Enter键继续......')

                        elif caozuoType == '2':
                            print('\n 已成功删除用户！\n')
                            input('按Enter键继续......')
                            continue
                        else:
                            pass

                    item_list.append(uname + ',' + pwd + '\n')

                if flag:
                    print(find_name + ' 不存在！\n')
                    input('按Enter键继续......')

            with open('user.csv','w') as f:
                for item in item_list:
                    f.write(item)
        except:
            print(find_name+' 不存在！\n')
            input('按Enter键继续......')

    if mytype == '3':
        newuname = input('请输入新的用户名：')
        newpwd = input('请输入新的用户登录密码：')

        with open('user.csv','a') as f:
            f.write(newuname+','+newpwd+'\n')

        print('\n 已成功添加用户！\n')
        input('按Enter键继续......')

    if mytype == '4':
        print('已成功保存用户信息\n')
        input('按Enter键继续......')


    if mytype == '5':
        print('谢谢使用，系统已退出')
        exit(0)