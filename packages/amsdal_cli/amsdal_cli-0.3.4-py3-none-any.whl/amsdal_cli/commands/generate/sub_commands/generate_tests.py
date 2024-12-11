import typer
from rich import print as rprint

from amsdal_cli.commands.generate.app import sub_app
from amsdal_cli.commands.generate.enums import TestDataType
from amsdal_cli.commands.generate.enums import TestType
from amsdal_cli.commands.generate.utils.tests.conftest_utils import create_conftest_if_not_exist
from amsdal_cli.commands.generate.utils.tests.unit import generate_and_save_unit_tests
from amsdal_cli.utils.cli_config import CliConfig
from amsdal_cli.utils.text import rich_error
from amsdal_cli.utils.text import rich_highlight
from amsdal_cli.utils.text import rich_info
from amsdal_cli.utils.text import rich_success


@sub_app.command(name='tests')
def generate_tests(
    ctx: typer.Context,
    model_name: str = typer.Option(..., help='The model name. It should be provided in PascalCase.'),
    test_type: TestType = typer.Option(TestType.UNIT, help='The type of test to generate.'),  # noqa: B008
    test_data_type: TestDataType = typer.Option(  # noqa: B008
        TestDataType.DYNAMIC,
        help='The type of test data to generate.',
    ),
) -> None:
    """
    Generates tests for the given model.

    Args:
        ctx (typer.Context): The Typer context object.
        model_name (str): The model name. It should be provided in PascalCase.
        test_type (TestType): The type of test to generate.
        test_data_type (TestDataType): The type of test data to generate.

    Returns:
        None
    """
    cli_config: CliConfig = ctx.meta['config']

    create_conftest_if_not_exist(cli_config)

    if test_type == TestType.UNIT:
        try:
            rprint(rich_info(f'Generating unit tests for {rich_highlight(model_name)}...'))

            if generate_and_save_unit_tests(model_name, cli_config, test_data_type=test_data_type):
                rprint(rich_success(f'Unit tests for {rich_highlight(model_name)} generated successfully.'))
        except Exception as e:
            rprint(rich_error(str(e)))
            raise typer.Exit(1) from e
