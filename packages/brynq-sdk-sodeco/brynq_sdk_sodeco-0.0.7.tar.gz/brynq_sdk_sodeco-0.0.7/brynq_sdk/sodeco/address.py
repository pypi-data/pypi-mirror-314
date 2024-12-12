from datetime import datetime
from .schemas import DATEFORMAT
from .base import SodecoBase
import pandas as pd
from typing import Optional


class Address(SodecoBase):

    def __init__(self, sodeco):
        super().__init__(sodeco)

    def get(self, worker_id: str) -> pd.DataFrame:
        url = f"{self.sodeco.base_url}worker/{worker_id}/address"

        data = self._make_request_with_polling(url)
        return pd.DataFrame(data)
