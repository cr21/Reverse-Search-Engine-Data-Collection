# from src.utils.database_handler import MongoClientConnector, COLLECTION_NAME


# client  = MongoClientConnector()
# print(client.database[COLLECTION_NAME])


from src.components.s3_data_collector import S3Collector

s3_client  =S3Collector()
s3_client.run_step()