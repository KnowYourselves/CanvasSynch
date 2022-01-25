import os
from typing import List

from canvasapi.course import Course as CanvasCourse

from app.api import CanvasAPI

from .assignment import Assignment


class Course:
    def __init__(self, api: CanvasAPI, course: CanvasCourse, base_path: str) -> None:
        self.api = api
        self.course = course
        self.path = f"{base_path}/{course.id}"

    def synch(self):
        assignments_names = self.get_assignments_names_from_static()
        assignments = self.get_assignments(assignments_names)
        for assignment in assignments:
            assignment.synch()

    def get_assignments(self, assignments_names: List[str]) -> List[Assignment]:
        assignments = self.api.get_or_create_assignments(self.course, assignments_names)
        return [
            Assignment(self.api, assignment, self.path) for assignment in assignments
        ]

    def get_assignments_names_from_static(self) -> List[str]:
        assignments_names = [
            dir_path
            for dir_path in os.listdir(self.path)
            if os.path.isdir(f"{self.path}/{dir_path}")
        ]
        return assignments_names
