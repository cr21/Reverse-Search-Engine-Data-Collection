import pymongo
import os
import certifi

ca =certifi.where()
MONGO_DB_URL_KEY = 'MONGO_DB_URL'
DATABASE_NAME= 'reverse_image_search_engine'

COLLECTION_NAME='embeddings'
MONGO_DB_URL = os.getenv(MONGO_DB_URL_KEY)

class MongoClientConnector:
    clinet= None

    def __init__(self, database_name:str = DATABASE_NAME, database_url:str=MONGO_DB_URL ) -> None:
        self.db_name = database_name
        try:
            if not MongoClientConnector.clinet:
                MongoClientConnector.client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.client = MongoClientConnector.client
            self.database = self.client[self.db_name]
            
        except Exception as exp:
            raise exp("Exception in MongoDb Connection")


    def to_dict(self):
        return self.__dict__



