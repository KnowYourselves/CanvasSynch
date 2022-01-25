import os
from typing import List

from canvasapi.assignment import Assignment as CanvasAssignment
from canvasapi.user import UserDisplay as CanvasUserDisplay

from app.api import CanvasAPI

from .user import User


class Assignment:
    def __init__(
        self, api: CanvasAPI, assignment: CanvasAssignment, base_path: str
    ) -> None:
        self.api = api
        self.assignment = assignment
        self.path = f"{base_path}/{assignment.name}"

    def synch(self):
        users = self.get_users_from_static()
        for user in users:
            user.synch()

    def get_users_from_static(self) -> List[User]:
        user_ids = [int(user_id) for user_id in os.listdir(self.path)]
        return [
            User(self.api, user, self.assignment, self.path)
            for user in self.get_users_by_ids(user_ids)
        ]

    def get_users_by_ids(self, users_ids: List[int]) -> List[CanvasUserDisplay]:
        users = self.assignment.get_gradeable_students()
        return list(filter(lambda user: user.id in users_ids, users))
