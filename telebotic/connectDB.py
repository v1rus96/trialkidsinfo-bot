import pymongo
from pymongo import MongoClient
mongo = MongoClient('mongodb://admin:firik1996@ds263127.mlab.com:63127/trialkids/retryWrites=false')
db = mongo['trialkids']
          
          
# class DB(object):
          
#     URI = "mongodb://admin:firik1996@ds263127.mlab.com:63127/trialkids"
          
#     @staticmethod
#     def init():
#         client = pymongo.MongoClient(DB.URI)
#         DB.DATABASE = client['trialkids']                                                                                                                                   
          
#     @staticmethod
#     def insert(collection, data):
#         DB.DATABASE[collection].insert(data)
          
#     @staticmethod
#     def find_one(collection, query):
#         return DB.DATABASE[collection].find_one(query)