import os

import click
from dotenv import load_dotenv

from app import CanvasSynch


@click.command()
@click.option(
    "--static-folder",
    default="./static",
    help="Folder with the courses to synch.",
)
@click.option("--synch-directly", is_flag=True)
def main(static_folder: str, synch_directly: bool):
    load_dotenv()

    base_url = os.environ.get("CANVAS_API_URL")
    access_token = os.environ.get("CANVAS_API_KEY")
    if not base_url or not access_token:
        exit(1)

    canvas_synch = CanvasSynch(base_url, access_token, static_folder=static_folder)
    canvas_synch.synch(override=synch_directly)


if __name__ == "__main__":
    import logging

    logger = logging.getLogger("canvasapi")
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    debug_handler = logging.StreamHandler(stream=open("debug.log", "w"))
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    error_handler = logging.StreamHandler()
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)
    logger.setLevel(logging.DEBUG)

    main()
