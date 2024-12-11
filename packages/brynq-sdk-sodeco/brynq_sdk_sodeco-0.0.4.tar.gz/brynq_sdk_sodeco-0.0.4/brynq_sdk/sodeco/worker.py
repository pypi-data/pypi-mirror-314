from datetime import datetime
import pandas as pd
import warnings
from .schemas.worker import WorkerSchema
from .schemas import DATEFORMAT
from .address import Address
from .communication import Communication
from .contract import Contract
from .family import Family
from .tax import Tax
from brynq_sdk.functions import Functions
from .base import SodecoBase
from typing import Optional


class Worker(SodecoBase):
    def __init__(self, sodeco):
        super().__init__(sodeco)
        self.contract = Contract(sodeco)
        self.address = Address(sodeco)
        self.communication = Communication(sodeco)
        self.family = Family(sodeco)
        self.tax = Tax(sodeco)
        self.url = f"{self.sodeco.base_url}worker"

    def get(self, worker_id: Optional[str] = None, start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
        """
        Get worker information, optionally filtered by worker_id and date range.
        
        Args:
            worker_id: Optional worker ID to get specific worker
            start_date: Start date for filtering workers
            end_date: End date for filtering workers (required if start_date is provided)
            
        Returns:
            pd.DataFrame: DataFrame containing worker information
            
        Raises:
            ValueError: If start_date is provided without end_date
        """
        url = self.url
        if worker_id is not None:
            url += f"/{worker_id}"
        if start_date is not None:
            if end_date is not None:
                url += f"/{start_date.strftime(DATEFORMAT)}/{end_date.strftime(DATEFORMAT)}"
            else:
                raise ValueError("if start_date is specified, end_date must be specified as well")

        data = self._make_request_with_polling(url, params={"limit": 100})
        employee = pd.DataFrame(data)
        employee = self._rename_camel_columns_to_snake_case(employee)
        addresses = pd.json_normalize(data,
                                      record_path='address',
                                      meta=['WorkerNumber']
                                      )
        addresses = self._rename_camel_columns_to_snake_case(addresses)
        family = pd.json_normalize(data,
                                         record_path='FamilyStatus',
                                         meta=['WorkerNumber']
                                         )
        family = self._rename_camel_columns_to_snake_case(family)
        communication = pd.json_normalize(data,
                                          record_path='Communication',
                                          meta=['WorkerNumber']
                                          )
        communication = self._rename_camel_columns_to_snake_case(communication)
        contract = pd.json_normalize(data,
                                     record_path='contract',
                                     meta=['WorkerNumber']
                                     )
        contract = self._rename_camel_columns_to_snake_case(contract)
        tax = pd.json_normalize(data,
                                record_path='Tax',
                                meta=['WorkerNumber']
                                )
        tax = self._rename_camel_columns_to_snake_case(tax)
        replacement = pd.json_normalize(data,
                                        record_path='Replacement',
                                        meta=['WorkerNumber']
                                        )
        replacement = self._rename_camel_columns_to_snake_case(replacement)

        return employee, family, addresses, communication, contract, tax, replacement

    def create(self, payload: dict, debug: bool = False) -> dict:
        """
        Create a worker based on the given payload.
        The payload must adhere to the structure defined by the WorkerSchema.
        
        Args:
            payload: The worker data to create
            debug: If True, prints detailed validation errors
            
        Returns:
            dict: The created worker data
            
        Raises:
            ValueError: If the payload is invalid
        """
        # Convert payload to DataFrame and validate
        df = pd.DataFrame([payload])
        valid_data, invalid_data = Functions.validate_data(df, WorkerSchema, debug=debug)

        if len(invalid_data) > 0:
            error_msg = "Invalid worker payload"
            if debug:
                error_msg += f": {invalid_data.to_dict(orient='records')}"
            raise ValueError(error_msg)

        # Send the POST request to create the worker
        data = self._make_request_with_polling(
            self.url,
            method='POST',
            json=valid_data.iloc[0].to_dict()
        )
        return data

    def update(self, worker_id: str, payload: dict, debug: bool = False) -> dict:
        """
        Update a worker based on the given payload.
        The payload must adhere to the structure defined by the WorkerSchema.
        
        Args:
            worker_id: The ID of the worker to update
            payload: The worker data to update
            debug: If True, prints detailed validation errors
            
        Returns:
            dict: The updated worker data
            
        Raises:
            ValueError: If the payload is invalid
        """
        # Convert payload to DataFrame and validate
        df = pd.DataFrame([payload])
        valid_data, invalid_data = Functions.validate_data(df, WorkerSchema, debug=debug)

        if len(invalid_data) > 0:
            error_msg = "Invalid worker payload"
            if debug:
                error_msg += f": {invalid_data.to_dict(orient='records')}"
            raise ValueError(error_msg)

        # Send the PUT request to update the worker
        url = f"{self.url}/{worker_id}"
        data = self._make_request_with_polling(
            url,
            method='PUT',
            json=valid_data.iloc[0].to_dict()
        )
        return data
