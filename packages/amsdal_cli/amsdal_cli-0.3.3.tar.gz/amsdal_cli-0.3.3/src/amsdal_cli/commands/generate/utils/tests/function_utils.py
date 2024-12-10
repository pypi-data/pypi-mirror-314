import ast


def test_function_arguments() -> ast.arguments:
    return ast.arguments(
        posonlyargs=[],
        args=[],
        vararg=None,
        kwonlyargs=[],
        kw_defaults=[],
        kwarg=None,
        defaults=[],
    )


def test_function_decorator_list() -> list[ast.expr]:
    return []
