import time
import pandas as pd
from typing import Any, Dict, Optional
import json
import re


class SodecoBase:
    def __init__(self, sodeco):
        self.sodeco = sodeco
        self.max_attempts = 10
        self.poll_interval = 2  # seconds

    def _make_request_with_polling(self, url: str, method: str = 'GET', headers: Optional[Dict] = None, **kwargs) -> Any:
        """
        Make a request and poll for results using the GUID-based system.
        
        Args:
            url: The URL to make the initial request to
            method: HTTP method to use (default: 'GET')
            headers: Additional headers to include in the request
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            The final response data after polling is complete
        """
        # Merge headers with base headers if provided
        if headers:
            self.sodeco.session.headers.update(headers)

        # Initial request to get GUID
        response = self.sodeco.session.request(
            method=method,
            url=url,
            **kwargs
        )
        response.raise_for_status()
        
        # Get GUID from response
        guid = response.json()

        # Start polling
        finished = False
        attempt = 0
        
        while not finished and attempt < self.max_attempts:
            poll_url = f"{self.sodeco.base_url}result/{guid}"
            poll_response = self.sodeco.session.get(poll_url)
            poll_response.raise_for_status()
            
            result = poll_response.json()
            
            # Check if the request is finished
            if result.get("Statuscode") == "200":
                result_dict = result.get("Response")
                return json.loads(result_dict) # Return the actual result data
                
            # Wait before next attempt
            time.sleep(self.poll_interval)
            attempt += 1
            
        raise TimeoutError(f"Request polling timed out after {self.max_attempts} attempts")

    def _rename_camel_columns_to_snake_case(self, df: pd.DataFrame) -> pd.DataFrame:
        def camel_to_snake_case(column):
            # Replace periods with underscores
            column = column.replace('.', '_')
            # Insert underscores before capital letters and convert to lowercase
            return re.sub(r'(?<!^)(?=[A-Z])', '_', column).lower()

        df.columns = map(camel_to_snake_case, df.columns)

        return df