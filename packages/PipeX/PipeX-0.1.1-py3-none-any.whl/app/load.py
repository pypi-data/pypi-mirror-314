import pandas as pd
import boto3
from sqlalchemy import create_engine
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file # ? This is not needed in the test_load.py file
load_dotenv()

logger = logging.getLogger(__name__)

def load_data(target: str, config: dict, data: pd.DataFrame):
    if target == "S3 Bucket":
        s3 = boto3.client(
            "s3",
            aws_access_key_id=config['aws_access_key_id'],
            aws_secret_access_key=config['aws_secret_access_key'],
            region_name=config['region_name']
        )
        
        csv_buffer = data.to_csv(index=False)
        bucket_name = config.get('bucket_name')
        file_name = config.get('file_name')
        
        if not bucket_name or not file_name:
            raise KeyError("bucket_name or file_name not found in config")

        s3.put_object(Bucket=bucket_name, Key=file_name, Body=csv_buffer)
        logger.info(f"Data loaded to S3 bucket: {bucket_name}")

    elif target == "database":
        db_type = config.get("db_type")
        if db_type == "mysql":
            engine = create_engine(
                f"mysql+mysqlconnector://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
            )
        elif db_type == "postgres":
            engine = create_engine(
                f"postgresql+psycopg2://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
            )
        else:
            raise ValueError("Database type not supported.")
        
        data.to_sql(config['table_name'], engine, if_exists='replace', index=False)
        logger.info(f"Data loaded to {db_type} database: {config['database']}")

    elif target == "non_relational_database":
        db_type = config.get("db_type")
        if db_type == "mongodb":
            client = MongoClient(
                host=config["host"],
                port=config["port"],
                username=config["username"],
                password=config["password"]
            )
            db = client[config["database"]]
            collection = db[config["collection"]]
            collection.insert_many(data.to_dict("records"))
            logger.info(f"Data loaded to MongoDB collection: {config['collection']}")
            client.close()
        else:
            raise ValueError("Non-relational database type not supported.")

    elif target == "Local File":
        file_type = config.get("file_type")
        if file_type == "csv":
            data.to_csv(config['file_path'], index=False)
            logger.info(f"Data loaded to CSV file: {config['file_path']}")
        elif file_type == "json":
            data.to_json(config['file_path'], orient='records', lines=True)
            logger.info(f"Data loaded to JSON file: {config['file_path']}")
        else:
            raise ValueError("File type not supported.")
    else:
        raise ValueError("Target type not supported.")