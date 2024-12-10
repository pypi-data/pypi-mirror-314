import json
from typing import Any

import typer
from amsdal_utils.utils.text import classify
from amsdal_utils.utils.text import to_snake_case
from rich import print as rprint

from amsdal_cli.commands.generate.app import sub_app
from amsdal_cli.commands.generate.enums import MODEL_JSON_FILE
from amsdal_cli.commands.generate.enums import SOURCES_DIR
from amsdal_cli.commands.generate.enums import ModelFormat
from amsdal_cli.commands.generate.utils.model_attributes import parse_attributes
from amsdal_cli.utils.cli_config import CliConfig
from amsdal_cli.utils.copier import write_file
from amsdal_cli.utils.text import rich_error


@sub_app.command(name='model, mdl, md')
def generate_model(
    ctx: typer.Context,
    model_name: str = typer.Argument(
        ...,
        help='The model name. It should be provided in PascalCase.',
    ),
    model_format: ModelFormat = typer.Option(ModelFormat.JSON.value, '--format'),  # noqa: B008
    attrs: list[str] = typer.Option(  # noqa: B008
        (None,),
        '--attributes',
        '-attrs',
    ),
    unique: list[str] = typer.Option(  # noqa: B008
        (None,),
        '--unique',
        '-u',
    ),
) -> None:
    """Generates model file.

    Example of usage:

    ```bash
    amsdal generate model UserProfile --format json -attrs "name:string email:string:index age:number:default=18"
    ```

    So the format of attribute definition is: `<name>:<type>[:<options>]`

    Supported types:

    - string - Example: `position:string`
    - number - Example: `age:number`
    - boolean - Example: `is_active:boolean`
    - dict - Example: `metadata:dict:string:Country` (equivalent to `metadata: dict[str, Country]` in Python)
    - belongs-to - Example: `user:belongs-to:User` (equivalent to `user: User` in Python)
    - has-many - Example: `posts:has-many:Post` (equivalent to `posts: list[Post]` in Python)

    Where "belongs-to" and "has-many" are used to define the relationship between models. The "belongs-to" type is used
    to define the relationship where the model has a reference to another model. The "has-many" type is used to define
    the relationship where the model has a list of references to another model.

    The options are:

    * index - to mark the attribute as indexed. Example: `email:string:index`
    * unique - to mark the attribute as unique. Example: `email:string:unique`
    * required - to mark the attribute as required. Example: `email:string:required`
    * default - to set the default value for the attribute. It should be provided in the format: `default=<value>`.
    Example: `age:number:default=18 name:string:default=Developer`
    In order to put multi-word default values, you should use quotes. Example:

    ```bash
    amsdal generate model Person -attrs "name:string:default='John Doe'"
    ```

    Note, `dict` type does not support default value due to its complex structure.

    The options can be combined. Examples:
    - `email:string:unique:required`
    - `meta:dict:string:string:required:unique`
    - `age:number:default=18:required`
    - `name:string:default='John Doe':required`

     The ordering of the options does not matter.
    """

    if model_format == ModelFormat.PY:
        rprint(rich_error('The PY format is not supported for now.'))
        raise typer.Exit

    cli_config: CliConfig = ctx.meta['config']
    model_name = classify(model_name)
    name = to_snake_case(model_name)

    output_path = cli_config.app_directory / SOURCES_DIR / 'models' / name
    parsed_attrs = parse_attributes(attrs)

    schema: dict[str, Any] = {
        'title': model_name,
        'type': 'object',
        'properties': {},
        'required': [attr.name for attr in parsed_attrs if attr.required],
        'indexed': [attr.name for attr in parsed_attrs if attr.index],
    }

    unique_attrs: list[str | tuple[str, ...]] = [attr.name for attr in parsed_attrs if attr.unique]

    for _unique in filter(None, unique):
        _unique_attrs = tuple(map(str.strip, _unique.split(',')))

        if _unique_attrs not in unique_attrs:
            unique_attrs.append(_unique_attrs)

    if unique_attrs:
        schema['unique'] = unique_attrs

    for attr in parsed_attrs:
        property_info: dict[str, Any] = {
            'title': attr.name,
            'type': attr.json_type,
        }

        if attr.has_items:
            property_info['items'] = attr.json_items

        if attr.default != attr.NotSet:
            property_info['default'] = attr.default

        schema['properties'][attr.name] = property_info

    write_file(
        json.dumps(schema, indent=cli_config.json_indent),
        destination_file_path=output_path / MODEL_JSON_FILE,
        confirm_overwriting=True,
    )
