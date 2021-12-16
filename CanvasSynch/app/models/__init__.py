from models import assignment
from models import base
from models import courses
from models import submission
from models import user

from models.assignment import (
    Assignment,
)
from models.base import (
    BaseClass,
)
from models.courses import (
    Course,
)
from models.submission import (
    Submission,
)
from models.user import (
    User,
)

__all__ = [
    "Assignment",
    "BaseClass",
    "Course",
    "Submission",
    "User",
    "assignment",
    "base",
    "courses",
    "submission",
    "user",
]
