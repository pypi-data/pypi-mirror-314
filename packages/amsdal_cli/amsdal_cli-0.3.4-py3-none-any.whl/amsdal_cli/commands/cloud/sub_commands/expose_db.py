import typing
from pathlib import Path
from typing import Optional

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal.manager import AsyncAmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print as rprint
from typer import Option

from amsdal_cli.commands.cloud.app import cloud_sub_app
from amsdal_cli.commands.cloud.environments.utils import get_current_env
from amsdal_cli.utils.cli_config import CliConfig
from amsdal_cli.utils.text import rich_error
from amsdal_cli.utils.text import rich_highlight
from amsdal_cli.utils.text import rich_info


@cloud_sub_app.command(name='expose-db, expose_db, edb')
def expose_db_command(
    ctx: typer.Context,
    env_name: typing.Annotated[
        typing.Optional[str],  # noqa: UP007
        Option('--env', help='Environment name. Default is the current environment from configratuion.'),
    ] = None,
    ip_address: Optional[str] = None,  # noqa: UP007
) -> None:
    """
    Adds your IP to the allowlist of the database and returns the connection configs.

    Args:
        ctx (typer.Context): The Typer context object.
        env_name (typing.Annotated[typing.Optional[str], Option]): The name of the environment. Defaults to the current
            environment from configuration.
        ip_address (Optional[str]): The IP address to add to the allowlist. If not provided, your IP will be used.

    Returns:
        None
    """

    cli_config: CliConfig = ctx.meta['config']
    env_name = env_name or get_current_env(cli_config)

    if cli_config.verbose:
        rprint(rich_info(f'Exposing database for environment: {rich_highlight(env_name)}'))

    AmsdalConfigManager().load_config(Path('./config.yml'))

    manager: AsyncAmsdalManager | AmsdalManager
    if AmsdalConfigManager().get_config().async_mode:
        manager = AsyncAmsdalManager()
    else:
        manager = AmsdalManager()

    manager.authenticate()

    try:
        response = manager.cloud_actions_manager.expose_db(
            env_name=env_name,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
            ip_address=ip_address,
        )
        rprint(response)
    except AmsdalCloudError as e:
        rprint(rich_error(str(e)))
        return
