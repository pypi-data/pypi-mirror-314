from datetime import datetime
from typing import Optional
import pandas as pd
from .base import SodecoBase
from .schemas import DATEFORMAT


class Contract(SodecoBase):

    def __init__(self, sodeco):
        super().__init__(sodeco)

    def get(self, worker_id: str, ref_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Get contract information for a worker, optionally at a specific reference date.
        
        Args:
            worker_id: The worker ID to get contract for
            ref_date: Optional reference date to get contract state at
            
        Returns:
            pd.DataFrame: DataFrame containing the contract information
        """
        url = f"{self.sodeco.base_url}worker/{worker_id}/contract"
        if ref_date is not None:
            url += f"/{ref_date.strftime(DATEFORMAT)}"

        data = self._make_request_with_polling(url)
        return pd.DataFrame(data)
