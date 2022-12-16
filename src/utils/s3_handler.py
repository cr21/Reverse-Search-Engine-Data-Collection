import boto3
from typing import Dict
from src.utils.utils import get_unique_image_name
import os
import sys
from src.exception import CustomException


class s3Connection:

    def __init__(self) -> None:
        session = boto3.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        self.s3 = session.resource("s3")
        self.bucket = self.s3.Bucket(os.environ["AWS_BUCKET_NAME"])
        

    def add_label(self, label:str) -> Dict:
        """
        This function will add label to s3 bucket 
        param  label : label_name:str
        :return: json response of return state message
        """
        try:
            key=f"images/{label}/"
            response=self.bucket.put_object(Body="",Key=key)
            return {"Created":True, "Path":response.key}
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
            self.bucket.upload_fileobj(
                                        image_path,
                                        f"images/{label}/{get_unique_image_name()}.jpeg",
                                        ExtraArgs={"ACL": "public-read"}
            
            )

            return {"Created":True}

            
        except Exception as exp:
            message = CustomException(exp, sys)
            return {"Created": False, "Reason": message.error_message}