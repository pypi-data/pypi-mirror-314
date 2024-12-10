from pathlib import Path

import typer

from amsdal_cli.app import app
from amsdal_cli.commands.build.utils.build_app import build_app
from amsdal_cli.commands.generate.enums import SOURCES_DIR
from amsdal_cli.utils.cli_config import CliConfig


@app.command(name='build, bld, b')
def build_command(
    ctx: typer.Context,
    output: Path = typer.Argument('.', help='Path to output directory'),  # noqa: B008
    config: Path = typer.Option(None, help='Path to custom config.yml file'),  # noqa: B008
) -> None:
    """
    Build the app and generate the models and other files.

    Args:
        ctx (typer.Context): The Typer context object.
        output (Path): The path to the output directory.
        config (Path, optional): The path to the custom config.yml file. Defaults to None.

    Returns:
        None
    """
    cli_config: CliConfig = ctx.meta['config']
    app_source_path = cli_config.app_directory / SOURCES_DIR

    build_app(
        app_source_path=app_source_path,
        config_path=config or cli_config.config_path,
        output=output,
    )
