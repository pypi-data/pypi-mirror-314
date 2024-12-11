from datetime import datetime
from typing import Optional
import pandas as pd
from .base import SodecoBase
from .schemas import DATEFORMAT


class CostCentres(SodecoBase):

    def __init__(self, sodeco):
        super().__init__(sodeco)

    def get(self, worker_id: Optional[str] = None, start_date: Optional[datetime] = None) -> pd.DataFrame:
        if worker_id is not None:
            url = f"{self.sodeco.base_url}worker/{worker_id}/costcentre"
            if start_date is not None:
                url += f"/{start_date.strftime(DATEFORMAT)}"
        else:
            if start_date is not None:
                raise ValueError("start_date can only be specified when worker_id is provided")
            url = f"{self.sodeco.base_url}costcentre"

        data = self._make_request_with_polling(url)
        return pd.DataFrame(data)
