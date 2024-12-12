import pytest
from app.extract import extract_data

def test_extract_data_from_api(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = [{"key": "value"}]
    mocker.patch("requests.get", return_value=mock_response)
    
    data = extract_data(
        source_type="api",
        connection_details={"headers": {"Authorization": "Bearer YOUR_API_KEY"}},
        query_or_endpoint="http://127.0.0.1:5000/data"
    )
    
    assert data.to_dict(orient='records') == [{"key": "value"}]

def test_extract_data_from_csv(mocker):
    mocker.patch("pandas.read_csv", return_value="csv_data")
    
    data = extract_data(
        source_type="file",
        connection_details={"file_type": "csv"},
        query_or_endpoint="path/to/your/file.csv"
    )
    
    assert data == "csv_data"