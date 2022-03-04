# Canvas Synch

**_With 💜, by Raúl Esteban - rsalvarez@uc.cl_**

## Description

This program is an initial approximation to synching a evaluations using the Canvas API. The objective of this program is to be an easy to use CLI to synch a group of evaluations from a group of courses easily.

## How to Use

### Dependencies

This script needs `Python 3.9` and `poetry 1.0.0` to be installed. Once this requirements are met, the dependencies can be installed by running the `poetry install` command. Once installed, you can enter the `poetry shell` command to access the newly created virtual environment.

### Environment Variables

For this script to function there must be a `.env` file with the following variables:

- **CANVAS_API_URL**: The url of the canvas site.
- **CANVAS_API_KEY**: The canvas token to be used.

### Input

#### Files

This program expects the following structure to exist as an input:

```text
<static>/
└── courses/
    ├── <course_id>/
    │   ├── <assignment_name>/
    │   │   ├── <user_id>/
    │   │   │   └── <filename>.pdf
    │   │   └── ...
    │   └── ...
    └── ...
```

Where `static` is part of the input. This folder input must have a subfolder called `courses`.

Inside the `courses` folder each subfolder will be interpreted as a canvas course id.

Inside each `course_id` folder, each subfolder will be interpreted as an assignment name in said course.

Inside each `assignment_id` folder, each subfolder will be interpreted as a canvas user id of a student of the course.

Finall, inside each `user_id` folder there must be a single pdf file, that will be interpreted as the assignment submission of the student.

For example:

```text
static/
└── courses/
    ├── 156/
    │   └── First Test/
    │       ├── 5/
    │       │   └── my_test.pdf
    │       └── 8/
    │           └── firstest.pdf
    └── 215/
        ├── Assignment One/
        │   └── 2/
        │       └── my_assignment.pdf
        └── Assignment Two/
            └── 2/
                └── my_assignment.pdf
```

The base folder is called `static`, in which there are two courses, of ids `156` and `215`.

In the `156` course there is one assignment, called `First Test` in which both the studens of id `5` and `8` have a submission.

On the other hand in the `215` course there are two assignments, `Assignment One` and `Assignment Two` both of which have a single submission from student id `2`.

#### Main Script

The entry point for the script is the `main.py` file. A help text can be obtained by running `python main.py --help`:

```text
Usage: main.py [OPTIONS]

Options:
  --static-folder TEXT  Folder with the courses to synch.
  --synch-directly
  --help                Show this message and exit.
```

The flag `--static-folder` sets the the `<static>` folder, it defaults to `static`.

The flag `--synch-directly` makes te script directly synch the contents of the `<static>` folder without any type of interactivity.

If the script is run **with** the `--synch-directly` flag set, it will iterate all the courses, for each assignment it will try to obtain it by name, if that fails it will create one with that name. Then, for each user it will create a sumbission in the assignment with the file.

If the script is run **without** the `--synch-directly` flag set the script will present an interactive CLI. First it will detect it the `<static>` folder exists, and offer the option to sync it directly if it does.

After this, there will be options select a course, then get or create an assignment, then to select an user, and finally, to select a file to submit as that users assignment.

#### Testing Script

In the folder `app/scripts` two testing scripts can be found, `get_canvas_courses` and `generate_test_static`.

##### `get_canvas_courses`

This script has a single positional argument, the path for the output file. The default value for this argument is `courses.json`.

To run this script, use the `python3 apps/scripts/get_canvas_courses.py` command. Once run it will obtain all the courses of the user and its students and it will save it in the output file as a JSON that can be used for the next script.

You can access the help text of this command by using the `--help` flag:

```text
Usage: get_canvas_courses.py [OPTIONS] [OUTPUT_FILE]

Options:
  --help  Show this message and exit.
```

##### `generate_test_static`

This script has two positional arguments, the input file (courses) and the output folder.

It also has two flags, `--test-pdf` which value will be the path for the pdf to use for the test, and `--n-assignments` which value will be the amount of assignments to create for each course.

The default values for the positional arguments are `courses.json` and `static`.

The default values for the flags are `test.pdf` and `3`.

To run this script, first run the `get_canvas_courses` script. Then you can run this script by using the `python3 app/generate_test_static.py` command. Once run, this script will generate an input folder that can be use to test the main script.

You can access the help text of this command by using the `--help` flag:

```text
Usage: generate_test_static.py [OPTIONS] [INPUT_FILE] [OUTPUT_FOLDER]

Options:
  --test-pdf PATH
  --n-assignments INTEGER
  --help                   Show this message and exit.
```

## Next Steps

This script is only the base for an eventual automation of the process. I recommend the following steps:

1. Create a web app that uses Canvas Oauth2 to get users access tokens.
2. Allow users (professors or teaching assistants) to upload the input folder as zip (or other compressed formats) to their.
3. Use the web app as a starting point for this script.

This is important because it is against Canvas TOS to ask users to give their tokens, so it is a must to implement Oauth2 in some web service so we can obtain the tokens.
