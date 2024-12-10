import asyncio
import sys
import typing
from pathlib import Path

import typer
from amsdal.cloud.enums import DeployType
from amsdal.cloud.enums import LakehouseOption
from amsdal.configs.main import settings
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal.manager import AsyncAmsdalManager
from amsdal.migration.file_migration_generator import AsyncFileMigrationGenerator
from amsdal.migration.file_migration_generator import FileMigrationGenerator
from amsdal.migration.schemas_loaders import JsonClassSchemaLoader
from amsdal_utils.config.manager import AmsdalConfigManager
from amsdal_utils.models.enums import SchemaTypes
from rich import print as rprint
from typer import Option

from amsdal_cli.commands.cloud.deploy.app import deploy_sub_app
from amsdal_cli.commands.cloud.environments.utils import get_current_env
from amsdal_cli.commands.generate.enums import SOURCES_DIR
from amsdal_cli.commands.migrations.constants import MIGRATIONS_DIR_NAME
from amsdal_cli.utils.cli_config import CliConfig
from amsdal_cli.utils.text import CustomConfirm
from amsdal_cli.utils.text import rich_error
from amsdal_cli.utils.text import rich_highlight
from amsdal_cli.utils.text import rich_info
from amsdal_cli.utils.text import rich_success
from amsdal_cli.utils.text import rich_warning


@deploy_sub_app.command('new, n')
def deploy_command(
    ctx: typer.Context,
    deploy_type: DeployType = DeployType.include_state_db,
    lakehouse_type: LakehouseOption = LakehouseOption.postgres,
    env_name: typing.Annotated[
        typing.Optional[str],  # noqa: UP007
        Option('--env', help='Environment name. Default is the current environment from configratuion.'),
    ] = None,
    from_env: typing.Optional[str] = Option(None, '--from-env', help='Environment name to copy from.'),  # noqa: UP007
    *,
    no_input: bool = Option(False, '--no-input', help='Do not prompt for input.'),
    skip_checks: bool = Option(
        False,
        '--skip-checks',
        help='Skip checking secrets and dependencies before deploying.',
    ),
) -> None:
    """
    Deploy the app to the Cloud Server.

    Args:
        ctx (typer.Context): The Typer context object.
        deploy_type (DeployType): The type of deployment. Defaults to DeployType.include_state_db.
        lakehouse_type (LakehouseOption): The type of lakehouse. Defaults to LakehouseOption.postgres.
        env_name (typing.Optional[str], optional): The name of the environment. Defaults to the current environment
            from configuration.
        from_env (typing.Optional[str], optional): The environment name to copy from.
        no_input (bool, optional): If True, do not prompt for input. Defaults to False.
        skip_checks (bool, optional): If True, skip checking secrets and dependencies before deploying.
            Defaults to False.

    Returns:
        None
    """
    cli_config: CliConfig = ctx.meta['config']
    app_source_path = cli_config.app_directory / SOURCES_DIR
    env_name = env_name or get_current_env(cli_config)

    if cli_config.verbose:
        rprint(rich_info(f'Deploying to environment: {rich_highlight(env_name)}'))

    AmsdalConfigManager().load_config(Path('./config.yml'))

    manager: AsyncAmsdalManager | AmsdalManager
    if AmsdalConfigManager().get_config().async_mode:
        manager = AsyncAmsdalManager()
        # Check migrations
        settings.override(APP_PATH=cli_config.app_directory)
        asyncio.run(_async_check_missing_generated_migrations(manager, app_source_path))
    else:
        manager = AmsdalManager()
        # Check migrations
        settings.override(APP_PATH=cli_config.app_directory)
        _check_missing_generated_migrations(manager, app_source_path)

    manager.authenticate()

    if not skip_checks:
        try:
            list_response_deps = manager.cloud_actions_manager.list_dependencies(
                env_name=env_name,
                application_uuid=cli_config.application_uuid,
                application_name=cli_config.application_name,
            )
        except AmsdalCloudError as e:
            rprint(rich_error(f'Failed to loading dependencies: {e}'))
            raise typer.Exit(1) from e

        config_dir: Path = cli_config.app_directory / '.amsdal'
        config_dir.mkdir(exist_ok=True, parents=True)
        _deps_path: Path = config_dir / '.dependencies'
        _deps_path.touch(exist_ok=True)
        _deps = set(_deps_path.read_text().split('\n'))
        _diff_deps = list(filter(None, _deps - set(list_response_deps.dependencies)))

        if _diff_deps:
            rprint(
                rich_warning(f'The following dependencies are missing: {", ".join(map(rich_highlight, _diff_deps))}')
            )

            if no_input:
                rprint(rich_info('Installing missing dependencies...'))
                install_deps = True
            else:
                install_deps = CustomConfirm.ask(
                    rich_info('Do you want to install the missing dependencies?'),
                    default=False,
                    show_default=False,
                    choices=['y', 'N'],
                )

            if not install_deps:
                rprint(rich_info('Use "amsdal cloud dependencies new NAME" to install the missing dependencies.'))
                raise typer.Exit(1)

            for dependency_name in _diff_deps:
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

        try:
            list_response_secrets = manager.cloud_actions_manager.list_secrets(
                with_values=False,
                env_name=env_name,
                application_uuid=cli_config.application_uuid,
                application_name=cli_config.application_name,
            )
        except AmsdalCloudError as e:
            rprint(rich_error(f'Failed to loading secrets: {e}'))
            raise typer.Exit(1) from e

        _secrets_path: Path = config_dir / '.secrets'
        _secrets_path.touch(exist_ok=True)
        _secrets = set(_secrets_path.read_text().split('\n'))
        _diff_secrets = list(filter(None, _secrets - set(list_response_secrets.secrets)))

        if _diff_secrets:
            rprint(rich_error(f'The following secrets are missing: {", ".join(_diff_secrets)}'))
            raise typer.Exit(1)

    try:
        manager.cloud_actions_manager.create_deploy(
            deploy_type=deploy_type.value,
            lakehouse_type=lakehouse_type.value,
            env_name=env_name,
            from_env=from_env,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
            no_input=no_input,
        )
    except AmsdalCloudError as e:
        if str(e) in ['Same environment name', 'same_environment_name']:
            rprint(
                rich_error(
                    f'Trying to deploy {rich_highlight(env_name)} environment from '
                    f'{rich_highlight(str(from_env))}. Please check the environment names.'
                )
            )
        elif str(e) in ['Environment not found', 'environment_not_found']:
            if from_env:
                rprint(
                    rich_error(f'Environment {rich_highlight(from_env)} not found. Please check the environment name.')
                )
            else:
                rprint(
                    rich_error(f'Environment {rich_highlight(env_name)} not found. Please check the environment name.')
                )

        elif str(e) in ['Environment not deployed', 'environment_not_deployed']:
            rprint(
                rich_error(
                    f'Environment {rich_highlight(str(from_env))} is not deployed. '
                    'Please check the environment name.'
                )
            )

        else:
            rprint(rich_error(str(e)))

        raise typer.Exit(1) from e


def _check_missing_generated_migrations(amsdal_manager: AmsdalManager, app_source_path: Path) -> None:
    """
    Check if there are missing migrations.

    Args:
        amsdal_manager (AmsdalManager): The Amsdal manager instance.

    Returns:
        None
    """
    amsdal_manager.pre_setup()

    rprint(rich_info('Building migrations...'), end=' ')
    amsdal_manager.build_migrations(app_source_path)
    rprint(rich_success('OK!'))

    if not amsdal_manager.is_setup:
        amsdal_manager.setup()

    if not amsdal_manager.is_authenticated:
        amsdal_manager.authenticate()

    amsdal_manager.post_setup()

    schema_loader = JsonClassSchemaLoader(app_source_path / 'models')
    migrations_dir = app_source_path / MIGRATIONS_DIR_NAME

    generator = FileMigrationGenerator(
        schema_loader=schema_loader,
        app_migrations_path=migrations_dir,
    )

    operations = generator.generate_operations(SchemaTypes.USER)

    if operations:
        rprint(rich_error('Missing generated migrations. Use `amsdal migrations new` to fix. Exiting...'))
        sys.exit(1)


async def _async_check_missing_generated_migrations(amsdal_manager: AsyncAmsdalManager, app_source_path: Path) -> None:
    """
    Check if there are missing migrations.

    Args:
        amsdal_manager (AsyncAmsdalManager): The Amsdal manager instance.

    Returns:
        None
    """
    amsdal_manager.pre_setup()

    rprint(rich_info('Building migrations...'), end=' ')
    amsdal_manager.build_migrations(app_source_path)
    rprint(rich_success('OK!'))

    if not amsdal_manager.is_setup:
        await amsdal_manager.setup()

    if not amsdal_manager.is_authenticated:
        amsdal_manager.authenticate()

    await amsdal_manager.post_setup()

    schema_loader = JsonClassSchemaLoader(app_source_path / 'models')
    migrations_dir = app_source_path / MIGRATIONS_DIR_NAME

    generator = AsyncFileMigrationGenerator(
        schema_loader=schema_loader,
        app_migrations_path=migrations_dir,
    )

    operations = await generator.generate_operations(SchemaTypes.USER)

    if operations:
        rprint(rich_error('Missing generated migrations. Use `amsdal migrations new` to fix. Exiting...'))
        sys.exit(1)
