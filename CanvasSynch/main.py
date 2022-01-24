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
    canvas_synch.start(override=synch_directly)


if __name__ == "__main__":
    main()
