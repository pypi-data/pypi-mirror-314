######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.36.3+obcheckpoint(0.1.4);ob(v1)                                                   #
# Generated on 2024-12-10T22:06:22.131332                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.logs_cli
    import metaflow._vendor.click.core

from .._vendor import click as click
from ..exception import CommandException as CommandException
from ..mflog import mflog as mflog

LOGGER_TIMESTAMP: str

LOG_SOURCES: list

class CustomGroup(metaflow._vendor.click.core.Group, metaclass=type):
    def __init__(self, name = None, commands = None, default_cmd = None, **attrs):
        ...
    def get_command(self, ctx, cmd_name):
        ...
    def parse_args(self, ctx, args):
        ...
    def resolve_command(self, ctx, args):
        ...
    def format_commands(self, ctx, formatter):
        ...
    ...

class CustomFormatter(object, metaclass=type):
    def __init__(self, default_cmd, original_formatter):
        ...
    def __getattr__(self, name):
        ...
    def write_dl(self, rows):
        ...
    ...

logs: CustomGroup

