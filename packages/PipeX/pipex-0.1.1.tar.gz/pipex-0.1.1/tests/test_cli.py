import pytest
from typer.testing import CliRunner
from app.cli import app

runner = CliRunner()

def test_extract(mocker):
    mocker.patch("app.extract.extract_data", return_value={"data": "extracted"})
    result = runner.invoke(app, ["extract", "api", "app/config.yaml"])
    assert result.exit_code == 0
    assert "Data extraction complete." in result.output

def test_transform(mocker):
    mocker.patch("app.transform.transform_data", return_value={"data": "transformed"})
    result = runner.invoke(app, ["transform", "test/stransform_script.py", "app/config.yaml", '{"data": "extracted"}'])
    assert result.exit_code == 0
    assert "Data transformation complete." in result.output

def test_load(mocker):
    mocker.patch("app.load.load_data")
    result = runner.invoke(app, ["load", "s3", "app/config.yaml", '{"data": "transformed"}'])
    assert result.exit_code == 0
    assert "Data loading complete." in result.output

def test_run(mocker):
    mocker.patch("app.extract.extract_data", return_value={"data": "extracted"})
    mocker.patch("app.transform.transform_data", return_value={"data": "transformed"})
    mocker.patch("app.load.load_data")
    result = runner.invoke(app, ["run", "--config", "app/config.yaml"])
    assert result.exit_code == 0
    assert "Running ETL pipeline with config: app/config.yaml" in result.output
    assert "Data extraction complete." in result.output
    assert "Data transformation complete." in result.output
    assert "Data loading complete." in result.output