# cf_wrapper_sdk.py

import os
import json
import time
import boto3
import logging
import requests
from typing import Optional, Dict, Any

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Initialize SDK with hardcoded values
BASE_URL = "https://2qo1fh9vhi.execute-api.us-east-1.amazonaws.com/Prod/"
API_AUTH_KEY = "f8b7c2a1-3d6e-4f9a-b5c7-2e8d9a0f1b3c"

class CloudFixSDK:
    def __init__(self):
        """Initialize the SDK with configuration."""
        self.base_url = BASE_URL
        self.headers = {"x-api-key": API_AUTH_KEY}

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'x-api-key': API_AUTH_KEY
        }

    def send_get_request(self, endpoint, params=None):
        """Send GET request to API endpoint."""
        try:
            # Remove any leading/trailing slashes from endpoint and BASE_URL
            endpoint = endpoint.strip('/')
            base_url = self.base_url.rstrip('/')
            
            # For API Gateway, ensure we have the correct path format
            url = f"{base_url}/{endpoint}"
            
            logger.info(f"Sending GET request to: {url}")
            response = requests.get(url, params=params, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending request to {endpoint}: {str(e)}")
            if hasattr(e.response, 'json'):
                try:
                    error_data = e.response.json()
                    return error_data
                except:
                    pass
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

    def list_options(self, option_type: str, limit: Optional[int] = None, offset: Optional[int] = None) -> Dict[str, Any]:
        """List available options (accounts, regions, services, finders)."""
        try:
            params = {}
            if limit is not None:
                params['limit'] = limit
            if offset is not None:
                params['offset'] = offset
            
            # Include option_type in the path instead of as a query parameter
            endpoint = f"list/{option_type}"
            return self.send_get_request(endpoint, params)
        except Exception as e:
            logger.error(f"Error listing {option_type}: {str(e)}")
            return {}

    def list_options_original(self, option_type, limit=100, offset=0):
        """Original list options implementation."""
        params = {
            'limit': limit,
            'offset': offset
        }
        response = requests.get(f"{self.base_url}list/{option_type}", headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

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