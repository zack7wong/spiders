import pymongo

#mongodb配置
MONGO_URL = 'localhost'
MONGO_DB = 'douban'
MONGO_TABLE_USER = 'doubanRes'
MONGO_PORT = 27017
MONGO_PASSWORD = None

class MongoClient(object):
    def __init__(self, host=MONGO_URL, port=MONGO_PORT, password=MONGO_PASSWORD):
        self.client = pymongo.MongoClient(host=host, port=port, password=password)
        self.db = self.client[MONGO_DB]
        self.table_user = self.db[MONGO_TABLE_USER]

    def count(self):
        count_num = self.db.get_collection(MONGO_TABLE_USER).count()
        return count_num

    def find(self,user_id):
        user_id = int(user_id)
        results = self.db.get_collection(MONGO_TABLE_USER).find_one({'user_id':user_id})
        if results:
            return results
        else:
            return None

    def find_one_flag(self):
        results = self.db.get_collection(MONGO_TABLE_USER).find_one({'flag':False})
        if results:
            return results
        else:
            return None

    def find_flag(self):
        results = self.db.get_collection(MONGO_TABLE_USER).find({'flag':False})
        if results:
            return results
        else:
            return None

    def all(self):
        results = self.db.get_collection(MONGO_TABLE_USER).find()
        return results

    def save(self,results):
        if self.table_user.update({'bookName':results['bookName']},{'$set':results},True):
            print('存储到MongoDB成功',results)
            return True
        else:
            print('存储失败',results)
            return False

    def save_first(self,results):
        res = self.find(results['user_id'])
        if res:
            print(results['user'],'已经在数据库中')
        else:
            if self.table_user.insert(results):
                print('存储到mongodb成功',results)
                return True
            else:
                print('存储失败',results)
                return False
