import ast
import json
from pathlib import Path

from amsdal_utils.models.data_models.schema import ObjectSchema
from amsdal_utils.utils.text import classify
from amsdal_utils.utils.text import to_snake_case

from amsdal_cli.commands.generate.enums import MODEL_JSON_FILE
from amsdal_cli.commands.generate.enums import TestDataType
from amsdal_cli.utils.text import rich_highlight


def get_class_schema(models_dir: Path, class_name: str) -> ObjectSchema:
    model_name = classify(class_name)
    name = to_snake_case(model_name)

    model_json_path = models_dir / name / MODEL_JSON_FILE

    if not model_json_path.exists():
        msg = f'Model JSON file not found for {rich_highlight(model_name)}.'
        raise ValueError(msg)

    model_dict = json.loads(model_json_path.read_text())

    return ObjectSchema(**model_dict)


def object_creation_call(
    model_name_snake_case: str,
    object_schema: ObjectSchema,
    models_dir: Path,
    imports_set: set[tuple[str, str]],
    test_data_type: TestDataType,
) -> ast.Call:
    return ast.Call(
        func=ast.Attribute(
            value=object_init_call(model_name_snake_case, object_schema, models_dir, imports_set, test_data_type),
            attr='save',
            ctx=ast.Load(),
        ),
        args=[],
        keywords=[],
    )


def object_init_call(
    model_name_snake_case: str,
    object_schema: ObjectSchema,
    models_dir: Path,
    imports_set: set[tuple[str, str]],
    test_data_type: TestDataType,
) -> ast.Call:
    from amsdal_cli.commands.generate.utils.tests.type_utils import keywords_for_schema

    imports_set.add((f'models.user.{model_name_snake_case}', object_schema.title))

    return ast.Call(
        func=ast.Name(id=object_schema.title, ctx=ast.Load()),
        args=[],
        keywords=keywords_for_schema(object_schema, models_dir, imports_set, test_data_type=test_data_type),
    )
