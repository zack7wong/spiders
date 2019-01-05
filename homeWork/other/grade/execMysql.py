#!/usr/bin/env python
# -*- coding:utf-8 -*-

import conMysql

class ExecMysql():
    def __init__(self):
        self.myCon = conMysql.ConMysql()
        self.myCon.dbconn()

    def insert(self,name,liucheng,uml,php,avg,rank,gradeSore):
        sql = "insert into grade(姓名,流程图,UML,PHP,平均分,排名,等级) values('%s','%s','%s','%s','%s','%s','%s')"%(name,liucheng,uml,php,avg,rank,gradeSore)
        self.myCon.cursor.execute(sql)
        self.myCon.db.commit()

    def researchDate(self):
        sql = 'select * from grade'
        self.myCon.cursor.execute(sql)
        results = self.myCon.cursor.fetchall()
        # print(results)
        return results

if __name__ == '__main__':
    exe = ExecMysql()
    exe.researchDate()
    # exe.insert('zz','zz','zz','zz','zz','zz','zz')