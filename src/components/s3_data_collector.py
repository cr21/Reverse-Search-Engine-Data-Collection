import os
import shutil
from zipfile import ZipFile
import sys
from src.exception import CustomException
from src.logger import logging





# https://www.kaggle.com/datasets/imbikramsaha/caltech-101 [ Get data from kaggle and put it into data folder ]


class S3Collector:

    def __init__(self):
        self.root_dir = os.path.join(os.getcwd(),'data')
        self.zip_file = os.path.join(self.root_dir,'archive.zip')
        self.images_dir = os.path.join(self.root_dir, 'caltech-101')
        # background images added by google we want to avoid it
        self.list_unwanted = ["BACKGROUND_Google"]

    def prepare_data(self):
        # prepare root dir
        try:

            os.makedirs(self.root_dir, exist_ok=True)
            logging.info("Extracting Zip file")
            with ZipFile(self.zip_file,'r') as files:
                print("hi")
                files.extractall(path=self.root_dir)
            
            files.close()
            logging.info("Data Extraction Process Finished")

            
        except Exception as exp:

            message = CustomException(exp, sys)
            logging.info(f"Data Collection Prepare Data  Process 1 Exception : {message}")
            return {"Created": False, "Reason": message.error_message}
    

    def remove_unwanted_classes(self):
        try:
            logging.info("Removing unwanted classes")
            for label in self.list_unwanted:
                path = os.path.join(self.images_dir, label)
                shutil.rmtree(path=path, ignore_errors=True)
            logging.info("Process finished removed unwanted classes")


        except Exception as exp:
            message = CustomException(exp, sys)
            logging.info(f"Data Collection Process  2 Exception : {message}")
            return {"Created": False, "Reason": message.error_message}

    def sync_data(self):
        logging.info("+++++++++++++ SYNC PROCESS STARTED ++++++++++++++++")
        os.system(f"aws s3 sync { self.images_dir }  s3://cr-img-search-engine/images/ ")
        logging.info("+++++++++++++ SYNC PROCESS FINISHED ++++++++++++++++")


    def run_step(self):
        try:

            self.prepare_data()
            self.remove_unwanted_classes()
            self.sync_data()
            return True
        except Exception as exp:
            message = CustomException(exp, sys)
            logging.info(f"Data Collection Process Exception : {message}")
            return {"Created": False, "Reason": message.error_message}

            


if __name__ == "__main__":
    s3_collector = S3Collector()
    s3_collector.run_step()