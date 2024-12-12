import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup logging configuration for tests
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')