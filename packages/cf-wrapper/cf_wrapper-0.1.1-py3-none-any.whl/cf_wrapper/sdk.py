# cf_wrapper_sdk.py

import os
import json
import time
import boto3
import logging
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Get base URL from environment variable
BASE_URL = ""

# Get API auth key from environment
API_AUTH_KEY = "f8b7c2a1-3d6e-4f9a-b5c7-2e8d9a0f1b3c"
if not API_AUTH_KEY:
    raise ValueError("API_AUTH_KEY environment variable is not set")

class CloudFixSDK:
    def __init__(self):
        self.api_url = BASE_URL
        self.api_key = API_AUTH_KEY
        if not self.api_url:
            raise ValueError("BASE_URL environment variable is not set")
        if not self.api_key:
            raise ValueError("API_AUTH_KEY environment variable is not set")

    def _get_headers(self):
        return {
            'x-api-auth': self.api_key,
            'x-api-key': self.api_key
        }

    def send_get_request(self, endpoint, params=None):
        """
        Sends a GET request to the specified endpoint with query parameters.
        """
        # Remove any leading/trailing slashes from endpoint and BASE_URL
        endpoint = endpoint.strip('/')
        base_url = self.api_url.rstrip('/')
        
        # For Lambda Function URL, ensure we have the correct path format
        if 'lambda-url' in base_url:
            url = f"{base_url}/{endpoint}"
        else:
            # For API Gateway, we don't need to add a slash
            url = f"{base_url}{endpoint}"
        
        try:
            logger.info(f"Sending request to: {url}")
            logger.info(f"Headers: {self._get_headers()}")
            logger.info(f"Params: {params}")
            response = requests.get(url, params=params, headers=self._get_headers())
            if response.status_code != 200:
                logger.error(f"Error response: {response.text}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request Error: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response content: {e.response.text}")
            return {"error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {"error": str(e)}

    def log_results(self, results):
        """
        Logs the JSON results in a formatted manner.
        """
        if isinstance(results, dict) and 'error' in results:
            logger.error(f"Error in results: {results['error']}")
            if 'details' in results:
                logger.error(f"Details: {results['details']}")
            return

        if not results:
            logger.warning("No results to display")
            return

        try:
            logger.info(json.dumps(results, indent=2))
        except Exception as e:
            logger.error(f"Error formatting results: {str(e)}")
            logger.debug(f"Raw results: {results}")

    def describe_table(self, table_name):
        """
        Fetches the structure of a specified table.
        Returns a list of dictionaries containing column information.
        """
        start_time = time.time()
        try:
            results = self.send_get_request(f"describe/{table_name}")
            end_time = time.time()
            logger.info(f"Query took {end_time - start_time:.2f} seconds")
            
            if isinstance(results, dict) and 'error' in results:
                logger.error(f"Error describing table: {results['error']}")
                return results
                
            return results
        except Exception as e:
            logger.error(f"Error describing table: {str(e)}")
            return {"error": str(e)}

    def list_options(self, option_type, limit=100, offset=0):
        """
        List available options (accounts, regions, services, finders).
        """
        try:
            params = {
                'limit': limit,
                'offset': offset
            }
            results = self.send_get_request(f"list/{option_type}", params)
            self.log_results(results)
            return results
        except Exception as e:
            logger.error(f"Error listing options: {str(e)}")
            return {"error": str(e)}

    def get_records(self, account=None, region=None, service=None, finder=None, limit=100, offset=0):
        """
        Get records filtered by account, region, service, and/or finder.
        """
        try:
            params = {
                'limit': limit,
                'offset': offset
            }
            if account:
                params['account'] = account
            if region:
                params['region'] = region
            if service:
                params['service'] = service
            if finder:
                params['finder'] = finder
                
            results = self.send_get_request("get", params)
            self.log_results(results)
            return results
        except Exception as e:
            logger.error(f"Error getting records: {str(e)}")
            return {"error": str(e)}

sdk = CloudFixSDK()

# End of cf_wrapper_sdk.py