import pymongo
import os

# MONGO_DB_URL_KEY = 'MONGO_DB_URL'
DATABASE_NAME= 'reverse_image_search_engine'
# MONGO_DB_URL = os.getenv(MONGO_DB_URL_KEY)


class MongoClientConnector:
    clinet= None

    def __init__(self, database_name:str = os.environ['DATABASE_NAME'] ) -> None:
        
        try:
            if  MongoClientConnector.clinet is None:
                mongo_url = f"mongodb+srv://{os.environ['ATLAS_CLUSTER_USERNAME']}:{os.environ['ATLAS_CLUSTER_PASSWORD']}@cluster0.ufj8ovv.mongodb.net/?retryWrites=true&w=majority"
               
                MongoClientConnector.client = pymongo.MongoClient(
                        mongo_url
                )
                print("mongoURL", mongo_url)
            self.client = MongoClientConnector.client
            self.database = self.client[database_name]
            self.db_name = database_name
            
            
        except Exception as exp:
            raise exp("Exception in MongoDb Connection")


    def to_dict(self):
        return self.__dict__



