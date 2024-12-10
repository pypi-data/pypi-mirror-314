from pathlib import Path

from amsdal.configs.main import settings
from amsdal.manager import AmsdalManager
from amsdal.manager import AsyncAmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print as rprint

from amsdal_cli.commands.build.utils.build_config_file import build_config_file
from amsdal_cli.utils.text import rich_info
from amsdal_cli.utils.text import rich_success
from amsdal_cli.utils.text import rich_warning


def build_app(
    app_source_path: Path,
    config_path: Path,
    output: Path = Path('.'),
) -> None:
    """
    Builds the application by processing transactions, models, static files, fixtures, and migrations.

    Args:
        app_source_path (Path): The path to the application's source code.
        config_path (Path): The path to the configuration file.
        output (Path, optional): The output directory for the built files. Defaults to the current directory.

    Returns:
        None
    """
    _build_app(app_source_path=app_source_path, config_path=config_path, output=output, manager_class=AmsdalManager)


def async_build_app(
    app_source_path: Path,
    config_path: Path,
    output: Path = Path('.'),
) -> None:
    """
    Builds the application by processing transactions, models, static files, fixtures, and migrations.

    Args:
        app_source_path (Path): The path to the application's source code.
        config_path (Path): The path to the configuration file.
        output (Path, optional): The output directory for the built files. Defaults to the current directory.

    Returns:
        None
    """
    _build_app(
        app_source_path=app_source_path, config_path=config_path, output=output, manager_class=AsyncAmsdalManager
    )


def _build_app(
    app_source_path: Path,
    config_path: Path,
    output: Path = Path('.'),
    manager_class: type[AmsdalManager] | type[AsyncAmsdalManager] = AmsdalManager,
) -> None:
    settings.override(APP_PATH=output)
    config_manager = AmsdalConfigManager()
    config_manager.load_config(config_path)
    amsdal_manager = manager_class()
    amsdal_manager.pre_setup()

    rprint(rich_info('Building transactions...'), end=' ')
    amsdal_manager.build_transactions(app_source_path)
    rprint(rich_success('OK!'))

    rprint(rich_info('Building models...'), end=' ')
    amsdal_manager.build_models(app_source_path / 'models')
    rprint(rich_success('OK!'))

    if output == Path('.'):
        rprint(rich_warning('No output directory specified, skipping config.yml generation.'))
    else:
        # build config file
        build_config_file(
            output_path=output,
            config_path=config_path,
            no_input=True,
        )

    rprint(rich_info('Building static files...'), end=' ')
    amsdal_manager.build_static_files(app_source_path)
    rprint(rich_success('OK!'))

    rprint(rich_info('Building fixtures...'), end=' ')
    amsdal_manager.build_fixtures(app_source_path / 'models')
    rprint(rich_success('OK!'))

    rprint(rich_info('Building migrations...'), end=' ')
    amsdal_manager.build_migrations(app_source_path)
    rprint(rich_success('OK!'))
