from dataclasses import dataclass
from typing import List

from models.base import BaseClass


@dataclass
class Assignment(BaseClass):
    name: str
    submission_types: List[str]
    allowed_extensions: List[str]
    published: bool
