import inquirer


class CanvasCLI:
    def select_element(self, elements, label):
        questions = [
            inquirer.List(
                f"{label}_selector",
                message=f"Which {label} do you want to synch?",
                choices=elements,
                default=elements[0],
            ),
        ]

        answer = inquirer.prompt(questions)
        return answer[f"{label}_selector"]

    def get_or_create_element(self, label):
        questions = [
            inquirer.List(
                "get_or_create",
                message=f"Do you want get or create an {label}?",
                choices=["Get", "Create"],
                default="Get",
            ),
        ]

        return inquirer.prompt(questions).get("get_or_create")

    def get_text_elements(self, labels):
        questions = [
            inquirer.Text(
                label,
                message=f"Please enter {label.capitalize()}",
            )
            for label in labels
        ]

        return inquirer.prompt(questions)

    def should_synch_directly(self, courses, override):
        if override:
            return

        courses_names = "\n\t".join([course.name for course in courses])
        questions = [
            inquirer.Confirm(
                "synch_method",
                message=(
                    "The following courses have been found in the static folder:\n"
                    f"\t{courses_names}\n"
                    "Would you like to synch them directly?"
                ),
                default=True,
            )
        ]

        return inquirer.prompt(questions).get("synch_method")
