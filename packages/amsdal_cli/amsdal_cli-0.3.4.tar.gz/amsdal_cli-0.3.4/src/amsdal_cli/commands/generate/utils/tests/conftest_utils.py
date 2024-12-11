from pathlib import Path

from amsdal_cli.commands.generate.enums import SOURCES_DIR
from amsdal_cli.utils.cli_config import CliConfig

CURRENT_DIR = Path(__file__).parent


def create_conftest_if_not_exist(cli_config: CliConfig) -> None:
    test_dir = cli_config.app_directory / SOURCES_DIR / 'tests'
    test_dir.mkdir(parents=True, exist_ok=True)
    conftest_file_path = test_dir / 'conftest.py'

    if not conftest_file_path.exists():
        with open(CURRENT_DIR / 'templates' / 'conftest.py') as f:
            conftest_file_path.write_text(f.read())
