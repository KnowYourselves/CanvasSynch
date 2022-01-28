import os
from typing import Dict, List, cast

from canvasapi.assignment import Assignment as CanvasAssignment
from canvasapi.course import Course as CanvasCourse
from canvasapi.user import UserDisplay as CanvasUserDisplay

from app.api import CanvasAPI
from app.cli import CanvasCLI

from .course import Course


class CanvasSynch:
    def __init__(
        self, base_url: str, access_token: str, static_folder="static"
    ) -> None:
        self.api = CanvasAPI(base_url, access_token)
        self.cli = CanvasCLI()
        self.static_folder = static_folder.rstrip("/")

    def synch(self, override=False) -> None:
        canvas_courses = self.get_courses_from_static()
        synch_directly = self.cli.should_synch_directly(canvas_courses, override)
        if override or synch_directly:
            courses = self.canvas_courses_to_our_courses(canvas_courses)
            self.direct_synch(courses)
        else:
            self.interactive_synch()

    def get_courses_from_static(self) -> List[CanvasCourse]:
        try:
            courses_path = f"{self.static_folder}/courses"
            courses_ids = [int(course_id) for course_id in os.listdir(courses_path)]
            return self.api.get_courses_by_id(courses_ids)

        except FileNotFoundError:
            return []

    def canvas_courses_to_our_courses(
        self, courses: List[CanvasCourse]
    ) -> List[Course]:
        return [
            Course(self.api, canvas_course, f"{self.static_folder}/courses")
            for canvas_course in courses
        ]

    def interactive_synch(self) -> None:
        course = self.get_course()
        assignment = self.get_assignment(course)
        user = self.get_user(assignment)
        filename = self.get_filename()
        _, file = self.api.upload_file(assignment, filename, user.id)
        self.api.create_submission(assignment, user.id, file.get("id"))

    def get_course(self) -> CanvasCourse:
        courses = self.api.get_courses()
        return self.cli.select_element(courses, label="course")

    def get_assignment(self, course: CanvasCourse):
        get_or_create = self.cli.get_or_create_element(label="assignment")
        if get_or_create == "Get":
            assignments = course.get_assignments()
            return self.cli.select_element(assignments, label="assignment")
        else:
            assignment_data = cast(
                Dict[str, str],
                self.cli.get_text_elements(labels=["name", "description"]),
            )
            return self.api.create_assignment(course, **assignment_data)

    def get_user(self, assignment: CanvasAssignment) -> CanvasUserDisplay:
        users = assignment.get_gradeable_students()
        if not users:
            print("There are no gradeable users.")
            exit(0)
        return self.cli.select_element(users, label="user")

    def get_filename(self) -> str:
        file_path = ""
        while not os.path.isfile(file_path):
            if file_path:
                print("Please enter a existing file.")
            file_path = self.cli.get_text_elements(labels=["file"]).get("file")
        return file_path

    def direct_synch(self, courses: List[Course]) -> None:
        for course in courses:
            course.synch()
