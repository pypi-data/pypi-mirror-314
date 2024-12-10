from pathlib import Path

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal.manager import AsyncAmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print as rprint

from amsdal_cli.commands.cloud.environments.app import environment_sub_app
from amsdal_cli.utils.cli_config import CliConfig
from amsdal_cli.utils.text import rich_error
from amsdal_cli.utils.text import rich_highlight
from amsdal_cli.utils.text import rich_success


@environment_sub_app.command(name='new, n')
def env_add_command(ctx: typer.Context, env_name: str) -> None:
    """
    Adds a new environment to your Cloud Server app.

    Args:
        ctx (typer.Context): The Typer context object.
        env_name (str): The name of the environment to add.

    Returns:
        None
    """

    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))

    manager: AsyncAmsdalManager | AmsdalManager
    if AmsdalConfigManager().get_config().async_mode:
        manager = AsyncAmsdalManager()
    else:
        manager = AmsdalManager()

    manager.authenticate()

    try:
        manager.cloud_actions_manager.create_env(
            env_name=env_name,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
        )
    except AmsdalCloudError as e:
        rprint(rich_error(str(e)))
        raise typer.Exit(1) from e

    rprint(rich_success(f'Environment {rich_highlight(env_name)} created successfully.'))
