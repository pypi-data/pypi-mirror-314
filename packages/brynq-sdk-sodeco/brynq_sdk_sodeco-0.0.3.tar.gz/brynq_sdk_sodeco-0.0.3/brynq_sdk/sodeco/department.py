from datetime import datetime
from .schemas import DATEFORMAT
import requests
import pandas as pd


class Department:

    def __init__(self, sodeco):
        self.sodeco = sodeco

    def get(self) -> pd.DataFrame:
        data = requests.Request(method='GET',
                                url=f"{self.sodeco.base_url}department")
        # TODO: add actual data retrieval here
        df = pd.DataFrame(data)

        return df
