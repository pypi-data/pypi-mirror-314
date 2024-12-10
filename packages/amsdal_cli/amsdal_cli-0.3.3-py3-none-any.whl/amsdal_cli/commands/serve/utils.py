import shutil
import sys
from pathlib import Path

from amsdal.configs.constants import CORE_MIGRATIONS_PATH
from amsdal.configs.main import settings
from amsdal.manager import AmsdalManager
from amsdal.manager import AsyncAmsdalManager
from amsdal.migration.base_migration_schemas import DefaultMigrationSchemas
from amsdal.migration.data_classes import MigrationFile
from amsdal.migration.data_classes import ModuleTypes
from amsdal.migration.executors.state_executor import StateMigrationExecutor
from amsdal.migration.file_migration_executor import FileMigrationExecutorManager
from amsdal.migration.file_migration_generator import AsyncFileMigrationGenerator
from amsdal.migration.file_migration_generator import FileMigrationGenerator
from amsdal.migration.file_migration_store import AsyncFileMigrationStore
from amsdal.migration.file_migration_store import FileMigrationStore
from amsdal.migration.migrations import MigrateData
from amsdal.migration.migrations_loader import MigrationsLoader
from amsdal.migration.schemas_loaders import JsonClassSchemaLoader
from amsdal.migration.utils import contrib_to_module_root_path
from amsdal_utils.config.manager import AmsdalConfigManager
from amsdal_utils.models.enums import SchemaTypes
from rich import print as rprint

from amsdal_cli.commands.generate.enums import SOURCES_DIR
from amsdal_cli.commands.migrations.constants import MIGRATIONS_DIR_NAME
from amsdal_cli.utils.text import CustomConfirm
from amsdal_cli.utils.text import rich_error
from amsdal_cli.utils.text import rich_info
from amsdal_cli.utils.text import rich_success
from amsdal_cli.utils.text import rich_warning


def cleanup_app(output_path: Path, *, remove_warehouse: bool = True) -> None:
    """
    Cleanup the generated models and files after stopping.

    Args:
        output_path (Path): The path to the output directory.
        remove_warehouse (bool, optional): If True, remove the warehouse directory. Defaults to True.

    Returns:
        None
    """

    for path in (
        (output_path / 'migrations'),
        (output_path / 'models'),
        (output_path / 'schemas'),
        (output_path / 'fixtures'),
        (output_path / 'static'),
    ):
        if not path.exists():
            continue
        shutil.rmtree(str(path.resolve()))

    warehouse_path = output_path / 'warehouse'

    if remove_warehouse and warehouse_path.exists():
        shutil.rmtree(str(warehouse_path.resolve()))


def build_app_and_check_migrations(
    output_path: Path,
    app_source_path: Path,
    config_path: Path,
    *,
    apply_fixtures: bool = True,
    confirm_migrations: bool | None = False,
) -> AmsdalManager:
    """
    Builds the application and checks for migrations.

    Args:
        output_path (Path): The path to the output directory.
        app_source_path (Path): The path to the application source directory.
        config_path (Path): The path to the configuration file.
        apply_fixtures (bool, optional): If True, apply fixtures to the database. Defaults to True.
        confirm_migrations (bool, optional): If True, confirm migrations before proceeding. Defaults to False.

    Returns:
        AmsdalManager: The Amsdal manager instance.
    """
    settings.override(APP_PATH=output_path)

    config_manager = AmsdalConfigManager()
    config_manager.load_config(config_path)

    amsdal_manager = AmsdalManager()
    amsdal_manager.pre_setup()

    rprint(rich_info('Building transactions...'), end=' ')
    amsdal_manager.build_transactions(app_source_path)
    rprint(rich_success('OK!'))

    rprint(rich_info('Building models...'), end=' ')
    amsdal_manager.build_models(app_source_path / 'models')
    rprint(rich_success('OK!'))

    rprint(rich_info('Building migrations...'), end=' ')
    amsdal_manager.build_migrations(app_source_path)
    rprint(rich_success('OK!'))

    has_unapplied = check_migrations_generated_and_applied(
        app_path=app_source_path.parent,
        build_dir=output_path,
        amsdal_manager=amsdal_manager,
    )

    if confirm_migrations and has_unapplied:
        run_server = CustomConfirm.ask(
            rich_info('Do you want to run server anyway?'),
            default=False,
            show_default=False,
            choices=['y', 'N'],
        )

        if not run_server:
            rprint(rich_error('Exiting...'))
            sys.exit(1)
    elif confirm_migrations is None:
        pass
    elif has_unapplied:
        rprint(rich_error('Exiting...'))
        sys.exit(1)

    rprint(rich_info('Building fixtures...'), end=' ')
    amsdal_manager.build_fixtures(app_source_path / 'models')
    rprint(rich_success('OK!'))

    if apply_fixtures:
        rprint(rich_info('Applying fixtures...'), end=' ')
        if not amsdal_manager.is_setup:
            amsdal_manager.setup()

        amsdal_manager.post_setup()
        amsdal_manager.init_classes()

        if not amsdal_manager.is_authenticated:
            amsdal_manager.authenticate()

        amsdal_manager.apply_fixtures()
        rprint(rich_success('OK!'))

    return amsdal_manager


def check_migrations_generated_and_applied(
    app_path: Path,
    build_dir: Path,
    amsdal_manager: AmsdalManager,
) -> bool:
    """
    Check if migrations are generated and applied.

    Args:
        app_path (Path): The path to the application directory.
        build_dir (Path): The path to the build directory.
        amsdal_manager (AmsdalManager): The Amsdal manager instance.

    Returns:
        bool: True if there are unapplied migrations, False otherwise.
    """
    if not amsdal_manager.is_setup:
        amsdal_manager.setup()

    if not amsdal_manager.is_authenticated:
        amsdal_manager.authenticate()

    amsdal_manager.post_setup()

    has_unapplied_migrations = _check_has_unapplied_migrations(build_dir=build_dir)

    if has_unapplied_migrations:
        return True

    return _check_migrations_generated_and_applied(app_path=app_path)


def _check_migrations_generated_and_applied(
    app_path: Path,
) -> bool:
    app_source_path = app_path / SOURCES_DIR
    schema_loader = JsonClassSchemaLoader(app_source_path / 'models')
    migrations_dir = app_source_path / MIGRATIONS_DIR_NAME

    generator = FileMigrationGenerator(
        schema_loader=schema_loader,
        app_migrations_path=migrations_dir,
    )

    operations = generator.generate_operations(SchemaTypes.USER)

    if operations:
        rprint(
            rich_warning(
                'WARNING: you have changes in our models. Use "amsdal migrations new" to generate migrations.',
            )
        )

        return True
    return False


def _check_has_unapplied_migrations(
    build_dir: Path,
) -> bool:
    store = FileMigrationStore()
    all_applied_migrations = store.fetch_migrations()
    core_loader = MigrationsLoader(
        migrations_dir=CORE_MIGRATIONS_PATH,
        module_type=ModuleTypes.CORE,
    )
    schemas = DefaultMigrationSchemas()

    if _check_has_unapplied_migrations_per_loader(core_loader, all_applied_migrations, schemas):
        return True

    for contrib in settings.CONTRIBS:
        contrib_root_path = contrib_to_module_root_path(contrib)

        if _check_has_unapplied_migrations_per_loader(
            MigrationsLoader(
                migrations_dir=contrib_root_path / settings.MIGRATIONS_DIRECTORY_NAME,
                module_type=ModuleTypes.CONTRIB,
                module_name=contrib,
            ),
            all_applied_migrations,
            schemas,
        ):
            return True

    return _check_has_unapplied_migrations_per_loader(
        MigrationsLoader(
            migrations_dir=build_dir / MIGRATIONS_DIR_NAME,
            module_type=ModuleTypes.APP,
        ),
        all_applied_migrations,
        schemas,
    )


def _check_has_unapplied_migrations_per_loader(
    core_loader: MigrationsLoader,
    all_applied_migrations: list[MigrationFile],
    schemas: DefaultMigrationSchemas,
) -> bool:
    for _migration in core_loader:
        if not _is_migration_applied(_migration, all_applied_migrations):
            rprint(
                rich_warning(
                    'WARNING: you have not applied all core migrations. '
                    'Use "amsdal migrations apply" to apply them.',
                )
            )

            return True
        else:
            # Register classes from migrations
            migration_class = FileMigrationExecutorManager.get_migration_class(_migration)
            migration_class_instance = migration_class()
            state_executor = StateMigrationExecutor(
                schemas,
                do_fetch_latest_version=True,
            )

            for _operation in migration_class_instance.operations:
                if isinstance(_operation, MigrateData):
                    continue

                _operation.forward(state_executor)

    return False


def _is_migration_applied(
    migration: MigrationFile,
    all_applied_migrations: list[MigrationFile],
) -> bool:
    for applied_migration in all_applied_migrations:
        if (
            migration.type == applied_migration.type
            and migration.number == applied_migration.number
            and migration.module == applied_migration.module
        ):
            return True

    return False


async def async_build_app_and_check_migrations(
    output_path: Path,
    app_source_path: Path,
    config_path: Path,
    *,
    apply_fixtures: bool = True,
    confirm_migrations: bool | None = False,
) -> AsyncAmsdalManager:
    """
    Builds the application and checks for migrations.

    Args:
        output_path (Path): The path to the output directory.
        app_source_path (Path): The path to the application source directory.
        config_path (Path): The path to the configuration file.
        apply_fixtures (bool, optional): If True, apply fixtures to the database. Defaults to True.
        confirm_migrations (bool, optional): If True, confirm migrations before proceeding. Defaults to False.

    Returns:
        AmsdalManager: The Amsdal manager instance.
    """
    settings.override(APP_PATH=output_path)

    config_manager = AmsdalConfigManager()
    config_manager.load_config(config_path)

    amsdal_manager = AsyncAmsdalManager()
    amsdal_manager.pre_setup()
    try:

        rprint(rich_info('Building transactions...'), end=' ')
        amsdal_manager.build_transactions(app_source_path)
        rprint(rich_success('OK!'))

        rprint(rich_info('Building models...'), end=' ')
        amsdal_manager.build_models(app_source_path / 'models')
        rprint(rich_success('OK!'))

        rprint(rich_info('Building migrations...'), end=' ')
        amsdal_manager.build_migrations(app_source_path)
        rprint(rich_success('OK!'))

        has_unapplied = await async_check_migrations_generated_and_applied(
            app_path=app_source_path.parent,
            build_dir=output_path,
            amsdal_manager=amsdal_manager,
        )

        if confirm_migrations and has_unapplied:
            run_server = CustomConfirm.ask(
                rich_info('Do you want to run server anyway?'),
                default=False,
                show_default=False,
                choices=['y', 'N'],
            )

            if not run_server:
                rprint(rich_error('Exiting...'))
                sys.exit(1)
        elif confirm_migrations is None:
            pass
        elif has_unapplied:
            rprint(rich_error('Exiting...'))
            sys.exit(1)

        rprint(rich_info('Building fixtures...'), end=' ')
        amsdal_manager.build_fixtures(app_source_path / 'models')
        rprint(rich_success('OK!'))

        if apply_fixtures:
            rprint(rich_info('Applying fixtures...'), end=' ')
            if not amsdal_manager.is_setup:
                await amsdal_manager.setup()

            await amsdal_manager.post_setup()
            amsdal_manager.init_classes()

            if not amsdal_manager.is_authenticated:
                amsdal_manager.authenticate()

            await amsdal_manager.apply_fixtures()
            rprint(rich_success('OK!'))
    except Exception:
        await amsdal_manager.teardown()

        raise

    return amsdal_manager


async def async_check_migrations_generated_and_applied(
    app_path: Path,
    build_dir: Path,
    amsdal_manager: AsyncAmsdalManager,
) -> bool:
    """
    Check if migrations are generated and applied.

    Args:
        app_path (Path): The path to the application directory.
        build_dir (Path): The path to the build directory.
        amsdal_manager (AsyncAmsdalManager): The Amsdal manager instance.

    Returns:
        bool: True if there are unapplied migrations, False otherwise.
    """
    if not amsdal_manager.is_setup:
        await amsdal_manager.setup()

    if not amsdal_manager.is_authenticated:
        amsdal_manager.authenticate()

    await amsdal_manager.post_setup()

    has_unapplied_migrations = await _async_check_has_unapplied_migrations(build_dir=build_dir)

    if has_unapplied_migrations:
        return True

    return await _async_check_migrations_generated_and_applied(app_path=app_path)


async def _async_check_has_unapplied_migrations(
    build_dir: Path,
) -> bool:
    store = AsyncFileMigrationStore()
    await store._init_migration_table()
    all_applied_migrations = await store.fetch_migrations()
    core_loader = MigrationsLoader(
        migrations_dir=CORE_MIGRATIONS_PATH,
        module_type=ModuleTypes.CORE,
    )
    schemas = DefaultMigrationSchemas()

    if _check_has_unapplied_migrations_per_loader(core_loader, all_applied_migrations, schemas):
        return True

    for contrib in settings.CONTRIBS:
        contrib_root_path = contrib_to_module_root_path(contrib)

        if _check_has_unapplied_migrations_per_loader(
            MigrationsLoader(
                migrations_dir=contrib_root_path / settings.MIGRATIONS_DIRECTORY_NAME,
                module_type=ModuleTypes.CONTRIB,
                module_name=contrib,
            ),
            all_applied_migrations,
            schemas,
        ):
            return True

    return _check_has_unapplied_migrations_per_loader(
        MigrationsLoader(
            migrations_dir=build_dir / MIGRATIONS_DIR_NAME,
            module_type=ModuleTypes.APP,
        ),
        all_applied_migrations,
        schemas,
    )


async def _async_check_migrations_generated_and_applied(
    app_path: Path,
) -> bool:
    app_source_path = app_path / SOURCES_DIR
    schema_loader = JsonClassSchemaLoader(app_source_path / 'models')
    migrations_dir = app_source_path / MIGRATIONS_DIR_NAME

    generator = AsyncFileMigrationGenerator(
        schema_loader=schema_loader,
        app_migrations_path=migrations_dir,
    )

    operations = await generator.generate_operations(SchemaTypes.USER)

    if operations:
        rprint(
            rich_warning(
                'WARNING: you have changes in our models. Use "amsdal migrations new" to generate migrations.',
            )
        )

        return True
    return False
