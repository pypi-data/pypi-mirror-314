import json

import typer
from amsdal.manager import AmsdalManager
from amsdal.manager import AsyncAmsdalManager
from amsdal_models.schemas.loaders.cli_fixtures_loader import FIXTURES
from amsdal_utils.config.manager import AmsdalConfigManager
from amsdal_utils.utils.text import to_snake_case

from amsdal_cli.commands.generate.app import sub_app
from amsdal_cli.commands.generate.utils.build_base_path import build_model_base_path
from amsdal_cli.utils.cli_config import CliConfig
from amsdal_cli.utils.copier import write_file


@sub_app.command(name='permission, p')
def generate_permission(
    ctx: typer.Context,
    model: str = typer.Option(..., help='The model name. It should be provided in PascalCase.'),
    *,
    create: bool = typer.Option(True, help="Generate 'create' permission."),
    read: bool = typer.Option(True, help="Generate 'read' permission."),
    update: bool = typer.Option(True, help="Generate 'update' permission."),
    delete: bool = typer.Option(True, help="Generate 'delete' permission."),
) -> None:
    """
    Generates permission fixture file for specified model.

    Args:
        ctx (typer.Context): The Typer context object.
        model (str): The model name. It should be provided in PascalCase.
        create (bool): Generate 'create' permission.
        read (bool): Generate 'read' permission.
        update (bool): Generate 'update' permission.
        delete (bool): Generate 'delete' permission.

    Returns:
        None
    """
    cli_config: CliConfig = ctx.meta['config']
    config_manager = AmsdalConfigManager()
    config_manager.load_config(cli_config.config_path)

    amsdal_manager: AsyncAmsdalManager | AmsdalManager
    if config_manager.get_config().async_mode:
        amsdal_manager = AsyncAmsdalManager()
        amsdal_manager.pre_setup()
    else:
        amsdal_manager = AmsdalManager()
        amsdal_manager.pre_setup()

    model_snake_case = to_snake_case(model)
    expected_permissions = []
    for permission_needed, permission_name in [
        (create, 'create'),
        (read, 'read'),
        (update, 'update'),
        (delete, 'delete'),
    ]:
        if permission_needed:
            expected_permissions.append(
                {
                    'external_id': f'{model_snake_case}_{permission_name}',
                    'model': model,
                    'action': permission_name,
                }
            )

    base_path = build_model_base_path(ctx, model)
    (base_path / FIXTURES).mkdir(parents=True, exist_ok=True)
    permissions_file = base_path / FIXTURES / 'permissions.json'

    if permissions_file.exists():
        permission_fixtures = json.loads(permissions_file.read_text())

        if not permission_fixtures.get('Permission'):
            permission_fixtures['Permission'] = []

    else:
        permission_fixtures = {'Permission': []}

    for permission in expected_permissions:
        if permission not in permission_fixtures['Permission']:
            permission_fixtures['Permission'].append(permission)

    write_file(
        json.dumps(permission_fixtures, indent=cli_config.json_indent),
        destination_file_path=permissions_file,
        confirm_overwriting=False,
    )
