import os
import yaml
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

def setup_logging(log_level=logging.INFO):
    """Setup logging configuration."""
    logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.info("Logging is set up.")

def load_config(config_path):
    """Load and parse a YAML configuration file."""
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Failed to load configuration from {config_path}: {e}")
        raise

def validate_data(data, schema):
    """Validate data against a schema."""
    from jsonschema import validate, ValidationError
    try:
        validate(instance=data, schema=schema)
        logger.info("Data validation successful.")
    except ValidationError as e:
        logger.error(f"Data validation failed: {e}")
        raise

def get_env_variable(var_name, default=None):
    """Get an environment variable or return a default value."""
    value = os.getenv(var_name, default)
    if value is None:
        logger.warning(f"Environment variable {var_name} is not set.")
    return value

# Example usage:
# setup_logging()
# config = load_config('config.yaml')
# validate_data(data, schema)
# aws_access_key = get_env_variable('AWS_ACCESS_KEY_ID')