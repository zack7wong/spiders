from config import *
import pymysql
import redis

class MysqlClient(object):
    def __init__(self, host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB,charset=MYSQL_CHARSET):
        self.client = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        self.cursor = self.client.cursor()

    def save(self, sql):
        try:
            self.cursor.execute(sql)
            self.client.commit()
        except:
            self.client.rollback()

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

class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        self.client = redis.Redis(host=host, port=port)

    def push(self, redis_key, redis_res):
        try:
            print('pushing...' + str(redis_key) + '...' + str(redis_res))
            self.client.rpush(redis_key, redis_res)
        except:
            print('push失败', + str(redis_res))
            return None

    def pop(self, redis_key):
        try:
            results = self.client.blpop(redis_key, timeout=5)
            return results
        except:
            print("pop Error: unable to fetch data")
            return None

    def llen(self, redis_key):
        try:
            results = self.client.llen(redis_key)
            return results
        except:
            print("llen Error: unable to fetch data")
            return None

if __name__ == '__main__':
    conn = MongoClient()
    data = {
        'user_id':1266321801,
        'aa':'aaga'
    }
    conn.save(data)
