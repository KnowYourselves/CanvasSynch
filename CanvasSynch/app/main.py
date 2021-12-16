import os
from typing import Dict
from dotenv import load_dotenv
from app.canvas.api import CanvasAPI
from pprint import pprint
from models import Assignment, Submission


def main():
    api = CanvasAPI()
    assignments: Dict[str, int] = {}
    for root, _, files in os.walk("../static/courses", topdown=False):
        if len(files) == 0:
            continue

        *_, course_id, assignment_name, user_id = root.split("/")
        filepath = f"{root}/{files[0]}"

        if assignment_name not in assignments:
            assignment = Assignment(
                allowed_extensions=["pdf"],
                name=assignment_name,
                published=True,
                submission_types=["online_upload"],
            )

            assignment_id, _ = api.create_assignment(
                course_id=int(course_id),
                assignment=assignment,
            )

            assignments[assignment_name] = assignment_id

        file_id, _ = api.create_file_in_assignment(
            assignment_id=assignments[assignment_name],
            course_id=int(course_id),
            user_id=int(user_id),
            filepath=filepath,
        )

        submission = Submission(
            submission_type="online_upload",
            user_id=int(user_id),
            file_ids=[file_id],
        )

        pprint(
            api.create_submission(
                int(course_id), assignments[assignment_name], submission
            )
        )


if __name__ == "__main__":
    load_dotenv()
    main()
