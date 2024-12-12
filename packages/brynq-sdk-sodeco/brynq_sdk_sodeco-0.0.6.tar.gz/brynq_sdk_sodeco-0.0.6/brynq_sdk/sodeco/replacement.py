from datetime import datetime
import pandas as pd
from .base import SodecoBase
from .schemas import DATEFORMAT


class Replacement(SodecoBase):

    def __init__(self, sodeco):
        super().__init__(sodeco)

    def get(self, worker_id: str, ref_date: datetime) -> pd.DataFrame:
        """
        Get replacement information for a worker at a specific reference date.
        
        Args:
            worker_id: The worker ID to get replacement for
            ref_date: Reference date to get replacement at (mandatory)
            
        Returns:
            pd.DataFrame: DataFrame containing the replacement information
        """
        url = f"{self.sodeco.base_url}worker/{worker_id}/replacement/{ref_date.strftime(DATEFORMAT)}"

        data = self._make_request_with_polling(url)
        return pd.DataFrame(data)
