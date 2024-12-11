from amsdal_cli.app import app
from amsdal_cli.config.main import settings

__all__ = ['app']

if __name__ == '__main__':
    app(context_settings={'settings': settings})
