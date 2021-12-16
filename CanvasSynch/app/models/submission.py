from typing import List
from .base import BaseClass
from dataclasses import dataclass


@dataclass
class Submission(BaseClass):
    submission_type: str
    user_id: int
    file_ids: List[int]
