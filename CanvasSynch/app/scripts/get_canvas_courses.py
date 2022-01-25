import json
import os
from typing import Iterable, cast

import click
from canvasapi import Canvas
from canvasapi.course import Course
from canvasapi.user import User
from dotenv import load_dotenv


@click.command()
@click.argument(
    "output_file", default="courses.json", type=click.File("w", encoding="utf-8")
)
def main(output_file):
    load_dotenv()
    base_url = os.environ.get("CANVAS_API_URL")
    access_token = os.environ.get("CANVAS_API_KEY")
    api = Canvas(base_url, access_token)

    courses_dict = {"courses": []}
    courses = cast(Iterable[Course], api.get_courses(enrollment_type="teacher"))
    for course in courses:
        users = cast(Iterable[User], course.get_users(enrollment_type="student"))
        courses_dict["courses"].append(
            {
                "id": course.id,
                "name": course.name,
                "students": [{"id": user.id} for user in users],
            }
        )

    json.dump(courses_dict, output_file, indent=4)


if __name__ == "__main__":
    main()
