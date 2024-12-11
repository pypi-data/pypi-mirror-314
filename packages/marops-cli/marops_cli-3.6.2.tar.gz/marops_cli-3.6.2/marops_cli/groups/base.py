import os
from typing import List
import json

import click
import subprocess
from python_on_whales.docker_client import DockerClient
from python_on_whales.utils import ValidPath

import marops_config
from marops_config import MarOpsConfig

from marops_cli.helpers import (
    docker_compose_path,
    get_project_root,
    call,
    get_marops_version,
)



SERVICES = [
    "marops_ui",
    "marops_core",
    "marops_docs",
    "marops_hasura",
    "marops_chart_tiler",
    "marops_chart_api",
    "marops_rsync",
    "postgres",
    "plugins",
    "studio",
    "traefik"
]

def marops_config_read():
    config = marops_config.read()
    version = get_marops_version()

    if version != "latest" and not config.prod:
        click.echo(click.style(f"Setting config.prod to True.", fg="red"))
        click.echo(click.style(f"You cannot run MarOps in developer mode when using the production vesion of marops-cli", fg="red"))
        config.prod = True

    return config


def _get_compose_files(config: MarOpsConfig) -> List[ValidPath]:
    compose_files: List[ValidPath] = [
        docker_compose_path("./docker-compose.base.yaml")
    ]
    if config.prod:
        compose_files.append(docker_compose_path("./docker-compose.prod.yaml"))
    else:
        compose_files.append(docker_compose_path("./docker-compose.dev.yaml"))
    
    if config.proxy:
        compose_files.append(docker_compose_path("./docker-compose.demo.yaml"))

    return compose_files


def _log_config(config: MarOpsConfig):
    click.echo(click.style("[+] MarOps Config:", fg="green"))
    for attr, value in config.__dict__.items():
        click.echo(
            click.style(f" ⠿ {attr}: ".ljust(26), fg="white") + click.style(str(value), fg="green")
        )

def _set_config_to_env(config: MarOpsConfig):
    os.environ["MAROPS_VERSION"] = get_marops_version()
    os.environ["MAROPS_DATA_PATH"] = config.data_path
    os.environ["MAROPS_BACKUP_PATH"] = config.backup_path
    os.environ["SECURE_COOKIE"] = "true" if config.secure_cookie else "false"
    os.environ["HASURA_GRAPHQL_ADMIN_SECRET"] = config.hasura_admin_secret
    os.environ["COMPOSE_PROJECT_NAME"] = "marops"

    # key must be at least 32 characters long
    os.environ["HASURA_GRAPHQL_JWT_SECRET"] = json.dumps({
        "type":"HS256",
        "key": f"{config.hasura_admin_secret.zfill(32)}-:^)",
        "header":{"type": "Cookie", "name": "token" }
    })
    os.environ["PROXY_HOST"] = config.proxy_host

    return os.environ


@click.command(name="build")
@click.argument(
    "services",
    required=False,
    nargs=-1,
    type=click.Choice(SERVICES),
)
def build(services: List[str]):
    """Builds MarOps"""
    config = marops_config_read()
    _set_config_to_env(config)

    docker_dev = DockerClient(
        compose_files=_get_compose_files(config),
        compose_project_directory=get_project_root(),
    )
    services_list = list(services) if services else None
    docker_dev.compose.build(cache=True, services=services_list)


@click.command(name="up")
@click.option(
    "--build",
    help="Should we do a docker build",
    is_flag=True,
)
@click.option(
    "--pull",
    help="Should we do a docker pull",
    is_flag=True,
)
@click.argument(
    "services",
    required=False,
    nargs=-1,
    type=click.Choice(SERVICES),
)
def up(build: bool, pull: bool, services: List[str]):
    """Starts MarOps"""
    config = marops_config_read()
    _log_config(config)
    _set_config_to_env(config)

    docker = DockerClient(
        compose_files=_get_compose_files(config),
        compose_project_directory=get_project_root(),
    )
    services_list = list(services) if services else None
    docker.compose.up(detach=True, build=build, services=services_list, pull="always" if pull else "missing")
   
@click.command(name="restart")
@click.argument(
    "services",
    required=False,
    nargs=-1,
    type=click.Choice(SERVICES),
)
def restart(services: List[str]):
    """Starts MarOps"""
    config = marops_config_read()
    _log_config(config)
    _set_config_to_env(config)

    docker = DockerClient(
        compose_files=_get_compose_files(config),
        compose_project_directory=get_project_root(),
    )
    services_list = list(services) if services else None
    docker.compose.restart(services=services_list)
   


@click.command(name="down")
@click.argument("args", nargs=-1)
def down(args: List[str]):
    """Stops MarOps"""
    config = marops_config_read()
    _log_config(config)
    _set_config_to_env(config)

    docker = DockerClient(
        compose_files=_get_compose_files(config),
        compose_project_directory=get_project_root(),
    )
    docker.compose.down()


@click.command(name="upgrade")
@click.option("--version", help="The version to upgrade to.")
def upgrade(version: str):
    """Upgrade MarOps CLI"""
    click.echo(f"Current version: {get_marops_version()}")
    result = click.prompt(
        "Are you sure you want to upgrade?", default="y", type=click.Choice(["y", "n"])
    )
    if result == "n":
        return

    if version:
        click.echo(click.style("Upgrading marops-config...", fg="blue"))
        call(f"pip install --upgrade marops-config=={version}")
        click.echo(click.style("Upgrading marops-cli...", fg="blue"))
        call(f"pip install --upgrade marops-cli=={version}")
    else:
        click.echo(click.style("Upgrading marops-config...", fg="blue"))
        call("pip install --upgrade marops-config")
        click.echo(click.style("Upgrading marops-cli...", fg="blue"))
        call("pip install --upgrade marops-cli")

    click.echo(click.style("Upgrade of MarOps CLI complete.", fg="green"))
    click.echo(
        click.style(
            "Run `marops up` to upgrade MarOps.", fg="green"
        )
    )


@click.command(name="authenticate")
@click.option(
    "--username",
    help="The username to use for authentication.",
    required=True,
    prompt=True,
)
@click.option("--token", help="The token to use for authentication.", required=True, prompt=True)
def authenticate(username: str, token: str):
    """
    Authenticate with the MarOps package repository so that you can pull images.

    To get a username and token you'll need to contact a Greenroom Robotics employee.
    """
    call(f"echo {token} | docker login ghcr.io -u {username} --password-stdin")


@click.command(name="configure")
@click.option("--default", is_flag=True, help="Use default values")
def configure(default: bool):  # type: ignore
    """Configure MarOps"""

    if default:
        config = MarOpsConfig()
        marops_config.write(config)
    else:
        # Check if the file exists
        if os.path.exists(marops_config.get_path()):
            click.echo(
                click.style(
                    f"MarOps config already exists: {marops_config.get_path()}",
                    fg="yellow",
                )
            )
            result = click.prompt(
                "Do you want to overwrite it?", default="y", type=click.Choice(["y", "n"])
            )
            if result == "n":
                return

        try:
            config_current = marops_config_read()
        except Exception:
            config_current = MarOpsConfig()

        config = MarOpsConfig(
            prod=click.prompt(
                "Prod Mode",
                default=config_current.prod,
                type=bool,
            ),
            data_path=click.prompt(
                "Data Path", default=config_current.data_path
            ),
            backup_path=click.prompt(
                "Backup Path", default=config_current.backup_path
            ),
            hasura_admin_secret=click.prompt(
                "Hasura Admin Secret", default=config_current.hasura_admin_secret
            ),
            secure_cookie=click.prompt(
                "Secure Cookie", default=config_current.secure_cookie, type=bool,
            ),
            proxy=click.prompt(
                "Proxy Mode", default=config_current.proxy, type=bool,
            ),
            proxy_host=click.prompt(
                "Proxy Host", default=config_current.proxy_host,
            ),
        )
        marops_config.write(config)



@click.command(name="config")
def config():  # type: ignore
    """Read Config"""
    config = marops_config_read()
    _log_config(config)
    _set_config_to_env(config)
    click.echo(click.style(f"path: {marops_config.get_path()}", fg="blue"))

@click.command(name="env")
@click.argument("args", nargs=-1)
def env(args: List[str]):  # type: ignore
    """Source env and run a command"""
    config = marops_config_read()
    _log_config(config)
    _set_config_to_env(config)
    subprocess.run(args, shell=True, check=True)
