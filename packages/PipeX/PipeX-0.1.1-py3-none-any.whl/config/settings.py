import os
from dotenv import load_dotenv
import yaml

# Load environment variables from .env file
load_dotenv()

def load_config(config_path):
    """Load and parse a YAML configuration file."""
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        raise RuntimeError(f"Failed to load configuration from {config_path}: {e}")

# Example usage:
# config = load_config('config.yaml')

# Environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
BUCKET_NAME = os.getenv('BUCKET_NAME')

# Example usage:
# print(AWS_ACCESS_KEY_ID)