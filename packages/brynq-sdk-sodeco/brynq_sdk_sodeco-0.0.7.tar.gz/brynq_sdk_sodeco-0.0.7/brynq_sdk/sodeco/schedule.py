import pandas as pd
from .base import SodecoBase


class Schedule(SodecoBase):
    """Class to handle work schedule information.
    
    This class provides access to possible work schedules within an employer. These
    schedules define the various working time arrangements that can be assigned to
    workers, including regular hours, shifts, and other time patterns.
    """
    
    def get(self) -> pd.DataFrame:
        """
        Get work schedule data.
        
        Returns:
            pd.DataFrame: The schedule data containing information about different
                         possible work time arrangements and their specifications.
        """
        url = f"{self.sodeco.base_url}/schedule"
        data = self._make_request_with_polling(url)
        return pd.DataFrame(data)
