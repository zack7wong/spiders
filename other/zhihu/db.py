import pymysql


#mysql配置
MYSQL_HOST = 'localhost'
MYSQL_DB = 'zhihu'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
MYSQL_CHARSET = 'utf8'


class MysqlClient(object):
    def __init__(self, host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB,charset=MYSQL_CHARSET):
        self.client = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        self.cursor = self.client.cursor()

    def save(self, sql):
        try:
            self.cursor.execute(sql)
            self.client.commit()
            print('存储成功')
        except:
            self.client.rollback()
            print('存储失败')

    def find_all(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except:
            print("Error: unable to fetch data")
            return None

    def find_one(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchone()
            return results
        except:
            print("Error: unable to find_one  data")
            return None

