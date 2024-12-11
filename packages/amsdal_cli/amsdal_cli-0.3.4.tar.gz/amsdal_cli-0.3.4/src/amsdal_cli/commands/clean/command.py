from pathlib import Path

import typer
from rich import print as rprint

from amsdal_cli.app import app
from amsdal_cli.commands.serve.utils import cleanup_app
from amsdal_cli.utils.text import rich_success


@app.command(name='clean, cln')
def clean_command(
    output: Path = typer.Argument('.', help='Path to output directory'),  # noqa: B008
    *,
    remove_db: bool = typer.Option(False, '--remove-db', '-db', help='Remove local database?'),
) -> None:
    """
    Cleans project's folder by removing all generated files and optionally local database.

    Args:
        output (Path): The path to the output directory.
        remove_db (bool): If True, the local database will be removed.

    Returns:
        None
    """

    cleanup_app(
        output_path=output,
        remove_warehouse=remove_db,
    )
    rprint(rich_success('Cleaned!'))
