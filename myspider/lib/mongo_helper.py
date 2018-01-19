#coding=utf-8

from pymongo.database import Database
from pymongo import MongoClient

class Mongo(object):
    '''  封装数据库操作 '''
    def __init__(self, host='localhost', port=27017, database='common', max_pool_size=10, timeout=10):
        self.host = host
        self.port = port
        self.max_pool_size = max_pool_size
        self.timeout = timeout
        self.database = database

    @property
    def connection(self):
        return MongoClient(self.host, self.port, maxPoolSize=self.max_pool_size, connectTimeoutMS=60 * 60 * self.timeout)

    def __getitem__(self, collection):
        return self.__getattr__(collection)

    def __getattr__(self, collection_or_func):
        db = self.connection[self.database]
        if collection_or_func in Database.__dict__:
            return getattr(db, collection_or_func)
        return Collection(db, collection_or_func)

    def __del__(self):
        self.connection.close()

class Collection(object):
    def __init__(self, db, collection):
        self.collection = getattr(db, collection)

    def __getattr__(self, operation):
        control_type = ['insert_one', 'remove', 'insert', 'update', 'find', 'find_one', 'drop']
        if operation in control_type:
            return getattr(self.collection, operation)
        raise AttributeError(operation)

if __name__ == '__main__':
    db = Mongo()
    print(db.name)
    print([ip for ip in db.proxy.find()])
    #for doc in db.proxy.find():
    #print(doc['name'])
    #db.jandan.find_one()
    #db.jandan.count()
    #db.jandan.insert_one({'x': 'usa'})

    #db.jandan.find().sort('name') #排序, 默认为升序
    #db.jandan.find().sort('name', ASCENDING)
    #db.jandan.find().sort('name', DESCENDING)
    #db.jandan.find().sort([('name', ASCENDING), ('age', DESCENDING)])
    #db.jandan.insert({'name': 'wang'})
    #db.jandan.update({'name': 'wang'}, {'$set': {'age':25, 'gender': 'male'}})

    #db.jandan.remove({'name':'tony'})
    #db.jandan.remove()
