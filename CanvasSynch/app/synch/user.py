import os

from canvasapi.assignment import Assignment as CanvasAssignment
from canvasapi.user import UserDisplay as CanvasUserDisplay

from app.api import CanvasAPI


class User:
    def __init__(
        self,
        api: CanvasAPI,
        user: CanvasUserDisplay,
        assignment: CanvasAssignment,
        base_path: str,
    ) -> None:
        self.api = api
        self.user = user
        self.assignment = assignment
        self.path = f"{base_path}/{user.id}"

    def synch(self):
        filename = self.get_user_filename_from_static()
        file_id = self.upload_file(filename)
        self.create_submission(file_id)

    def get_user_filename_from_static(self) -> str:
        filename = os.listdir(self.path)[0]
        return f"{self.path}/{filename}"

    def upload_file(self, filename: str) -> int:
        _, file = self.api.upload_file(self.assignment, filename, self.user.id)
        return file.get("id")

    def create_submission(self, file_id) -> None:
        self.api.create_submission(self.assignment, self.user.id, file_id)
