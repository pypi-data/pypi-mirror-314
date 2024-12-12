import typer
import yaml
import pandas as pd
import os
from io import StringIO
from dotenv import load_dotenv
import questionary
from app.load import load_data
from app.extract import extract_data
from app.transform import transform_data
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PipeX.CLI")

app = typer.Typer()

# Helper Functions
def apply_env_variables(config):
    """
    Recursively replace placeholders in the config with environment variables.
    """
    if isinstance(config, dict):
        return {key: apply_env_variables(value) for key, value in config.items()}
    elif isinstance(config, str) and config.startswith("${") and config.endswith("}"):
        env_var = config[2:-1]
        return os.getenv(env_var, config)  # Replace with env value or leave as is
    else:
        return config


def validate_questionary_input(prompt_result, prompt_type="input"):
    """Validate the result of a questionary prompt."""
    if not prompt_result:
        typer.echo(f"{prompt_type.capitalize()} prompt aborted. Exiting.")
        raise typer.Exit()
    return prompt_result

def validate_config(config_data, required_keys):
    """Validate that all required keys are present in the config."""
    for key in required_keys:
        if key not in config_data:
            typer.echo(f"Missing required config key: {key}")
            raise typer.Exit()

    # Check for unresolved placeholders
    for section, content in config_data.items():
        if isinstance(content, dict):
            for sub_key, value in content.items():
                if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                    typer.echo(f"Unresolved placeholder in {section}.{sub_key}: {value}")
                    raise typer.Exit()


# Interactive Prompt Functions
def prompt_for_extraction_method():
    return validate_questionary_input(
        questionary.select(
            "How would you like to extract data?",
            choices=["API", "File", "Database (SQL)", "Database (NoSQL)"]
        ).ask(),
        "extraction method"
    )

def prompt_for_loading_method():
    return validate_questionary_input(
        questionary.select(
            "Where would you like to load the transformed data?",
            choices=["S3 Bucket", "Local File"]
        ).ask(),
        "loading method"
    )

def prompt_for_aws_credentials():
    aws_access_key_id = validate_questionary_input(questionary.text("Enter your AWS Access Key ID:").ask())
    aws_secret_access_key = validate_questionary_input(
        questionary.text("Enter your AWS Secret Access Key:", validate=lambda val: len(val) > 0).ask()
    )
    aws_region = validate_questionary_input(questionary.text("Enter your AWS Region:").ask())
    bucket_name = validate_questionary_input(questionary.text("Enter your S3 Bucket Name:").ask())
    return aws_access_key_id, aws_secret_access_key, aws_region, bucket_name

def prompt_for_transform_script():
    return validate_questionary_input(
        questionary.text("Enter the path to your transformation script (leave blank to use default):").ask(),
        "transformation script"
    )

# CLI Commands
@app.command()
def run(config: str = "config.yaml"):
    """Run the full ETL pipeline."""
    typer.echo(f"Running ETL pipeline with config: {config}")

    # Load and validate config
    try:
        with open(config, 'r') as file:
            config_data = yaml.safe_load(file)
    except yaml.YAMLError as e:
        typer.echo(f"Error parsing config.yaml: {e}")
        raise typer.Exit()

    validate_config(config_data, ['extract', 'transform', 'load'])
    config_data = apply_env_variables(config_data)

    # Extraction
    extraction_method = prompt_for_extraction_method()
    typer.echo(f"Selected extraction method: {extraction_method}")
    extracted_data = extract_data(
        source_type=config_data['extract']['source'],
        connection_details=config_data['extract']['connection_details'],
        query_or_endpoint=config_data['extract']['query_or_endpoint']
    )
    data_json = extracted_data.to_json(orient='split')

    # Transformation
    typer.echo("Transforming data...")
    transform_script = prompt_for_transform_script() or config_data['transform']['script']
    if not os.path.exists(transform_script):
        typer.echo(f"Transformation script not found: {transform_script}")
        raise typer.Exit()

    transformed_data = transform_data(
        script=transform_script,
        config=config_data['transform']['config'],
        data=pd.read_json(StringIO(data_json), orient='split')
    )

    # Loading
    loading_method = prompt_for_loading_method()
    typer.echo(f"Selected loading method: {loading_method}")
    if loading_method == "S3 Bucket":
        aws_access_key_id, aws_secret_access_key, aws_region, bucket_name = prompt_for_aws_credentials()
        config_data['load']['config']['aws_access_key_id'] = aws_access_key_id
        config_data['load']['config']['aws_secret_access_key'] = aws_secret_access_key
        config_data['load']['config']['region_name'] = aws_region
        config_data['load']['config']['bucket_name'] = bucket_name

    load_data(
        target=config_data['load']['target'],
        config=config_data['load']['config'],
        data=transformed_data
    )

    typer.echo("ETL pipeline completed successfully.")

if __name__ == "__main__":
    app()
