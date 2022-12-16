import os
import sys
from src.utils.database_handler import MongoClientConnector
from src.logger import logging
from src.exception import CustomException

class MongoMetaDataStore:

    def __init__(self):
        self.root_dir = os.path.join(os.getcwd(),'data')
        self.images_dir = os.path.join(self.root_dir, 'caltech-101')
        self.labels = os.listdir(self.images_dir)
        self.mongo_client = MongoClientConnector()

    def register_labels(self):
        """
        Register Image Label meta data to mongodb 
        This will be use ful to keep track of what all labels we are using and can modify according to future needs
        
        """
        try:
            records = {}

            for num, label in enumerate(self.labels):
                records[f"{num}"] = label
            self.mongo_client.database['labels'].insert_one(records)
            
        except Exception as exp:
            message = CustomException(exp, sys)
            return {"Created":False, "Reason":message.error_message}


    def run_step(self):
        try:
            self.register_labels()
        except Exception as exp:
            message = CustomException(exp, sys)
            return {"Created":False, "Reason":message.error_message}



if __name__ == "__main__":
    mongo_meta_store = MongoMetaDataStore()
    mongo_meta_store.run_step()