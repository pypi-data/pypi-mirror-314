from amsdal_cli.app import app
from amsdal_cli.commands.tests.app import sub_app
from amsdal_cli.commands.tests.sub_commands import *  # noqa

app.add_typer(sub_app, name='tests, test')
