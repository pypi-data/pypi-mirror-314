from typing import List, Optional, Dict, Any
import click
import os
from pathlib import Path
import subprocess
import platform
import pkg_resources


def get_project_root() -> Path:
    current_file_dir = Path(__file__).parent
    return current_file_dir.parent.parent.parent


def get_marops_version():
    """MarOps version is latest if it is a dev version otherwise it is the CLI version"""
    version = pkg_resources.require("marops-cli")[0].version
    if version == "0.0.0":
        version = "latest"
    return version


def is_dev_version():
    if os.environ.get("MAROPS_CLI_DEV_MODE") == "false":
        return False

    if os.environ.get("MAROPS_CLI_DEV_MODE") == "true":
        return True
    return pkg_resources.require("marops_cli")[0].version == "0.0.0"


def docker_compose_path(path: str) -> Path:
    current_file_dir = Path(__file__).parent
    return current_file_dir / "docker" / path


def get_docker_file_args(files: List[str]):
    return "-f " + " -f ".join(files)


def get_args_str(args: List[str]):
    return " ".join(args)


def call(command: str, abort: bool=True, env: Optional[Dict[str, Any]]=None):
    click.echo(click.style(f"Running: {command}", fg="blue"))
    if env:
        env = {**os.environ, **env}

    prj_root = get_project_root()
    error = subprocess.call(command, shell=True, executable="/bin/bash", cwd=prj_root, env=env)
    if error and abort:
        raise click.ClickException("Failed")


def get_arch():
    arch = platform.machine()
    if arch == "x86_64":
        return "amd64"
    elif arch == "aarch64":
        return "arm64"
    else:
        print(f"Unsupported arch: {arch}")
        exit(1)
