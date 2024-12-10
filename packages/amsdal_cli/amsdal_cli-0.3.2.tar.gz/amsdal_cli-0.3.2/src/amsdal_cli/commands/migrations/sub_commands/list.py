import asyncio
from collections import defaultdict
from pathlib import Path
from typing import Annotated

import typer
from amsdal.configs.constants import CORE_MIGRATIONS_PATH
from amsdal.configs.main import settings
from amsdal.manager import AmsdalManager
from amsdal.manager import AsyncAmsdalManager
from amsdal.migration.data_classes import MigrationFile
from amsdal.migration.data_classes import ModuleTypes
from amsdal.migration.file_migration_store import AsyncFileMigrationStore
from amsdal.migration.file_migration_store import FileMigrationStore
from amsdal.migration.migrations_loader import MigrationsLoader
from amsdal.migration.utils import contrib_to_module_root_path
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print as rprint

from amsdal_cli.commands.build.utils.build_app import async_build_app
from amsdal_cli.commands.build.utils.build_app import build_app
from amsdal_cli.commands.generate.enums import SOURCES_DIR
from amsdal_cli.commands.migrations.constants import MIGRATIONS_DIR_NAME
from amsdal_cli.utils.cli_config import CliConfig
from amsdal_cli.utils.text import rich_info
from amsdal_cli.utils.text import rich_success


def _fetch_migrations() -> list[MigrationFile]:
    amsdal_manager = AmsdalManager()
    amsdal_manager.setup()
    amsdal_manager.authenticate()
    amsdal_manager.post_setup()

    store = FileMigrationStore()
    return store.fetch_migrations()


async def _async_fetch_migrations() -> list[MigrationFile]:
    amsdal_manager = AsyncAmsdalManager()
    await amsdal_manager.setup()
    try:
        amsdal_manager.authenticate()
        await amsdal_manager.post_setup()

        store = AsyncFileMigrationStore()
        return await store.fetch_migrations()
    finally:
        await amsdal_manager.teardown()


def list_migrations(
    ctx: typer.Context,
    build_dir: Annotated[Path, typer.Option('--build-dir', '-b')] = Path('.'),
    *,
    config: Annotated[Path, typer.Option('--config', '-c')] = None,  # type: ignore # noqa: RUF013
) -> None:
    r"""
    Show all migrations, which are applied and not applied including CORE and CONTRIB migrations.

    Args:
        ctx (typer.Context): The Typer context object.
        build_dir (Annotated\[Path, typer.Option\]): Directory to build the application.
        config (Annotated\[Path, typer.Option\], optional): Path to the configuration file.

    Returns:
        None
    """

    if ctx.invoked_subcommand is not None:
        return

    cli_config: CliConfig = ctx.meta['config']
    app_source_path = cli_config.app_directory / SOURCES_DIR
    config_path = config or cli_config.config_path
    config_manager = AmsdalConfigManager()
    config_manager.load_config(config_path)

    if config_manager.get_config().async_mode:
        async_build_app(
            app_source_path=app_source_path,
            config_path=config_path,
            output=build_dir,
        )
        _all_applied_migrations = asyncio.run(_async_fetch_migrations())

    else:
        build_app(
            app_source_path=app_source_path,
            config_path=config_path,
            output=build_dir,
        )
        _all_applied_migrations = _fetch_migrations()

    _core_applied_numbers = [_m.number for _m in _all_applied_migrations if _m.type == ModuleTypes.CORE]
    _app_applied_numbers = [_m.number for _m in _all_applied_migrations if _m.type == ModuleTypes.APP]
    _contrib_applied_numbers: dict[str, list[int]] = defaultdict(list)

    for _m in _all_applied_migrations:
        if _m.type == ModuleTypes.CONTRIB and _m.module:
            _contrib_applied_numbers[_m.module].append(_m.number)

    core_loader = MigrationsLoader(
        migrations_dir=CORE_MIGRATIONS_PATH,
        module_type=ModuleTypes.CORE,
    )
    contrib_loaders: list[tuple[str, MigrationsLoader]] = []

    for contrib in settings.CONTRIBS:
        contrib_root_path = contrib_to_module_root_path(contrib)

        contrib_loaders.append(
            (
                contrib,
                MigrationsLoader(
                    migrations_dir=contrib_root_path / settings.MIGRATIONS_DIRECTORY_NAME,
                    module_type=ModuleTypes.CONTRIB,
                    module_name=contrib,
                ),
            ),
        )

    app_migrations_loader = MigrationsLoader(
        migrations_dir=build_dir / MIGRATIONS_DIR_NAME,
        module_type=ModuleTypes.APP,
    )

    rprint(rich_success('Core:'))

    for _migration in core_loader:
        _is_migrated = 'x' if _migration.number in _core_applied_numbers else ' '
        _color = 'green' if _is_migrated == 'x' else 'grey'
        rprint(rf'[{_color}]  - \[{_is_migrated}] {_migration.path.name}[/{_color}]')

    rprint(rich_success('Contrib:'))
    for _contrib, _loader in contrib_loaders:
        _contrib_name = _contrib.rsplit('.', 2)[0]
        _applied_numbers = _contrib_applied_numbers[_contrib]

        for _migration in _loader:
            _is_migrated = 'x' if _migration.number in _applied_numbers else ' '
            _color = 'green' if _is_migrated == 'x' else 'grey'
            rprint(rf'[{_color}]  - \[{_is_migrated}] {_contrib_name}: {_migration.path.name}[/{_color}]')

    _app_migration_files = list(app_migrations_loader)

    if _app_migration_files:
        rprint(rich_success('App:'))

        for _migration in _app_migration_files:
            _is_migrated = 'x' if _migration.number in _app_applied_numbers else ' '
            _color = 'green' if _is_migrated == 'x' else 'grey'
            rprint(rf'[{_color}]  - \[{_is_migrated}] {_migration.path.name}[/{_color}]')
    else:
        rprint(rich_info("You don't have any migrations in your app"))
