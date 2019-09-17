from telebotic.connectDB import db
#from helpers import async

import copy

messages = db.trialdata


class MessageModel:
    def __init__(self, data):
        data = data or {}
        for k, v in data.items():
            setattr(self, k, v)

    def to_json(self):
        return self.__dict__

    def save(self):
        try:
            res = messages.insert_one(copy.deepcopy(self.__dict__))
            return res.acknowledged
        except Exception as exc:
            print("[Message Model Error] Insert New Message:", exc.args) 
        return False

    @staticmethod
    def save_one(data):
        try:
            res = messages.insert_one(data)
            return res.acknowledged
        except Exception as exc:
            print ("[Message Model Error] Insert New Message:", exc.args)
        return False

    @staticmethod
    def get_one(args, filters):
        try:
            message = messages.find_one(args, filters)
            if message:
                return message
            return {}
        except Exception as e:
            print ('[Message Model Error] Find message: ' + str(e))
        return {}

    @staticmethod
    def update_message(args, set_query):
        try:
            res = messages.update_one(args, set_query, upsert=False)
            if res.acknowledged:
                return True
            return False
        except Exception as e:
            print ('[Message Model Error] Update message: ' + str(e))
        return False

    @staticmethod
    def get_all(args, filters):
        try:
            ids = messages.find(args, filters)
            if ids:
                return list(ids)
            return []
        except Exception as e:
            print ('[Message Model Error] Get message ids: ' + str(e))
        return []

    @staticmethod
    def delete_one(args):
        try:
            messages.remove(args)
            return True
        except Exception as e:
            print ('[Message Model Error] Delete message: ' + str(e))
        return False