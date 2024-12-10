from collections.abc import Generator
from pathlib import Path
from typing import Any

import amsdal_glue as glue
import typer
from amsdal.manager import AmsdalManager
from amsdal_data.connections.constants import CLASS_OBJECT_META
from amsdal_data.connections.constants import OBJECT_TABLE
from amsdal_data.connections.constants import PRIMARY_PARTITION_KEY
from amsdal_data.connections.constants import SECONDARY_PARTITION_KEY
from amsdal_data.connections.db_alias_map import CONNECTION_BACKEND_ALIASES
from amsdal_data.connections.historical.data_query_transform import METADATA_FIELD
from amsdal_data.connections.historical.data_query_transform import METADATA_TABLE_ALIAS
from amsdal_data.connections.historical.data_query_transform import NEXT_VERSION_FIELD
from amsdal_data.utils import object_schema_to_glue_schema
from amsdal_utils.config.data_models.amsdal_config import AmsdalConfig
from amsdal_utils.config.manager import AmsdalConfigManager
from amsdal_utils.models.data_models.enums import BaseClasses
from amsdal_utils.models.data_models.schema import ObjectSchema
from amsdal_utils.models.enums import SchemaTypes
from amsdal_utils.models.enums import Versions
from amsdal_utils.utils.classes import import_class
from amsdal_utils.utils.text import to_snake_case
from rich import print as rprint

from amsdal_cli.app import app
from amsdal_cli.commands.build.utils.build_app import build_app
from amsdal_cli.commands.generate.enums import SOURCES_DIR
from amsdal_cli.commands.restore.enums import RestoreType
from amsdal_cli.utils.cli_config import CliConfig
from amsdal_cli.utils.text import rich_info
from amsdal_cli.utils.text import rich_success


@app.command(name='restore, rst')
def restore_command(
    ctx: typer.Context,
    restore_type: RestoreType = RestoreType.MODELS,
    *,
    config: Path = typer.Option(None, help='Path to custom config.yml file'),  # noqa: B008
) -> None:
    """
    Restores the models JSON schemas to /src directory from the database.

    Args:
        ctx (typer.Context): The Typer context object.
        config (Path, optional): Path to custom config.yml file.

    Returns:
        None
    """
    cli_config: CliConfig = ctx.meta['config']

    if restore_type == RestoreType.MODELS:
        _restore_models(cli_config, config)
    else:
        _restore_state_db(cli_config, config)


def _restore_models(cli_config: CliConfig, config: Path | None) -> None:
    app_source_path = cli_config.app_directory / SOURCES_DIR

    app_source_path.mkdir(exist_ok=True)

    build_app(
        app_source_path=app_source_path,
        config_path=config or cli_config.config_path,
        output=Path('.'),
    )

    amsdal_manager = AmsdalManager()
    amsdal_manager.setup()
    amsdal_manager.authenticate()
    amsdal_manager.register_internal_classes()

    rprint(rich_info('Reading classes...'))
    class_object_model = import_class('models.core.class_object.ClassObject')
    class_objects = class_object_model.objects.filter(  # type: ignore[attr-defined]
        _address__class_version=Versions.LATEST,
        _address__object_version=Versions.LATEST,
        _metadata__is_deleted=False,
        _metadata__class_schema_type=SchemaTypes.USER,
    ).execute()

    rprint(f'[yellow]Found {len(class_objects)} classes...[/yellow]')

    for class_object in class_objects:
        class_name = class_object.object_id
        model_path = app_source_path / 'models' / to_snake_case(class_name) / 'model.json'
        rprint(rich_info(f'Restoring {class_name}...'), end=' ')
        model_path.parent.mkdir(exist_ok=True)
        model_path.write_text(class_object.class_schema)
        rprint(rich_success('Restored!'))

    rprint()
    rprint(rich_success('Done! All classes are restored.'))


def _restore_state_db(cli_config: CliConfig, config_path: Path | None) -> None:
    config_manager = AmsdalConfigManager()
    config_manager.load_config(config_path or cli_config.config_path)
    lakehouse_connection = _get_lakehouse_connection(config_manager.get_config())
    state_connection = _get_state_connection(config_manager.get_config())

    class_object_ref, class_object_meta_ref = _get_class_object_reference(lakehouse_connection)

    for table_ref, schema in _get_user_schemas(lakehouse_connection, class_object_ref, class_object_meta_ref):
        rprint(rich_info(f'Restoring {table_ref.name}'))
        glue_schema = object_schema_to_glue_schema(schema)

        state_connection.run_schema_command(
            glue.SchemaCommand(
                mutations=[
                    glue.RegisterSchema(
                        schema=glue_schema,
                    ),
                ],
            ),
        )

        for item in _get_all_latest_data(lakehouse_connection, table_ref):
            item.pop(SECONDARY_PARTITION_KEY, None)
            item.pop('_metadata', None)

            state_connection.run_mutations(
                mutations=[
                    glue.InsertData(
                        schema=glue.SchemaReference(
                            name=table_ref.name,
                            version=glue.Version.LATEST,
                        ),
                        data=[
                            glue.Data(
                                data=item,
                            ),
                        ],
                    ),
                ],
            )
            rprint('.', end='')
    rprint(rich_success('Done! All classes are restored.'))


def _get_lakehouse_connection(config: AmsdalConfig) -> glue.SqliteConnection | glue.PostgresConnection:
    connection_name = config.resources_config.lakehouse

    return _get_connection(connection_name, config)


def _get_state_connection(config: AmsdalConfig) -> glue.SqliteConnection | glue.PostgresConnection:
    connection_name = config.resources_config.repository.default  # type: ignore[union-attr]

    return _get_connection(connection_name, config)


def _get_connection(connection_name: str, config: AmsdalConfig) -> glue.SqliteConnection | glue.PostgresConnection:
    creds = config.connections[connection_name].credentials
    backend_alias = config.connections[connection_name].backend
    backend = import_class(CONNECTION_BACKEND_ALIASES.get(backend_alias, backend_alias))
    connection = backend()
    connection.connect(**creds)

    return connection


def _get_class_object_reference(
    connection: glue.SqliteConnection | glue.PostgresConnection,
) -> tuple[glue.SchemaReference, glue.SchemaReference]:
    table = glue.SchemaReference(
        name=OBJECT_TABLE,
        version='',
    )
    conditions = glue.Conditions(
        glue.Condition(
            field=glue.FieldReference(
                field=glue.Field(name=PRIMARY_PARTITION_KEY),
                table_name=table.name,
            ),
            lookup=glue.FieldLookup.EQ,
            value=glue.Value(BaseClasses.CLASS_OBJECT.value),
        ),
    )
    _add_latest_condition(conditions)

    query = glue.QueryStatement(
        table=table,
        where=conditions,
        limit=glue.LimitQuery(limit=1),
    )

    result = connection.query(query)

    if not result:
        msg = 'No class object found in the database.'
        raise ValueError(msg)

    conditions_meta = glue.Conditions(
        glue.Condition(
            field=glue.FieldReference(
                field=glue.Field(name=PRIMARY_PARTITION_KEY),
                table_name=table.name,
            ),
            lookup=glue.FieldLookup.EQ,
            value=glue.Value(CLASS_OBJECT_META),
        ),
    )
    _add_latest_condition(conditions_meta)

    query_meta = glue.QueryStatement(
        table=table,
        where=conditions_meta,
        limit=glue.LimitQuery(limit=1),
    )

    result_meta = connection.query(query_meta)

    if not result_meta:
        msg = 'No class object meta found in the database.'
        raise ValueError(msg)

    class_object_data = result[0].data
    class_object_meta_data = result_meta[0].data

    _class_object_ref = glue.SchemaReference(
        name=BaseClasses.CLASS_OBJECT.value,
        version=class_object_data[SECONDARY_PARTITION_KEY],
    )
    _class_object_meta_ref = glue.SchemaReference(
        name=CLASS_OBJECT_META,
        version=class_object_meta_data[SECONDARY_PARTITION_KEY],
    )

    return _class_object_ref, _class_object_meta_ref


def _add_latest_condition(conditions: glue.Conditions) -> None:
    conditions.children.append(
        glue.Conditions(
            glue.Condition(
                field=glue.FieldReference(
                    field=glue.Field(name=NEXT_VERSION_FIELD),
                    table_name=METADATA_TABLE_ALIAS,
                ),
                lookup=glue.FieldLookup.ISNULL,
                value=glue.Value(value=True),
            ),
            glue.Condition(
                field=glue.FieldReference(
                    field=glue.Field(name=NEXT_VERSION_FIELD),
                    table_name=METADATA_TABLE_ALIAS,
                ),
                lookup=glue.FieldLookup.EQ,
                value=glue.Value(value=''),
            ),
            connector=glue.FilterConnector.OR,
        )
    )


def _get_user_schemas(
    connection: glue.SqliteConnection | glue.PostgresConnection,
    class_object_ref: glue.SchemaReference,
    class_object_meta_ref: glue.SchemaReference,
) -> list[tuple[glue.SchemaReference, ObjectSchema]]:
    schemas = []

    for schema_data in _get_all_latest_data(connection, class_object_ref):
        class_version = schema_data.pop(SECONDARY_PARTITION_KEY, None)
        meta_conditions = glue.Conditions(
            glue.Condition(
                field=glue.FieldReference(
                    field=glue.Field(name=PRIMARY_PARTITION_KEY),
                    table_name=class_object_meta_ref.name,
                ),
                lookup=glue.FieldLookup.EQ,
                value=glue.Value(schema_data[PRIMARY_PARTITION_KEY]),
            ),
        )
        _add_latest_condition(meta_conditions)
        query_meta = glue.QueryStatement(
            table=class_object_meta_ref,
            where=meta_conditions,
            limit=glue.LimitQuery(limit=1),
        )

        result_meta = connection.query(query_meta)

        if not result_meta:
            msg = f'No class object meta found for {schema_data[PRIMARY_PARTITION_KEY]}'
            raise ValueError(msg)

        meta_data = result_meta[0].data
        meta_props = meta_data.pop('properties')
        schema_data.update(meta_data)

        if meta_props:
            for prop in meta_props:
                schema_data['properties'][prop].update(meta_props[prop])

        for name, prop in schema_data['properties'].items():
            prop['field_name'] = name

        schema_data.pop('_metadata', None)
        schema_data.pop(PRIMARY_PARTITION_KEY, None)

        schemas.append(
            (
                glue.SchemaReference(
                    name=schema_data['title'],
                    version=class_version or '',
                ),
                ObjectSchema(**schema_data),
            )
        )

    return schemas


def _get_all_latest_data(
    connection: glue.SqliteConnection | glue.PostgresConnection,
    table_ref: glue.SchemaReference,
) -> Generator[dict[str, Any], None, None]:
    is_deleted_field = glue.Field(
        name=METADATA_FIELD,
        child=glue.Field(name='is_deleted'),
    )
    is_deleted_field.child.parent = is_deleted_field  # type: ignore[union-attr]

    conditions = glue.Conditions(
        glue.Condition(
            field=glue.FieldReference(
                field=is_deleted_field,
                table_name=table_ref.name,
            ),
            lookup=glue.FieldLookup.EQ,
            value=glue.Value(False),
        ),
    )
    _add_latest_condition(conditions)

    _limit = 20
    _offset = 0

    while True:
        limit = glue.LimitQuery(limit=_limit, offset=_offset)

        query = glue.QueryStatement(
            table=table_ref,
            where=conditions,
            limit=limit,
        )

        result = connection.query(query)

        if not result:
            break

        for item in result:
            yield item.data

        _offset += _limit
