import os
from typing import List, Optional
import json

import click
import glob
import subprocess
from python_on_whales.docker_client import DockerClient
from python_on_whales.utils import ValidPath

import marops_config
from marops_config import MarOpsConfig

from marops_cli.helpers import (
    get_project_root,
    call,
)

def get_packages(package_name: Optional[str] = None):
    root_dir = get_project_root()
    pyproject_paths = glob.glob("projects/plugins/**/pyproject.toml", recursive=True, root_dir=root_dir)
    package_paths = [root_dir / os.path.dirname(package_path) for package_path in pyproject_paths]
    if package_name:
        return [package_path for package_path in package_paths if package_name == os.path.basename(package_path)]
    else:
        return package_paths


@click.group(help="Poetry commands")
def poetry():
    pass


@click.command(name="install")
@click.argument(
    "package_name",
    required=False,
    nargs=1,
)
def install(package_name: Optional[str]):
    """Installs poetry deps"""
    packages = get_packages(package_name)
    for package in packages:
        subprocess.call("poetry install", shell=True, executable="/bin/bash", cwd=package)


@click.command(name="lock")
@click.argument(
    "package_name",
    required=False,
    nargs=1,
)
def lock(package_name: Optional[str]):
    """Lock poetry deps"""
    packages = get_packages(package_name)
    for package in packages:
        click.echo(click.style(f"Running lock for '{os.path.basename(package)}'", fg="green"))
        subprocess.call("poetry lock", shell=True, executable="/bin/bash", cwd=package)

@click.command(name="update")
@click.argument(
    "package_name",
    required=False,
    nargs=1,
)
def update(package_name: Optional[str]):
    """Update poetry deps"""
    packages = get_packages(package_name)
    for package in packages:
        click.echo(click.style(f"Running update for '{os.path.basename(package)}'", fg="green"))
        subprocess.call("poetry update", shell=True, executable="/bin/bash", cwd=package)

@click.command(name="test")
@click.argument(
    "package_name",
    required=False,
    nargs=1,
)
def test(package_name: Optional[str]):
    """Run pytest"""
    packages = get_packages(package_name)

    has_error = False
    for package in packages:
        click.echo(click.style(f"Running tests for '{os.path.basename(package)}'", fg="green"))
        error = subprocess.call("poetry run pytest -vv", shell=True, executable="/bin/bash", cwd=package)
        if error:
            has_error = True
    if has_error:
        raise click.ClickException("At least one test failed")


@click.command(name="pyright")
@click.argument(
    "package_name",
    required=False,
    nargs=1,
)
def pyright(package_name: Optional[str]):
    """Run pyright"""
    packages = get_packages(package_name)

    has_error = False
    for package in packages:
        click.echo(click.style(f"Running typecheck for '{os.path.basename(package)}'", fg="green"))
        error = subprocess.call("poetry run pyright", shell=True, executable="/bin/bash", cwd=package)
        if error:
            has_error = True
    if has_error:
        raise click.ClickException("At least one test failed")
