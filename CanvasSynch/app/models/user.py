from dataclasses import dataclass
from datetime import datetime

from models.base import BaseClass


@dataclass
class User(BaseClass):
    id: int
    name: str
    created_at: datetime
    sortable_name: str
    short_name: str
