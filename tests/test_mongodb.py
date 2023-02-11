import unittest
import json
import pymongo
from faker import Faker
from src import get_app
from src.service.mongodb import MongoRepository
from src.model.models import User
from src.config import config


class MongoTestCase(unittest.TestCase):
    def setUp(self):
        self.fake = Faker()
        app = get_app()
        app.config.from_object(config['testing'])
        self.mongo = MongoRepository(uri=app.config['MONGO_URI'], db=app.config['MONGO_DB'], collection_name=app.config['MONGO_DB_COLLECTION'])

    def test_insert_one(self):
        user = User(name=self.fake.name(), email=self.fake.email())
        obj, result_total_num, result_msg = self.mongo.insert_one(user)
        self.assertIsInstance(obj, object)
        self.assertEqual(1, result_total_num)
        self.assertIn('insert success', result_msg)

    def test_insert_many(self):
        count=10
        l = []
        for _ in range(count):
            user = User(name=self.fake.name(), email=self.fake.email())
            l.append(user)
        obj, result_total_num, result_msg = self.mongo.insert_many(l)
        self.assertIsInstance(obj, list)
        self.assertEqual(count, result_total_num)
        self.assertIn('insert many success', result_msg)


    def test_update_by_id(self):
        user = User(name=self.fake.name(), email=self.fake.email())
        obj = self.mongo.db[self.mongo.collection_name].insert_one(json.loads(json.dumps(user, default=lambda o: o.__dict__)))
        inserted_id = obj.inserted_id
        user.name = self.fake.name()
        obj, result_total_num, result_msg = self.mongo.update_by_id(inserted_id, user)
        self.assertIsInstance(obj, object)
        self.assertEqual(1, result_total_num)
        self.assertIn('update success', result_msg)

    def test_query(self):
        count=10
        l = []
        for _ in range(count):
            user = User(name=self.fake.name(), email=self.fake.email())
            l.append(user)
        obj, result_total_num, result_msg = self.mongo.insert_many(l)
        query = {}
        sort = ('name', pymongo.ASCENDING)
        obj, result_total_num, result_msg = self.mongo.query(query=query, sort=sort)
        self.assertIsInstance(obj, list)
        self.assertEqual(count, result_total_num)
        self.assertIn('query success', result_msg)

    def test_query_by_page(self):
        count=10
        l = []
        for _ in range(count):
            user = User(name=self.fake.name(), email=self.fake.email())
            l.append(user)
        obj, result_total_num, result_msg = self.mongo.insert_many(l)
        query = {}
        sort = ('name', pymongo.ASCENDING)
        page = 1
        page_size = 5
        obj, result_total_num, result_msg = self.mongo.query_by_page(query=query, sort=sort, page=page, page_size=page_size)
        self.assertIsInstance(obj, list)
        self.assertEqual(count, result_total_num)
        self.assertIn('query by page success', result_msg)

    def test_query_by_id(self):
        user = User(name=self.fake.name(), email=self.fake.email())
        obj = self.mongo.db[self.mongo.collection_name].insert_one(json.loads(json.dumps(user, default=lambda o: o.__dict__)))
        inserted_id = obj.inserted_id
        obj, result_total_num, result_msg = self.mongo.query_by_id(inserted_id)
        self.assertIsInstance(obj, object)
        self.assertEqual(1, result_total_num)
        self.assertIn('query by id success', result_msg)

    def test_delete_by_id(self):
        user = User(name=self.fake.name(), email=self.fake.email())
        obj = self.mongo.db[self.mongo.collection_name].insert_one(json.loads(json.dumps(user, default=lambda o: o.__dict__)))
        inserted_id = obj.inserted_id
        obj, result_total_num, result_msg = self.mongo.delete_by_id(str(inserted_id))
        self.assertIsInstance(obj, object)
        self.assertEqual(1, result_total_num)
        self.assertIn('delete by id success', result_msg)

    def test_delete_many(self):
        count=10
        l = []
        for _ in range(count):
            user = User(name=self.fake.name(), email=self.fake.email())
            l.append(user)
        obj, result_total_num, result_msg = self.mongo.insert_many(l)
        query = {}
        obj, result_total_num, result_msg = self.mongo.delete_many(query=query)
        self.assertIsInstance(obj, object)
        self.assertEqual(count, result_total_num)
        self.assertIn('delete many success', result_msg)

    def tearDown(self):
        self.mongo.db[self.mongo.collection_name].drop()
