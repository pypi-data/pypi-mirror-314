import marops_cli.groups.base as base
import marops_cli.groups.setup as setup
import marops_cli.groups.poetry as poetry
from marops_cli.helpers import is_dev_version, get_marops_version
from marops_cli.banner import get_banner
import click
import os


def cli():
    dev_mode = is_dev_version()
    version = get_marops_version()
    mode = "Developer" if dev_mode else "User"
    banner = get_banner(mode, version)

    os.environ["MAROPS_CLI_DEV_MODE"] = "true" if dev_mode else "false"

    @click.group(help=banner)
    def marops_cli():
        pass

    marops_cli.add_command(base.configure)
    marops_cli.add_command(base.config)
    marops_cli.add_command(base.upgrade)
    marops_cli.add_command(base.up)
    marops_cli.add_command(base.restart)
    marops_cli.add_command(base.down)
    marops_cli.add_command(base.authenticate)

    if dev_mode:
        marops_cli.add_command(base.build)
        marops_cli.add_command(base.env)
        marops_cli.add_command(setup.setup)
        setup.setup.add_command(setup.secrets)

        marops_cli.add_command(poetry.poetry)
        poetry.poetry.add_command(poetry.install)
        poetry.poetry.add_command(poetry.lock)
        poetry.poetry.add_command(poetry.update)
        poetry.poetry.add_command(poetry.test)
        poetry.poetry.add_command(poetry.pyright)


    marops_cli()


if __name__ == "__main__":
    cli()
