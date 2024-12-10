from subprocess import PIPE
from subprocess import Popen

import typer
from amsdal.manager import AmsdalManager
from amsdal.utils.tests.enums import DbExecutionType
from amsdal.utils.tests.enums import LakehouseOption
from amsdal.utils.tests.enums import StateOption
from amsdal_utils.config.manager import AmsdalConfigManager

from amsdal_cli.commands.tests.app import sub_app
from amsdal_cli.utils.cli_config import CliConfig

PYTEST_COMMAND = 'pytest'


@sub_app.command(
    name='run',
    context_settings={
        'allow_extra_args': True,
        'ignore_unknown_options': True,
    },
)
def run_tests(
    ctx: typer.Context,
    db_execution_type: DbExecutionType = DbExecutionType.include_state_db,
    state_option: StateOption = StateOption.sqlite,
    lakehouse_option: LakehouseOption = LakehouseOption.sqlite,
) -> None:
    """
    Run tests with the specified database execution type, state option, and lakehouse option.

    Args:
        ctx (typer.Context): The Typer context object.
        db_execution_type (DbExecutionType): The type of database execution to use.
        state_option (StateOption): The state option to use.
        lakehouse_option (LakehouseOption): The lakehouse option to use.

    Returns:
        None
    """

    cli_config: CliConfig = ctx.meta['config']
    config_manager = AmsdalConfigManager()
    config_manager.load_config(cli_config.config_path)
    manager = AmsdalManager()
    manager.setup()
    manager.authenticate()
    manager.teardown()
    AmsdalManager.invalidate()
    AmsdalConfigManager.invalidate()

    with Popen(  # noqa: S603
        [
            PYTEST_COMMAND,
            'src',
            '--color=yes',
            '--db_execution_type',
            db_execution_type,
            '--state_option',
            state_option,
            '--lakehouse_option',
            lakehouse_option,
            *ctx.args,
        ],
        stdout=PIPE,
        bufsize=1,
        universal_newlines=True,
    ) as p:
        if p.stdout is not None:
            for line in p.stdout:
                print(line, end='')  # noqa: T201
