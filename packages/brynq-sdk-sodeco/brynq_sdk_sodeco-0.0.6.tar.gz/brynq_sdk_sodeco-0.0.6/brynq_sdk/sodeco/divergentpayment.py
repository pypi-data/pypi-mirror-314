from typing import Optional
import pandas as pd

from .base import SodecoBase


class DivergentPayment(SodecoBase):
    """Class to handle divergent payment information.
    
    This class provides access to divergent payment data for workers. Divergent
    payments represent non-standard or exceptional payment arrangements that differ
    from regular payment schemes, which may be applied based on specific
    circumstances or agreements.
    """
    
    def get(self, worker_id: str) -> pd.DataFrame:
        """
        Get divergent payment data for a worker.
        
        Args:
            worker_id (str): The ID of the worker
            
        Returns:
            pd.DataFrame: The divergent payment data containing information about
                         any special or non-standard payment arrangements for the worker.
        """
        url = f"{self.sodeco.base_url}/worker/{worker_id}/divergentpayment"
        data = self._make_request_with_polling(url)
        return pd.DataFrame(data)
