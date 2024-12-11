from typing import Optional
import pandas as pd
from .base import SodecoBase


class Car(SodecoBase):

    def __init__(self, sodeco):
        super().__init__(sodeco)

    def get(self, worker_id: Optional[str] = None) -> pd.DataFrame:
        if worker_id is not None:
            url = f"{self.sodeco.base_url}worker/{worker_id}/companycar"
        else:
            url = f"{self.sodeco.base_url}companycar"

        data = self._make_request_with_polling(url)
        return pd.DataFrame(data)
