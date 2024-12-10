import typer
from amsdal_utils.utils.text import classify
from amsdal_utils.utils.text import to_snake_case

from amsdal_cli.commands.generate.app import sub_app
from amsdal_cli.commands.generate.enums import SOURCES_DIR
from amsdal_cli.utils.cli_config import CliConfig
from amsdal_cli.utils.copier import copy_blueprint


@sub_app.command(name='transaction, tr, t')
def generate_transaction(
    ctx: typer.Context,
    transaction_name: str = typer.Argument(
        ...,
        help=(
            'The transaction name. Note, it will always transform the provided name to camel_case. Enter the name in '
            'camel_case in order to avoid any issues.'
        ),
    ),
) -> None:
    """
    Generates transaction file for specified model.

    Args:
        ctx (typer.Context): The Typer context object.
        transaction_name (str): The transaction name. Note, it will always transform the provided name to camel_case.
                                Enter the name in camel_case in order to avoid any issues.

    Returns:
        None
    """
    cli_config: CliConfig = ctx.meta['config']
    name = to_snake_case(transaction_name)
    output_path = cli_config.app_directory / SOURCES_DIR / 'transactions'

    copy_blueprint(
        source_file_path=cli_config.templates_path / 'transaction.pyt',
        destination_path=output_path,
        destination_name=f'{name}.py',
        context={
            'transaction_method_name': name,
            'transaction_class_name': classify(transaction_name),
        },
        confirm_overwriting=True,
    )
