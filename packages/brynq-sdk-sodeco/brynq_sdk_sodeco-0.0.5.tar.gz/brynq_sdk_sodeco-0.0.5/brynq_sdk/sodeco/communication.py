from datetime import datetime
from .schemas import DATEFORMAT
from .base import SodecoBase
import requests
import pandas as pd
from typing import Optional


class Communication(SodecoBase):

    def __init__(self, sodeco):
        super().__init__(sodeco)

    def get(self, worker_id: str) -> pd.DataFrame:
        url = f"{self.sodeco.base_url}worker/{worker_id}/communication"

        data = self._make_request_with_polling(url)
        return pd.DataFrame(data)
