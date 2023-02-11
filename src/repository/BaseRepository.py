from bson import ObjectId
import json

class BaseRepository:
    def __init__(self, db: object, collection_name: str):
        self.db = db
        self.collection_name = collection_name

    def insert_one(self, entity: object):
        self.db[self.collection_name].insert_one(json.loads(json.dumps(entity, default=lambda o: o.__dict__)))
        return entity, 1, 'insert success'

    def insert_many(self, entity: list):
        insert_entity = []
        for item in entity:
            insert_entity.append(json.loads(json.dumps(item, default=lambda o: o.__dict__)))
        self.db[self.collection_name].insert_many(insert_entity)
        return entity, len(insert_entity), 'insert many success'

    def update_by_id(self, id: tuple, entity: object):
        self.db[self.collection_name].update_one({'_id': ObjectId(id)}, {'$set': json.loads(json.dumps(entity, default=lambda o: o.__dict__))})
        return entity, 1, 'update success'

    def query(self, query, sort):
        sort_key, sort_direction = sort[0], sort[1]
        result = self.db[self.collection_name].find(filter=query).sort(sort_key, sort_direction)
        result_list = []
        for item in result:
            result_list.append(item)
        return result_list, self.db[self.collection_name].count_documents(query), 'query success'

    def query_by_page(self, query, sort, page, page_size):
        sort_key, sort_direction = sort[0], sort[1]
        result = self.db[self.collection_name].find(filter=query).sort(sort_key, sort_direction).skip((page - 1) * page_size).limit(page_size)
        result_list = []
        for item in result:
            result_list.append(item)
        return result_list, self.db[self.collection_name].count_documents(query), 'query by page success'

    def query_by_id(self, id):
        self.db[self.collection_name].find_one({'_id': ObjectId(id)})
        return self.db[self.collection_name].find_one({'_id': ObjectId(id)}), 1, 'query by id success'

    def delete_by_id(self, id):
        self.db[self.collection_name].delete_one({'_id': ObjectId(id)})
        return self.db[self.collection_name].delete_one({'_id': ObjectId(id)}), 1, 'delete by id success'

    def delete_many(self, query):
        count = self.db[self.collection_name].count_documents(query)
        self.db[self.collection_name].delete_many(query)
        return self.db[self.collection_name].delete_many(query), count, 'delete many success'
