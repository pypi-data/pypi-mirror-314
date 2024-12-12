import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Import submodules
from .extract import extract_data
from .transform import transform_data
from .load import load_data
from .storage import save_to_file, upload_to_s3, download_from_s3, file_exists_in_s3, save_data
from .api import APIClient
from .utils import setup_logging, load_config, validate_data, get_env_variable

__all__ = [
    'extract_data',
    'transform_data',
    'load_data',
    'save_to_file',
    'upload_to_s3',
    'download_from_s3',
    'file_exists_in_s3',
    'save_data',
    'APIClient',
    'setup_logging',
    'load_config',
    'validate_data',
    'get_env_variable'
]