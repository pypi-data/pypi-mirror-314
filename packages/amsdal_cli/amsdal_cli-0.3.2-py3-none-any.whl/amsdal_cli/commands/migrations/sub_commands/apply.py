import asyncio
from collections import defaultdict
from pathlib import Path
from typing import Annotated

import typer
from amsdal.configs.main import settings
from amsdal.manager import AmsdalManager
from amsdal.manager import AsyncAmsdalManager
from amsdal.migration.data_classes import MigrationDirection
from amsdal.migration.data_classes import MigrationFile
from amsdal.migration.data_classes import MigrationResult
from amsdal.migration.data_classes import ModuleTypes
from amsdal.migration.executors.default_executor import DefaultAsyncMigrationExecutor
from amsdal.migration.executors.default_executor import DefaultMigrationExecutor
from amsdal.migration.file_migration_executor import AsyncFileMigrationExecutorManager
from amsdal.migration.file_migration_executor import FileMigrationExecutorManager
from amsdal.migration.migrations import MigrationSchemas
from amsdal.migration.migrations_loader import MigrationsLoader
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print as rprint

from amsdal_cli.commands.build.utils.build_app import build_app
from amsdal_cli.commands.generate.enums import SOURCES_DIR
from amsdal_cli.commands.migrations.app import sub_app
from amsdal_cli.commands.migrations.constants import MIGRATIONS_DIR_NAME
from amsdal_cli.utils.cli_config import CliConfig
from amsdal_cli.utils.text import rich_info
from amsdal_cli.utils.text import rich_success
from amsdal_cli.utils.text import rich_warning


def _sync_apply(
    number: str | None,
    build_dir: Path,
    *,
    module_type: ModuleTypes,
    fake: bool,
    config_path: Path,
    app_source_path: Path,
) -> None:

    build_app(
        app_source_path=app_source_path,
        config_path=config_path,
        output=build_dir,
    )

    settings.override(APP_PATH=build_dir)
    config_manager = AmsdalConfigManager()
    config_manager.load_config(config_path)
    amsdal_manager = AmsdalManager()
    amsdal_manager.setup()
    amsdal_manager.authenticate()
    amsdal_manager.post_setup()

    app_migrations_loader = MigrationsLoader(
        migrations_dir=build_dir / MIGRATIONS_DIR_NAME,
        module_type=ModuleTypes.APP,
    )
    schemas = MigrationSchemas()
    executor = FileMigrationExecutorManager(
        app_migrations_loader=app_migrations_loader,
        executor=DefaultMigrationExecutor(schemas),
    )

    if number and number.lower().strip() == 'zero':
        number = '-1'

    result: list[MigrationResult] = executor.execute(
        migration_number=int(number) if number else None,
        module_type=module_type,
        fake=fake,
    )

    if not result:
        rprint(rich_info('Migrations are up to date'))
        return

    reverted = [item for item in result if item.direction == MigrationDirection.BACKWARD]
    applied = [item for item in result if item.direction == MigrationDirection.FORWARD]

    if reverted:
        rprint(rich_warning('Migrations reverted'))

        _render([item.migration for item in reverted], color='yellow')

    if applied:
        rprint(rich_success('Migrations applied'))

        _render([item.migration for item in applied], color='green')


async def _async_sync_apply(
    number: str | None,
    build_dir: Path,
    *,
    module_type: ModuleTypes,
    fake: bool,
    config_path: Path,
    app_source_path: Path,
) -> None:

    build_app(
        app_source_path=app_source_path,
        config_path=config_path,
        output=build_dir,
    )

    settings.override(APP_PATH=build_dir)
    config_manager = AmsdalConfigManager()
    config_manager.load_config(config_path)
    amsdal_manager = AsyncAmsdalManager()
    await amsdal_manager.setup()
    try:
        amsdal_manager.authenticate()
        await amsdal_manager.post_setup()

        app_migrations_loader = MigrationsLoader(
            migrations_dir=build_dir / MIGRATIONS_DIR_NAME,
            module_type=ModuleTypes.APP,
        )
        schemas = MigrationSchemas()
        executor = AsyncFileMigrationExecutorManager(
            app_migrations_loader=app_migrations_loader,
            executor=DefaultAsyncMigrationExecutor(schemas),
        )

        if number and number.lower().strip() == 'zero':
            number = '-1'

        result: list[MigrationResult] = await executor.execute(
            migration_number=int(number) if number else None,
            module_type=module_type,
            fake=fake,
        )

        if not result:
            rprint(rich_info('Migrations are up to date'))
            return

        reverted = [item for item in result if item.direction == MigrationDirection.BACKWARD]
        applied = [item for item in result if item.direction == MigrationDirection.FORWARD]

        if reverted:
            rprint(rich_warning('Migrations reverted'))

            _render([item.migration for item in reverted], color='yellow')

        if applied:
            rprint(rich_success('Migrations applied'))

            _render([item.migration for item in applied], color='green')
    finally:
        await amsdal_manager.teardown()


def _render(migrations: list[MigrationFile], color: str = 'yellow') -> None:
    migrations_per_type = defaultdict(list)

    for migration in migrations:
        migrations_per_type[migration.type].append(migration)

    if ModuleTypes.CORE in migrations_per_type:
        rprint(f'[{color}]Core:[/{color}]')

        for migration in migrations_per_type[ModuleTypes.CORE]:
            rprint(f'  - [{color}]{migration.path.name}[/{color}]')

    if ModuleTypes.CONTRIB in migrations_per_type:
        rprint(f'[{color}]Contrib:[/{color}]')

        for migration in migrations_per_type[ModuleTypes.CONTRIB]:
            if migration.module:
                contrib_name = '.'.join(migration.module.split('.')[:-2])
            else:
                contrib_name = 'N/A'

            rprint(f'  - [{color}]{contrib_name}: {migration.path.name}[/{color}]')

    if ModuleTypes.APP in migrations_per_type:
        rprint(f'[{color}]App:[/{color}]')

        for migration in migrations_per_type[ModuleTypes.APP]:
            rprint(f'  - [{color}]{migration.path.name}[/{color}]')


@sub_app.command(name='apply, apl, ap')
def apply_migrations(
    ctx: typer.Context,
    number: Annotated[
        str,  # noqa: RUF013
        typer.Option(
            '--number',
            '-n',
            help=(
                'Number of migration, e.g. 0002 or just 2. '
                'Use "zero" as a number to unapply all migrations including initial one.'
            ),
        ),
    ] = None,  # type: ignore[assignment]
    build_dir: Annotated[Path, typer.Option(..., '--build-dir', '-b')] = Path('.'),
    *,
    module_type: Annotated[ModuleTypes, typer.Option(..., '--module', '-m')] = ModuleTypes.APP,
    fake: Annotated[bool, typer.Option('--fake', '-f')] = False,
    config: Annotated[Path, typer.Option(..., '--config', '-c')] = None,  # type: ignore # noqa: RUF013
) -> None:
    r"""
    Apply migrations to the application.

    Args:
        ctx (typer.Context): The Typer context object.
        number (Annotated\[str, typer.Option\], optional): Number of migration, e.g. 0002 or just 2.
            Use "zero" as a number to unapply all migrations including the initial one.
        build_dir (Annotated\[Path, typer.Option\]): Directory to build the application.
        module_type (Annotated\[ModuleTypes, typer.Option\]): Type of module to apply migrations to.
        fake (Annotated\[bool, typer.Option\]): If True, fake the migration application.
        config (Annotated\[Path, typer.Option\], optional): Path to the configuration file.

    Returns:
        None
    """

    cli_config: CliConfig = ctx.meta['config']
    app_source_path = cli_config.app_directory / SOURCES_DIR
    config_path = config or cli_config.config_path
    config_manager = AmsdalConfigManager()
    config_manager.load_config(config_path)

    if config_manager.get_config().async_mode:
        asyncio.run(
            _async_sync_apply(
                build_dir=build_dir,
                module_type=module_type,
                fake=fake,
                number=number,
                config_path=config_path,
                app_source_path=app_source_path,
            )
        )
    else:
        _sync_apply(
            build_dir=build_dir,
            module_type=module_type,
            fake=fake,
            number=number,
            config_path=config_path,
            app_source_path=app_source_path,
        )
