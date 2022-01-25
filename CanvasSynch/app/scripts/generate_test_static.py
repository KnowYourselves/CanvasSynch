import json
import os
import random
import shutil

import click


@click.command()
@click.argument(
    "input_file",
    default="courses.json",
    type=click.File("r", encoding="utf-8"),
)
@click.argument(
    "output_folder",
    default="static",
    type=click.Path(exists=True),
)
@click.option(
    "--test-pdf",
    default="test.pdf",
    type=click.Path(exists=True),
)
@click.option(
    "--n-assignments",
    default=3,
    type=click.INT,
)
def main(input_file, output_folder, test_pdf, n_assignments):
    random_base = f"{random.randint(0, 100000):<06}"
    filename = os.path.basename(test_pdf)

    base_path = f"{output_folder}/courses"
    courses = json.load(input_file)
    for course in courses.get("courses"):
        course_id = course.get("id")
        students = course.get("students")

        course_path = f"{base_path}/{course_id}"
        for i in range(n_assignments):
            assignment_path = f"{course_path}/{random_base}_Test_{i}"
            for student in students:
                student_id = student.get("id")
                student_path = f"{assignment_path}/{student_id}/{filename}"

                os.makedirs(os.path.dirname(student_path), exist_ok=True)
                shutil.copy(test_pdf, student_path)


if __name__ == "__main__":
    main()
