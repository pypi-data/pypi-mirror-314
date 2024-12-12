from datetime import datetime
from typing import Optional
import pandas as pd
from .base import SodecoBase
from .schemas import DATEFORMAT


class Car(SodecoBase):

    def __init__(self, sodeco):
        super().__init__(sodeco)

    def get(self, worker_id: Optional[str] = None, start_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Get company car information, optionally filtered by worker_id and/or start_date.
        
        Args:
            worker_id: Optional worker ID to get company cars for a specific worker
            start_date: Optional start date to get car information from a specific date (car Id)
            
        Returns:
            pd.DataFrame: DataFrame containing the company car information
        """
        if worker_id is not None:
            url = f"{self.sodeco.base_url}worker/{worker_id}/companycar"
        else:
            url = f"{self.sodeco.base_url}companycar"

        if start_date is not None:
            url += f"/{start_date.strftime(DATEFORMAT)}"

        data = self._make_request_with_polling(url)
        return pd.DataFrame(data)
