import os
from dotenv import load_dotenv


class BaseConfig:
    load_dotenv()
    DEBUG = False
    TESTING = False
    MONGO_URI = os.getenv('MONGO_URI')
    MONGO_DB=os.getenv('MONGO_DB')
    MONGO_DB_COLLECTION=os.getenv('MONGO_DB_COLLECTION')

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class TestingConfig(DevelopmentConfig):
    TESTING = True

class ProductionConfig(DevelopmentConfig):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
