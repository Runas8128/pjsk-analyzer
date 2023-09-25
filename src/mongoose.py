from os import environ
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from pandas import DataFrame

class Mongoose:
    __client = None
    
    @classmethod
    @property
    def client(cls):
        if not cls.__client:
            cls.__client = MongoClient(environ.get('MONGODB_URL'), server_api=ServerApi('1'))
        return cls.__client

    @classmethod
    def test(cls):
        try:
            cls.client.admin.command('ping')
            print("Pinged deployment. Successfully connected to MongoDB!")
        except Exception as e:
            print(e)
    
    @classmethod
    def has(cls, uid: str, data: dict):
        col = cls.client['pjsk_db'][uid]
        return len(DataFrame(col.find(data)).index) != 0

    @classmethod
    def get(cls, uid: str, data: dict):
        return list(cls.client['pjsk_db'][uid].find(data))
    
    @classmethod
    def upload(cls, uid: str, data: dict):
        col = cls.client['pjsk_db'][uid]
        col.insert_one(data)
