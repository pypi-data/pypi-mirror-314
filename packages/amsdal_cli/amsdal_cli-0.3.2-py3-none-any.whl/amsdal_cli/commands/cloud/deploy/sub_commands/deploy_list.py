import datetime
import json
from pathlib import Path
from typing import Annotated

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal.manager import AsyncAmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print as rprint
from rich.table import Table

from amsdal_cli.commands.cloud.deploy.app import deploy_sub_app
from amsdal_cli.commands.cloud.enums import OutputFormat
from amsdal_cli.utils.text import rich_error


def list_command(
    output: Annotated[OutputFormat, typer.Option('--output', '-o')] = OutputFormat.default,
    *,
    list_all: Annotated[bool, typer.Option('--all', '-a')] = False,
) -> None:
    """
    List the apps on the Cloud Server.

    Args:
        output (Annotated[OutputFormat, typer.Option]): The output format for the list.
        list_all (Annotated[bool, typer.Option]): If True, list all apps.

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

    try:
        list_response = manager.cloud_actions_manager.list_deploys(list_all=list_all)
    except AmsdalCloudError as e:
        rprint(rich_error(str(e)))
        return

    if not list_response:
        return

    if output in (OutputFormat.default, OutputFormat.wide):
        if not list_response.deployments:
            rprint('No deployments found.')

        else:
            data_table = Table()

            data_table.add_column('Deploy ID', justify='center')
            data_table.add_column('Environment', justify='center')
            data_table.add_column('Status', justify='center')
            data_table.add_column('Application Name', justify='center')
            data_table.add_column('Created At', justify='center')
            data_table.add_column('Last Update At', justify='center')

            if output == OutputFormat.wide:
                data_table.add_column('Application UUID', justify='center')
                data_table.add_column('Application URL', justify='center')

            for deployment in list_response.deployments:
                if output == OutputFormat.wide:
                    data_table.add_row(
                        deployment.deployment_id,
                        deployment.environment_name,
                        deployment.status,
                        deployment.application_name or '-',
                        datetime.datetime.fromtimestamp(
                            deployment.created_at / 1000,
                            tz=datetime.timezone.utc,
                        ).strftime('%Y-%m-%d %H:%M:%S %Z'),
                        datetime.datetime.fromtimestamp(
                            deployment.last_update_at / 1000,
                            tz=datetime.timezone.utc,
                        ).strftime('%Y-%m-%d %H:%M:%S %Z'),
                        deployment.application_uuid or '-',
                        deployment.domain_url or '-',
                    )
                else:
                    data_table.add_row(
                        deployment.deployment_id,
                        deployment.environment_name,
                        deployment.status,
                        deployment.application_name or '-',
                        datetime.datetime.fromtimestamp(
                            deployment.created_at / 1000,
                            tz=datetime.timezone.utc,
                        ).strftime('%Y-%m-%d %H:%M:%S %Z'),
                        datetime.datetime.fromtimestamp(
                            deployment.last_update_at / 1000,
                            tz=datetime.timezone.utc,
                        ).strftime('%Y-%m-%d %H:%M:%S %Z'),
                    )

            rprint(data_table)

    else:
        rprint(json.dumps(list_response.model_dump(), indent=4))


@deploy_sub_app.callback(invoke_without_command=True)
def list_command_callback(
    ctx: typer.Context,
    output: Annotated[OutputFormat, typer.Option('--output', '-o')] = OutputFormat.default,
    *,
    list_all: Annotated[bool, typer.Option('--all', '-a')] = False,
) -> None:
    """
    List the apps on the Cloud Server.

    Args:
        ctx (typer.Context): The Typer context object.
        output (Annotated[OutputFormat, typer.Option]): The output format for the list.
        list_all (Annotated[bool, typer.Option]): If True, list all apps.

    Returns:
        None
    """

    if ctx.invoked_subcommand is not None:
        return

    list_command(
        output=output,
        list_all=list_all,
    )
