from pathlib import Path

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal.manager import AsyncAmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print as rprint

from amsdal_cli.commands.cloud.deploy.app import deploy_sub_app
from amsdal_cli.commands.cloud.environments.utils import get_current_env
from amsdal_cli.utils.cli_config import CliConfig
from amsdal_cli.utils.text import CustomConfirm
from amsdal_cli.utils.text import rich_error
from amsdal_cli.utils.text import rich_highlight
from amsdal_cli.utils.text import rich_info
from amsdal_cli.utils.text import rich_success
from amsdal_cli.utils.text import rich_warning


@deploy_sub_app.command(name='delete, del, d')
def destroy_command(ctx: typer.Context, deployment_id: str) -> None:
    """
    Destroy the app on the Cloud Server.

    Args:
        ctx (typer.Context): The Typer context object.
        deployment_id (str): The ID of the deployment to destroy.

    Returns:
        None
    """
    AmsdalConfigManager().load_config(Path('./config.yml'))

    manager: AsyncAmsdalManager | AmsdalManager
    if AmsdalConfigManager().get_config().async_mode:
        manager = AsyncAmsdalManager()
    else:
        manager = AmsdalManager()

    manager.authenticate()
    cli_config: CliConfig = ctx.meta['config']
    current_env = get_current_env(cli_config)

    try:
        list_response = manager.cloud_actions_manager.list_deploys(list_all=False)
    except AmsdalCloudError as e:
        rprint(rich_error(str(e)))
        return

    found_deployment = False
    deployment_env = current_env
    for deployment in list_response.deployments:
        if deployment.deployment_id == deployment_id:
            found_deployment = True
            deployment_env = deployment.environment_name or ''
            break

    if not found_deployment:
        rprint(rich_error(f'Deployment with ID {rich_highlight(deployment_id)} not found.'))
        return

    if cli_config.application_name:
        msg = (
            f'You are about to destroy the deployment for {rich_highlight(cli_config.application_name)} '
            f'and environment {rich_highlight(deployment_env)}.'
        )

    else:
        msg = (
            f'You are about to destroy the deployment with ID {rich_highlight(deployment_id)} and '
            f'environment {rich_highlight(deployment_env)}.'
        )

    if not CustomConfirm.ask(
        rich_info(f'{msg} Are you sure you want to proceed?'),
        default=False,
        show_default=False,
        choices=['y', 'N'],
    ):
        rprint(rich_warning('Operation canceled.'))
        return

    try:
        manager.cloud_actions_manager.destroy_deploy(deployment_id)
    except AmsdalCloudError as e:
        rprint(rich_error(str(e)))
        return

    rprint(
        rich_success(
            'Destroying process is in progress now. '
            'After a few minutes, you can check the status of your deployment.'
        )
    )
