from datetime import datetime
from typing import Optional
import pandas as pd
from .base import SodecoBase
from .schemas import DATEFORMAT


class Family(SodecoBase):

    def __init__(self, sodeco):
        super().__init__(sodeco)

    def get(self, worker_id: str, ref_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Get family status information for a worker, optionally at a specific reference date.
        
        Args:
            worker_id: The worker ID to get family status for
            ref_date: Optional reference date to get family status at
            
        Returns:
            pd.DataFrame: DataFrame containing the family status information
        """
        url = f"{self.sodeco.base_url}worker/{worker_id}/familystatus"
        if ref_date is not None:
            url += f"/{ref_date.strftime(DATEFORMAT)}"

        data = self._make_request_with_polling(url)
        return pd.DataFrame(data)
