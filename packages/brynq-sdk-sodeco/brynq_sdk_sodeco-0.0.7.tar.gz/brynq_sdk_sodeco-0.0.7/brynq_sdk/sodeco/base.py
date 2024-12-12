import logging
import time
import pandas as pd
from typing import Any, Dict, Optional, List, Union
import json
import re
import requests
logging.basicConfig(level=logging.INFO, format='%(message)s')


class SodecoBase:
    """Base class for Sodeco API endpoints."""

    def __init__(self, sodeco):
        self.sodeco = sodeco
        self.max_attempts = 25
        self.poll_interval = 5  # seconds

    def _make_request_with_polling(self, url: str, method: str = 'GET', headers: Optional[Dict] = None, **kwargs) -> Any:
        """
        Make a request and poll for results for each employer.
        
        This method handles the following status codes:
        - 200: Success, data is returned
        - 202: Request accepted, still processing
        - 204: No Content, endpoint exists but no data found
        
        For each employer in the list:
        1. Updates headers with employer information
        2. Makes initial request to get GUID
        3. Polls result endpoint until data is ready (200) or no data found (204)
        4. Adds employer information to each record
        
        Args:
            url: The URL to make the initial request to
            method: HTTP method to use (default: 'GET')
            headers: Additional headers to include in the request
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            list: List of dictionaries containing data from all employers. Each record includes
                 an 'employer' field. Returns empty list if no data found (status 204).
            
        Raises:
            requests.exceptions.HTTPError: If any request fails
        """
        all_data = []
        employers = [self.sodeco.employers] if isinstance(self.sodeco.employers, str) else self.sodeco.employers
        
        for employer in employers:
            self.sodeco.update_headers(employer)
            
            if headers:
                self.sodeco.session.headers.update(headers)

            response = self.sodeco.session.request(
                method=method,
                url=url,
                **kwargs
            )
            response.raise_for_status()
            guid = response.json()

            while True:
                poll_url = f"{self.sodeco.base_url}result/{guid}"
                poll_response = self.sodeco.session.get(poll_url)
                poll_response.raise_for_status()
                result = poll_response.json()
                status = result.get("Statuscode")
                
                if status == "204":
                    logging.info(f"No data found for employer {employer}")
                    break
                elif status == "200":
                    result_data = json.loads(result.get("Response"))
                    record_count = len(result_data)
                    logging.info(f"Received {record_count} records for employer {employer}")
                    all_data.extend([{**record, 'employer': employer} for record in result_data])
                    break
                elif status == "202" or status == "302":
                    logging.info(f"Request still processing for employer {employer}, waiting {self.poll_interval} seconds...")
                    time.sleep(self.poll_interval)
                else:
                    error_msg = f"Unexpected status code: {status}"
                    logging.error(error_msg)
                    raise ValueError(error_msg)
                    
        total_records = len(all_data)
        logging.info(f"Completed processing all employers. Total records: {total_records}")

        return all_data

    def _rename_camel_columns_to_snake_case(self, df: pd.DataFrame) -> pd.DataFrame:
        def camel_to_snake_case(column):
            # Replace periods with underscores
            column = column.replace('.', '_')
            # Insert underscores before capital letters and convert to lowercase
            return re.sub(r'(?<!^)(?=[A-Z])', '_', column).lower()
            
        df.columns = map(camel_to_snake_case, df.columns)
        return df