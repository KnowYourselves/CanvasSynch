import os
from typing import List

from canvasapi.user import UserDisplay as CanvasUserDisplay

from app.api import CanvasAPI


class User:
    def __init__(self, api: CanvasAPI, user: CanvasUserDisplay, base_path: str) -> None:
        self.api = api
        self.user = user
        self.path = f"{base_path}/{user.id}"

    def synch(self):
        print(self.get_user_filename_from_static())

    def get_user_filename_from_static(self) -> str:
        filename = os.listdir(self.path)[0]
        return f"{self.path}/{filename}"
