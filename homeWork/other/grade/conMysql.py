#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymysql

class ConMysql():
    def dbconn(self):
        self.host = 'localhost'
        self.username = 'root'
        self.password = 'root'
        self.mydb = 'test'

        self.db = pymysql.connect(self.host, self.username, self.password, self.mydb)
        self.cursor = self.db.cursor()

        print('已连接上数据库')