import pytest
import pandas as pd
from app.transform import transform_data

def test_transform_data(mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data='def transform(data): data["column3"] = data["column1"] * 2; return data'))
    
    data = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
    config = {
        'drop_columns': ['column2'],
        'rename_columns': {'column1': 'new_column1'},
        'filter_rows': 'new_column1 > 1',
        'add_columns': {'column4': 'data["new_column1"] + 10'}
    }
    options = {
        'drop_columns': True,
        'rename_columns': False,
        'filter_rows': True,
        'add_columns': True
    }
    
    transformed_data = transform_data('tests/transform_script.py', config, data, options)
    
    expected_data = pd.DataFrame({
        'new_column1': [2, 3],
        'column3': [4, 6],
        'column4': [12, 13]
    })
    
    pd.testing.assert_frame_equal(transformed_data, expected_data)