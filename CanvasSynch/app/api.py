from typing import Iterable, List, Optional

from canvasapi import Canvas
from canvasapi.assignment import Assignment
from canvasapi.course import Course
from canvasapi.exceptions import ResourceDoesNotExist
from canvasapi.submission import Submission
from canvasapi.user import UserDisplay


class CanvasAPI:
    def __init__(self, base_url: str, access_token: str) -> None:
        self.api = Canvas(base_url=base_url, access_token=access_token)

    def get_courses(self, enrollment_type="teacher") -> Iterable[Course]:
        return self.api.get_courses(enrollment_type=enrollment_type)

    def create_assignment(
        self, course: Course, name: str, description: str = ""
    ) -> Assignment:
        return course.create_assignment(
            {
                "name": name,
                "submission_types": ["online_upload"],
                "allowed_extensions": ["pdf"],
                "description": description,
            }
        )

    def get_gradeable_students(self, assignment: Assignment) -> Iterable[UserDisplay]:
        return assignment.get_gradeable_students()

    def upload_file(self, assignment: Assignment, file_path: str, user_id: int):
        return assignment.upload_to_submission(file_path, user=user_id)

    def create_submission(
        self, assignment: Assignment, user_id: int, file_id: int = None
    ) -> Submission:
        return assignment.submit(
            submission={
                "submission_type": "online_upload",
                "user_id": user_id,
                "file_ids": [file_id],
            },
        )

    def get_courses_by_id(self, courses_ids: List[int]) -> List[Course]:
        courses = [self._get_course_by_id(course_id) for course_id in courses_ids]
        return [course for course in courses if course]

    def _get_course_by_id(self, course_id: int) -> Optional[Course]:
        try:
            return self.api.get_course(course_id)
        except (TypeError, ResourceDoesNotExist):
            return None

    def get_or_create_assignments(self, course: Course, assignments_names: List[str]):
        all_assignments = course.get_assignments()
        assignments: List[Assignment] = []
        for name in assignments_names:
            assignment = self.get_assignment_by_name(all_assignments, name)
            if not assignment:
                assignment = self.create_assignment(course, name)
            assignments.append(assignment)
        return assignments

    def get_assignment_by_name(
        self, assignments: Iterable[Assignment], name: str
    ) -> Optional[Assignment]:
        for assignment in assignments:
            if assignment.name == name:
                return assignment
