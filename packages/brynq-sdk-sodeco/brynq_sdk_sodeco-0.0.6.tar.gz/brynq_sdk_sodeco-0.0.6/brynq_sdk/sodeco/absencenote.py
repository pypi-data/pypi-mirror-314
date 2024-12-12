from datetime import datetime
from typing import Optional
import pandas as pd
from .base import SodecoBase
from .schemas import DATEFORMAT


class AbsenceNote(SodecoBase):
    """Class to handle worker absence notes.
    
    This class provides access to worker absence notes, which contain information about 
    worker absences and their associated documentation. Each note can be retrieved either
    by worker ID alone or with a specific note date.
    """
    
    def get(self, worker_id: str, note_id: Optional[datetime] = None) -> pd.DataFrame:
        """
        Get absence note data for a worker.
        
        Args:
            worker_id (str): The ID of the worker
            note_id (datetime, optional): The date of the specific note to retrieve.
                                        If not provided, returns all notes for the worker.
            
        Returns:
            pd.DataFrame: The absence note data containing details about worker absences
                         and their associated documentation.
        """
        if note_id:
            url = f"{self.sodeco.base_url}/worker/{worker_id}/absencenote/{note_id.strftime(DATEFORMAT)}"
        else:
            url = f"{self.sodeco.base_url}/worker/{worker_id}/absencenote"
            
        data = self._make_request_with_polling(url)
        return pd.DataFrame(data)