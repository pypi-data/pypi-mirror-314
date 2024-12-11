import random
import string
import uuid
from pathlib import Path

import typer
from amsdal.__about__ import __version__ as amsdal_version
from amsdal_utils.utils.text import slugify
from amsdal_utils.utils.text import to_snake_case
from rich import print as rprint

from amsdal_cli.app import app
from amsdal_cli.commands.generate.enums import SOURCES_DIR
from amsdal_cli.utils.copier import copy_blueprints_from_directory
from amsdal_cli.utils.text import rich_error
from amsdal_cli.utils.text import rich_success


@app.command(name='new, n')
def new_command(
    app_name: str = typer.Argument(
        ...,
        help='The Application name. For example: MyApplication',
    ),
    output_path: Path = typer.Argument(  # noqa: B008
        ...,
        help='Output path, where the app will be created.',
    ),
) -> None:
    """
    Generates a new AMSDAL application.

    Args:
        app_name (str): The Application name. For example: MyApplication.
        output_path (Path): Output path, where the app will be created.

    Returns:
        None
    """

    if not output_path.exists():
        rprint(rich_error(f'The output path "{output_path.resolve()}" does not exist.'))
        raise typer.Exit

    if output_path.is_file():
        rprint(rich_error(f'The output path "{output_path.resolve()}" is not a directory.'))
        raise typer.Exit

    output_path /= to_snake_case(app_name)

    if output_path.exists():
        if output_path.is_file():
            rprint(rich_error(f'The path "{output_path.resolve()}" is not a directory.'))
            raise typer.Exit

        if any(output_path.iterdir()):
            rprint(rich_error(f'The directory "{output_path.resolve()}" is not empty.'))
            raise typer.Exit

    application_uuid = (random.choice(string.ascii_lowercase) + uuid.uuid4().hex[:31]).lower()  # noqa: S311

    copy_blueprints_from_directory(
        source_path=Path(__file__).parent / 'templates',
        destination_path=output_path,
        context={
            'application_uuid': application_uuid,
            'application_name': app_name,
            'application_name_slugify': slugify(app_name),
            'amsdal_version': amsdal_version,
        },
    )
    (output_path / SOURCES_DIR).mkdir(exist_ok=True)

    rprint(rich_success(f'The application is successfully created in {output_path.resolve()}'))
