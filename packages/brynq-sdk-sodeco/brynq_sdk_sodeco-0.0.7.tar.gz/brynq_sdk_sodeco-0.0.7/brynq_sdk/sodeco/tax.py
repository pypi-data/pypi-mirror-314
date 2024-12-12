from datetime import datetime
from typing import Optional
from .schemas import DATEFORMAT
import requests
import pandas as pd
from .base import SodecoBase


class Tax(SodecoBase):

    def __init__(self, sodeco):
        super().__init__(sodeco)

    def get(self, worker_id: str, ref_date: Optional[datetime] = None) -> pd.DataFrame:
        url = f"{self.sodeco.base_url}worker/{worker_id}/tax"
        if ref_date is not None:
            url += f"/{ref_date.strftime(DATEFORMAT)}"

        data = self._make_request_with_polling(url)
        return pd.DataFrame(data)
