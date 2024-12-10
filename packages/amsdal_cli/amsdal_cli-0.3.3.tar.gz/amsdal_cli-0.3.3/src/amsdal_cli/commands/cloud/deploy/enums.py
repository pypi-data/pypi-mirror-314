from enum import Enum


class OutputFormat(str, Enum):
    """
    Output format for CLI commands.

    Attributes:
        default (str): Default output format.
        json (str): JSON output format.
        wide (str): Wide output format.
    """

    default = 'default'
    json = 'json'
    wide = 'wide'
