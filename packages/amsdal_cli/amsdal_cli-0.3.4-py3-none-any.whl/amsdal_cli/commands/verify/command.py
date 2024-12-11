import tempfile
import traceback
from pathlib import Path

import typer
from amsdal.configs.constants import CORE_SCHEMAS_PATH
from amsdal.configs.constants import TYPE_SCHEMAS_PATH
from amsdal_models.classes.manager import ClassManager
from amsdal_models.schemas.data_models.schemas_directory import SchemasDirectory
from amsdal_utils.models.enums import SchemaTypes
from rich import print as rprint

from amsdal_cli.app import app
from amsdal_cli.commands.generate.enums import MODEL_JSON_FILE
from amsdal_cli.commands.generate.enums import SOURCES_DIR
from amsdal_cli.commands.verify.utils.verify_json_model import verify_json_model
from amsdal_cli.commands.verify.utils.verify_python_file import verify_python_file
from amsdal_cli.utils.cli_config import CliConfig
from amsdal_cli.utils.copier import walk
from amsdal_cli.utils.text import rich_error
from amsdal_cli.utils.text import rich_info
from amsdal_cli.utils.text import rich_success


@app.command(name='verify, vrf, v')
def verify_command(
    ctx: typer.Context,
    *,
    building: bool = typer.Option(False, help='Do verify model building?'),
) -> None:
    """
    Verifies all application's files such as models, properties, transactions, etc.

    Args:
        ctx (typer.Context): The Typer context object.
        building (bool, optional): If True, verify model building. Defaults to False.

    Returns:
        None
    """
    cli_config: CliConfig = ctx.meta['config']
    errors = []

    rprint(rich_info('Syntax checking...'), end=' ')

    for file_item in walk(cli_config.app_directory / SOURCES_DIR):
        if file_item.name == MODEL_JSON_FILE:
            errors.extend(verify_json_model(file_item))
        elif file_item.name.endswith('.py'):
            errors.extend(verify_python_file(file_item))

    if errors:
        for error in errors:
            rprint(rich_error(f'File: {error.file_path.resolve()}: {error.message}'))
            rprint(rich_error(str(error.details)))

        raise typer.Exit(1)

    rprint(rich_success('OK!'))

    if not building:
        return

    rprint(rich_info('Build models checking...'), end=' ')
    with tempfile.TemporaryDirectory() as _temp_dir:
        output_path: Path = Path(_temp_dir)
        class_manager = ClassManager()
        class_manager.init_models_root(output_path / 'models')

        try:
            class_manager.generate_models(
                [
                    SchemasDirectory(path=TYPE_SCHEMAS_PATH, schema_type=SchemaTypes.TYPE),
                    SchemasDirectory(path=CORE_SCHEMAS_PATH, schema_type=SchemaTypes.CORE),
                    SchemasDirectory(
                        path=cli_config.app_directory / SOURCES_DIR / 'models', schema_type=SchemaTypes.USER
                    ),
                ]
            )
        except Exception as ex:
            rprint(rich_error(f'Failed: {ex} - {traceback.format_exc()}'))
            raise typer.Exit(1) from ex

    rprint(rich_success('OK!'))
