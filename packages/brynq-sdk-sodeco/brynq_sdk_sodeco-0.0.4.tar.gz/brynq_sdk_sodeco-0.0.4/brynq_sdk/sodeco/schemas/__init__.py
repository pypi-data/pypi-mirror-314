"""Schema definitions for Sodeco package"""

DATEFORMAT = '%Y%m%d'

from .worker import WorkerSchema
from .absence import AbsenceSchema, AbsencesSchema

__all__ = ['WorkerSchema', 'AbsenceSchema', 'AbsencesSchema']
