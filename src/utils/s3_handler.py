import boto3
from typing import Dict
from src.utils.utils import get_unique_image_name
import os
import io
import sys
from src.exception import CustomException
#s3 connections1
class s3Connection:

    def __init__(self) -> None:
        # session = boto3.Session(
        #     aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        #     aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        # )
        # self.s3 = session.resource("s3")

        self.s3 = boto3.client('s3')
        self.bucket = os.getenv('AWS_BUCKET_NAME')
        #self.bucket = self.s3.Bucket('cr-img-search-engine')
        #self.bucket = self.s3.Bucket(os.getenv("AWS_BUCKET_NAME"))
        

    def add_label(self, label:str) -> Dict:
        """
        This function will add label to s3 bucket 
        param  label : label_name:str
        :return: json response of return state message
        """
        try:
            key=f"images/{label}/"
            response=self.s3.put_object(Bucket=self.bucket,Body="",Key=key)
            
            get_res = self.s3.get_object(Bucket=self.bucket,Key=key)
            
            return {"Created":True}
        except Exception as exp:
            message = CustomException(exp, sys)
            return {"Created": False, "Reason": message.error_message}

    def upload_to_s3(self,image_path,label):
        """
        Upload file object to in predefined label directory
        param label: label Name
        :param image_path: Path to the image to upload
        :return: json Response of state message (success or failure) 
        """
        try:

            # fo = io.BytesIO(b'my data stored as file object in RAM')
            # client.upload_fileobj(fo, bucket, key)

            self.s3.upload_fileobj(image_path, self.bucket, f"images/{label}/{get_unique_image_name()}.jpeg")
        
            # self.bucket.upload_fileobj(
            #                             image_path,
            #                             f"images/{label}/{get_unique_image_name()}.jpeg",
            #                             ExtraArgs={"ACL": "public-read"}
            
            # )
            
            return {"Created":True}

            
        except Exception as exp:
            message = CustomException(exp, sys)
            return {"Created": False, "Reason": message.error_message}