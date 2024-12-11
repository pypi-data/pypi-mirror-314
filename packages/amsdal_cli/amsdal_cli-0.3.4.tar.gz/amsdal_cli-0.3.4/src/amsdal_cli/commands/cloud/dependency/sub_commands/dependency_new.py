import typing
from pathlib import Path

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal.manager import AsyncAmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print as rprint
from typer import Option

from amsdal_cli.commands.cloud.dependency.app import dependency_sub_app
from amsdal_cli.commands.cloud.environments.utils import get_current_env
from amsdal_cli.utils.cli_config import CliConfig
from amsdal_cli.utils.text import rich_error
from amsdal_cli.utils.text import rich_highlight
from amsdal_cli.utils.text import rich_info
from amsdal_cli.utils.text import rich_success


@dependency_sub_app.command(name='new, n')
def dependency_new_command(
    ctx: typer.Context,
    dependency_name: str,
    env_name: typing.Annotated[
        typing.Optional[str],  # noqa: UP007
        Option('--env', help='Environment name. Default is the current environment from configratuion.'),
    ] = None,
) -> None:
    """
    Creates a new dependency for your Cloud Server app.

    Args:
        ctx (typer.Context): The Typer context object.
        dependency_name (str): The name of the dependency to create.
        env_name (typing.Optional[str], optional): The name of the environment.
            Defaults to the current environment from configuration.

    Returns:
        None
    """

    cli_config: CliConfig = ctx.meta['config']
    env_name = env_name or get_current_env(cli_config)

    if cli_config.verbose:
        rprint(
            rich_info(f'Adding dependency {rich_highlight(dependency_name)} to environment: {rich_highlight(env_name)}')
        )

    AmsdalConfigManager().load_config(Path('./config.yml'))

    manager: AsyncAmsdalManager | AmsdalManager
    if AmsdalConfigManager().get_config().async_mode:
        manager = AsyncAmsdalManager()
    else:
        manager = AmsdalManager()

    manager.authenticate()

    try:
        manager.cloud_actions_manager.add_dependency(
            dependency_name=dependency_name,
            env_name=env_name,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
        )
    except AmsdalCloudError as e:
        rprint(rich_error(str(e)))
        raise typer.Exit(1) from e
    else:
        config_dir: Path = cli_config.app_directory / '.amsdal'
        config_dir.mkdir(exist_ok=True, parents=True)
        _deps_path: Path = config_dir / '.dependencies'
        _deps_path.touch(exist_ok=True)
        _deps = set(_deps_path.read_text().split('\n'))
        _deps.add(dependency_name)
        _deps_path.write_text('\n'.join(_deps))

    rprint(rich_success('Dependency added successfully'))
