# MarOps CLI

Publicly available on [PyPi](https://pypi.org/project/marops-cli/) for convenience but if you don't work at Greenroom Robotics, you probably don't want to use this.

## Install

* For development:
  * `pip install -e ./libs/marops_config`
  * `pip install -e ./tools/marops_cli`
* For production: `pip install marops-cli`
* You may also need to `export PATH=$PATH:~/.local/bin` if you don't have `~/.local/bin` in your path
* Install autocomplete:
  * bash: `echo 'eval "$(_MAROPS_COMPLETE=bash_source marops)"' >> ~/.bashrc`
  * zsh: `echo 'eval "$(_MAROPS_COMPLETE=zsh_source marops)"' >> ~/.zshrc` (this is much nicer)
  * If using zsh, the git checker plugin make terminal slow. Suggest you run `git config oh-my-zsh.hide-info 1` in the zsh terminal inside the repo

## Usage

* `marops --help` to get help with the CLI

## Dev mode

MarOps CLI can be ran in dev mode. This will happen if it is installed with `pip install -e ./tools/marops` or if the environment variable `MAROPS_CLI_DEV_MODE` is set to `true`.