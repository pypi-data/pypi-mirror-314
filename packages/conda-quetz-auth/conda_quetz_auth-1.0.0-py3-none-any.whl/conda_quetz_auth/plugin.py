"""
A place to register plugin hooks
"""
from conda.cli.conda_argparse import BUILTIN_COMMANDS
from conda.plugins import CondaAuthHandler, CondaPreCommand, CondaSubcommand, hookimpl

from .handlers import TokenAuthHandler
from .constants import PLUGIN_NAME


ENV_COMMANDS = {
    "env_config",
    "env_create",
    "env_export",
    "env_list",
    "env_remove",
    "env_update",
}

BUILD_COMMANDS = {
    "build",
    "convert",
    "debug",
    "develop",
    "index",
    "inspect",
    "metapackage",
    "render",
    "skeleton",
}


@hookimpl
def conda_auth_handlers():
    """
    Registers auth handlers
    """
    yield CondaAuthHandler(name="dp-quetz-auth", handler=TokenAuthHandler)