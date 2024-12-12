"""
api.py will have :
- APIClient class
- get method
- post method
- get_with_auth method

this module is needed for:
- making http requests
- handling http errors
- handling http retries
- handling http timeouts
- handling http caching
- handling http authentication
- handling http headers

"""

import requests
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from cachetools import cached, TTLCache

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url, headers=None, cache_enabled=True):
        self.base_url = base_url
        self.headers = headers
        self.session = requests.Session()
        self.session.headers.update(headers or {})
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[504, 500, 502, 429, 503])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        self.cache = TTLCache(maxsize=100, ttl=300)
        self.cache_enabled = cache_enabled

    @cached(cache=lambda self: self.cache)
    def get(self, endpoint, params=None, timeout=10):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Making GET request to {url}")
        try:
            response = self.session.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error occurred: {e}")
            raise
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout error occurred: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred: {e}")
            raise

    def post(self, endpoint, data=None, timeout=10):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Making POST request to {url}")
        try:
            response = self.session.post(url, json=data, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error occurred: {e}")
            raise
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout error occurred: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred: {e}")
            raise

    def get_with_auth(self, endpoint, token, params=None, timeout=10):
        headers = {
            "Authorization": f"Bearer {token}"
        }
        self.session.headers.update(headers)
        return self.get(endpoint, params=params, timeout=timeout)

# Example usage:
# client = APIClient("http://127.0.0.1:5000")
# data = client.get("/data")
# data_with_auth = client.get_with_auth("/data", "your_token")
# response = client.post("/data", data={"key": "value"})