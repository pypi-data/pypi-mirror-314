from datetime import datetime
from typing import Optional
from .schemas import DATEFORMAT
import requests
import pandas as pd


class Tax:

    def __init__(self, sodeco):
        self.sodeco = sodeco

    def get(self, worker_id: str, ref_date: Optional[datetime] = None) -> pd.DataFrame:
        url = f"{self.sodeco.base_url}worker/{worker_id}/tax"
        if ref_date is not None:
            url += f"/{ref_date.strftime(DATEFORMAT)}"

        data = requests.Request(method='GET',
                                url=url)
        # TODO: add actual data retrieval here
        df = pd.DataFrame(data)

        return df
