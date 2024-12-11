from datetime import datetime
from .schemas import DATEFORMAT
from .base import SodecoBase
import pandas as pd
from typing import Optional



class Contract(SodecoBase):

    def __init__(self, sodeco):
        super().__init__(sodeco)

    def get(self, worker_id: Optional[str] = None) -> pd.DataFrame:
        if worker_id is not None:
            url = f"{self.sodeco.base_url}worker/{worker_id}/contract"
        else:
            url = f"{self.sodeco.base_url}contract"

        data = self._make_request_with_polling(url)
        return pd.DataFrame(data)
