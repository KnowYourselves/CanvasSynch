import os

from typing import Any, Dict, List, Tuple

import requests
from models.assignment import Assignment
from models.courses import Course
from models.submission import Submission
from models.user import User
from .bearer_token import BearerAuth


class CanvasAPI:
    def __init__(self) -> None:
        self.url = os.environ["CANVAS_BASE_URL"]
        self.token = os.environ["CANVAS_TOKEN"]

    def get_users_from_course(self, course_id: int) -> List[User]:
        url = f"{self.url}courses/{course_id}/users"
        response = requests.get(url, auth=BearerAuth(self.token))
        users = response.json()
        return [User(**user) for user in users]

    def get_user_from_course(self, course_id: int, user_id: int) -> User:
        url = f"{self.url}courses/{course_id}/users/{user_id}"
        response = requests.get(url, auth=BearerAuth(self.token))
        user = response.json()
        return User(**user)

    def get_courses(self) -> List[Course]:
        url = f"{self.url}courses"
        response = requests.get(url, auth=BearerAuth(self.token))
        courses = response.json()
        return [Course.from_dict(course) for course in courses]

    def create_assignment(
        self, course_id: int, assignment: Assignment
    ) -> Tuple[int, int]:
        url = f"{self.url}courses/{course_id}/assignments"
        response = requests.post(
            url,
            json={"assignment": assignment.to_dict()},
            auth=BearerAuth(self.token),
        )
        return response.json().get("id"), 201

    def delete_assignment(self, course_id: int, assignment_id: int) -> int:
        url = f"{self.url}courses/{course_id}/assignments/{assignment_id}"
        response = requests.delete(
            url,
            auth=BearerAuth(self.token),
        )
        return response.status_code

    def create_submission(
        self, course_id: int, assignment_id: int, submission: Submission
    ) -> Tuple[Dict[str, Any], int]:
        url = f"{self.url}courses/{course_id}/assignments/{assignment_id}/submissions"
        response = requests.post(
            url,
            json={"submission": submission.to_dict()},
            auth=BearerAuth(self.token),
        )
        return response.json(), 201

    def create_file_in_assignment(
        self, course_id: int, assignment_id: int, user_id: int, filepath: str
    ) -> Tuple[int, int]:
        size = os.path.getsize(filepath)
        name = os.path.basename(filepath)

        url = f"{self.url}courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}/files"
        response = requests.post(
            url,
            json={"name": name, "size": size},
            auth=BearerAuth(self.token),
        )

        upload_url = response.json().get("upload_url")
        payload = {"name": "test.pdf", "size": "20597"}
        files = [
            (
                "",
                (
                    name,
                    open(filepath, "rb"),
                    "application/pdf",
                ),
            )
        ]
        response = requests.post(upload_url, data=payload, files=files)
        return response.json().get("id"), response.status_code
