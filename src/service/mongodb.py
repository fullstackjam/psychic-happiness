from src.repository.BaseRepository import BaseRepository
from pymongo import MongoClient


class MongoRepository(BaseRepository):
    def __init__(self, uri, db, collection_name):
        self.client = MongoClient(uri)
        self.db = self.client[db]
        super().__init__(self.db, collection_name)
