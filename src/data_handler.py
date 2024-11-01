# src/data_handler.py

from pymongo import MongoClient

class DataHandler:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="linkedin_data"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.posts = self.db["posts"]

    def store_post_data(self, post_data):
        self.posts.insert_one(post_data)

