from src.utils.database_handler import MongoClientConnector
from src.logger import logging
from src.exception import CustomException
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List, Union, Any
import os
import io
import sys
from src.utils.s3_handler import s3Connection

import uvicorn

app = FastAPI(title="Image Data Collection Server")
mongo_client = MongoClientConnector()
s3_connection =  s3Connection()

choices = {}

@app.get("/")
def run():
    return {"dummy"}
# Fetch All Labels

@app.get("/fetch")
def fetch_label():
    try:
        global choices
        print("mongo_client",mongo_client.database)
        print("*"*100)
        result = mongo_client.database['labels'].find()
        print(result)
        if result:
            print(result)
            print("*"*300)
        documents = []
        for id,doc in enumerate(result):
            documents.append(doc)
            print(id,doc)
        print(len(documents))
        print("**")
        choices = dict(documents[0])
        response = {"Status": "Success", "Response": str(documents[0])}
        return JSONResponse(content=response, status_code=200, media_type="application/json")

        
    except Exception as e:
        return {"status":"Fail"}

@app.post("/add_label/{label_name}")
def add_label(label_name:str):
    """
    If label is not present in Mongodb meta store then add it 
    And create corosponding bucket folder in s3 as well
    
    """
    query_result = mongo_client.database['labels'].find()
    all_doc = [doc for doc in query_result]
    last_val = list(map(int, list(all_doc[0].keys())[1:]))[-1]
    response = mongo_client.database['labels'].update_one(
                                                            {"_id":all_doc[0]["_id"]},
                                                            {"$set":{str(last_val+1):label_name}}
                                             )
                
    if response.modified_count == 1:
        response = s3_connection.add_label(label_name)
        return {"status":"Success", "s3-response":response}
    else:
        return {"status":"Fail", "message":response[1]}



@app.get("/single_upload/")
def single_upload():
    info = {"Response": "Available", "Post-Request-Body": ["label", "Files"]}
    return JSONResponse(content=info, status_code=200, media_type="application/json")


@app.post("/single_upload/")
async def single_upload(label: str, file: UploadFile = None):
    # print(type(file.file))
    # import io
    # ffff= io.BytesIO(file.file)
    # print(type(ffff))
    # print(1/0)
    # return {"file":type(file.file)}
    label = choices.get(label, False)
    #print(label)
    if file.content_type == "image/jpeg" and label != False:
        contents = await file.read()
        #print(contents)
        temp_file = io.BytesIO()
        temp_file.write(contents)
        temp_file.seek(0)
        
        
        response = s3_connection.upload_to_s3(temp_file, label)
        temp_file.close()
        return {"filename": file.filename, "label": label, "S3-Response": response}
    else:
        return {
            "ContentType": f"Content type should be Image/jpeg not {file.content_type}",
            "LabelFound": label
        }



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)