from datetime import datetime
from .schemas import DATEFORMAT
from .base import SodecoBase
from typing import Optional
import pandas as pd


class Dimona(SodecoBase):
    """Class to handle the dimona endpoint for workers."""
    
    def __init__(self, sodeco):
        super().__init__(sodeco)

    def get(self, worker_id: str, start_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Get dimona data for a worker.
        
        Args:
            worker_id (str): The ID of the worker
            start_date (datetime, optional): The start date to retrieve dimona data from
            
        Returns:
            pd.DataFrame: The dimona data
        """
        if start_date:
            url = f"{self.sodeco.base_url}/worker/{worker_id}/dimona/{start_date.strftime(DATEFORMAT)}"
        else:
            url = f"{self.sodeco.base_url}/worker/{worker_id}/dimona"
            
        data = self._make_request_with_polling(url)
        return pd.DataFrame(data)
