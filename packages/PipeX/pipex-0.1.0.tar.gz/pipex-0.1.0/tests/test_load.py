import pytest
import pandas as pd
from app.load import load_data

def test_load_data_to_csv(mocker):
    mocker.patch("pandas.DataFrame.to_csv")
    
    data = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
    load_data(
        target="Local File",
        config={'file_type': 'csv', 'file_path': 'app/data.csv'},
        data=data
    )
    
    pd.DataFrame.to_csv.assert_called_once_with('app/data.csv', index=False)

def test_load_data_to_s3(mocker):
    mock_s3 = mocker.Mock()
    mocker.patch("boto3.client", return_value=mock_s3)
    
    data = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
    load_data(
        target="S3 Bucket",
        config={
            'aws_access_key_id': 'YOUR_ACCESS_KEY',
            'aws_secret_access_key': 'YOUR_SECRET_KEY',
            'region_name': 'us-west-2',
            'bucket_name': 'your-bucket-name',
            'file_name': 'data.csv'
        },
        data=data
    )
    
    mock_s3.put_object.assert_called_once_with(
        Bucket='your-bucket-name',
        Key='data.csv',
        Body=mocker.ANY
    )

def test_load_data_to_mysql(mocker):
    mock_engine = mocker.Mock()
    mocker.patch("sqlalchemy.create_engine", return_value=mock_engine)
    
    data = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
    load_data(
        target="database",
        config={
            'db_type': 'mysql',
            'host': 'localhost',
            'username': 'root',
            'password': 'password',
            'port': 3306,
            'database': 'mydatabase',
            'table_name': 'mytable'
        },
        data=data
    )
    
    data.to_sql.assert_called_once_with('mytable', mock_engine, if_exists='replace', index=False)