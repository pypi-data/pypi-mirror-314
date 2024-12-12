from datetime import datetime
import pandas as pd
import warnings
from .costcentres import CostCentres
from .dimona import Dimona
from .replacement import Replacement
from .car import Car
from .schemas.worker import WorkerSchema
from .schemas import DATEFORMAT
from .address import Address
from .communication import Communication
from .contract import Contracts
from .family import Family
from .tax import Tax
from brynq_sdk.functions import Functions
from .base import SodecoBase
from typing import Optional
from .divergentsalary import DivergentSalaryScale
from .absencenote import AbsenceNote
from .divergentpayment import DivergentPayment
from .leavecounters import LeaveCounters


class Workers(SodecoBase):
    def __init__(self, sodeco):
        super().__init__(sodeco)
        self.url = f"{self.sodeco.base_url}worker"
        self.addresses = Address(sodeco)
        self.communications = Communication(sodeco)
        self.contracts = Contracts(sodeco)
        self.costcentres = CostCentres(sodeco)
        self.families = Family(sodeco)
        self.taxes = Tax(sodeco)
        self.cars = Car(sodeco)
        self.dimonas = Dimona(sodeco)
        self.divergentsalaries = DivergentSalaryScale(sodeco)
        self.replacements = Replacement(sodeco)
        self.absencenotes = AbsenceNote(sodeco)
        self.divergentpayments = DivergentPayment(sodeco)
        self.leavecounters = LeaveCounters(sodeco)

    def get(self, worker_id: Optional[str] = None, start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
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

        limit = 100
        offset = 0
        all_data = []
        
        while True:
            batch_data = self._make_request_with_polling(url, params={"limit": limit, "offset": offset})
            all_data.extend(batch_data)
            
            # If we got fewer results than the limit, we've reached the end
            if len(batch_data) < limit:
                break
                
            # Increment offset for next batch
            offset += limit

        employee = pd.DataFrame(all_data)
        employee = employee.drop(columns=['FamilyStatus', 'address', 'Communication', 'contract', 'Tax', 'Replacement'])
        employee = self._rename_camel_columns_to_snake_case(employee)
        addresses = pd.json_normalize(all_data,
                                      record_path='address',
                                      meta=['WorkerNumber']
                                      )
        addresses = self._rename_camel_columns_to_snake_case(addresses)
        family = pd.json_normalize(all_data,
                                   record_path='FamilyStatus',
                                   meta=['WorkerNumber']
                                   )
        family = self._rename_camel_columns_to_snake_case(family)
        communication = pd.json_normalize(all_data,
                                          record_path='Communication',
                                          meta=['WorkerNumber']
                                          )
        communication = self._rename_camel_columns_to_snake_case(communication)
        contract = pd.json_normalize(all_data,
                                     record_path='contract',
                                     meta=['WorkerNumber']
                                     )
        salary_compositions = pd.json_normalize(all_data,
                                     record_path=['contract', 'SalaryCompositions'],
                                     meta=['WorkerNumber']
                                     )
        salary_compositions = self._rename_camel_columns_to_snake_case(salary_compositions)
        contract = self._rename_camel_columns_to_snake_case(contract)
        contract = contract.drop(columns=['salary_compositions'])
        tax = pd.json_normalize(all_data,
                                record_path='Tax',
                                meta=['WorkerNumber']
                                )
        tax = self._rename_camel_columns_to_snake_case(tax)
        replacement = pd.json_normalize(all_data,
                                        record_path='Replacement',
                                        meta=['WorkerNumber']
                                        )
        replacement = self._rename_camel_columns_to_snake_case(replacement)

        return employee, family, addresses, communication, contract, tax, replacement, salary_compositions

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
