from config import *
import pymongo
#mongodb配置
MONGO_URL = 'localhost'
MONGO_DB = 'weibo'
MONGO_TABLE_POST = 'weibo_post'
MONGO_TABLE_COMMENT = 'weibo_comment'
MONGO_TABLE_WENZHANG = 'weibo_wenzhang'
MONGO_PORT = 27017
MONGO_PASSWORD = None

#redis配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = ''
REDIS_EMPLOYMENT = 'employment'

#mysql配置
MYSQL_HOST = 'localhost'
MYSQL_DB = 'employment'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
MYSQL_CHARSET = 'utf8'


class MongoClient(object):
    def __init__(self, host=MONGO_URL, port=MONGO_PORT, password=MONGO_PASSWORD):
        self.client = pymongo.MongoClient(host=host, port=port, password=password)
        self.db = self.client[MONGO_DB]
        self.table_post = self.db[MONGO_TABLE_POST]
        self.table_comment = self.db[MONGO_TABLE_COMMENT]
        self.table_wenzhang = self.db[MONGO_TABLE_WENZHANG]

    def count(self,myTable):
        count_num = self.db.get_collection(myTable).count()
        return count_num

    def find(self,user_id,myTable):
        user_id = int(user_id)
        results = self.db.get_collection(myTable).find_one({'user_id':user_id})
        if results:
            return results
        else:
            return None

    def find_one_flag(self,myTable):
        results = self.db.get_collection(myTable).find_one({'flag':False})
        if results:
            return results
        else:
            return None

    def find_flag(self,myTable):
        results = self.db.get_collection(myTable).find({'flag':False})
        if results:
            return results
        else:
            return None

    def all(self,myTable):
        results = self.db.get_collection(myTable).find()
        return results

    def save_post(self,results):
        if self.table_post.update({'postId':results['postId']},{'$set':results},True):
            print('存储微博到MongoDB成功',results)
            return True
        else:
            print('存储微博失败',results)
            return False

    def save_comment(self,results):
        if self.table_comment.update({'commentId':results['commentId']},{'$set':results},True):
            print('存储评论到MongoDB成功',results)
            return True
        else:
            print('存储评论失败',results)
            return False

    def save_wenzhang(self,results):
        if self.table_wenzhang.update({'wenzhangId':results['wenzhangId']},{'$set':results},True):
            print('存储文章到MongoDB成功',results)
            return True
        else:
            print('存储文章失败',results)
            return False

    def save_first(self,results):
        res = self.find(results['user_id'])
        if res:
            print(results['user'],' 该用户已经在数据库中')
        else:
            if self.table_user.insert(results):
                print('存储到mongodb成功',results)
                return True
            else:
                print('存储失败',results)
                return False


if __name__ == '__main__':
    conn = MongoClient()
    data = {
        'user_id':1266321801,
        'aa':'aaga'
    }
    conn.save(data)
