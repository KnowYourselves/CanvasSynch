from dataclasses import dataclass

from models.base import BaseClass


@dataclass
class Course(BaseClass):
    id: int
    name: str
    course_code: str
