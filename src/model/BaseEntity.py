class BaseEntity(object):
    collection_name = ''
    def __init__(self, collection_name):
        self.collection_name = collection_name
    @property
    def get_collection_name(self):
        return self.__class__.__name__
