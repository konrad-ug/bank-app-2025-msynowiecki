from pymongo import MongoClient
from src.account_registry import AccountRegistry

class MongoAccountsRepository(AccountRegistry):
    def __init__(self):
        super().__init__()
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client["bank"]
        self.collection = self.db["accounts"]

    def save_all(self, accounts):
        self.collection.delete_many({})  # czyścimy kolekcję
        for account in accounts:
            self.collection.update_one(
                {"pesel": account.pesel},
                {"$set": account.to_dict()},
                upsert=True
            )

    def load_all(self):
        return list(self.collection.find({}, {"_id": 0}))
