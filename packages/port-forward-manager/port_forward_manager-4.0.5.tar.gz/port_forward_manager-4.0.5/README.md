# Port Forward Manager (PFM)
PFM allows quick and easy management of ports forwarded over SSH (local or remote).

# Installation

```
# Install tmux
brew install tmux
# Install python poetry https://python-poetry.org/docs/
brew install poetry
or
curl -sSL https://install.python-poetry.org | python3 -

# Install PFM
pip install --upgrade port-forward-manager

# If you get the error "This environment is externally managed" then you can do:
# find /opt/homebrew -name EXTERNALLY-MANAGED
# 
# With the file that was found you just have to delete it or change the name like:
# sudo mv /opt/homebrew/Cellar/python@3.12/3.12.5/Frameworks/Python.framework/Versions/3.12/lib/python3.12/EXTERNALLY-MANAGED /opt/homebrew/Cellar/python@3.12/3.12.5/Frameworks/Python.framework/Versions/3.12/lib/python3.12/EXTERNALLY-MANAGED.old

```

Settings file is stored in ~/.ssh/pfm.settings.yaml

## Configure autocomplete

Add to end of ~/.zshrc

```
fpath+=~/.zfunc

autoload -Uz compinit
compinit
zstyle ':completion:*' menu select

```

Generate autocomplete configuration

```
pfm --install-completion

# If gives error: ModuleNotFoundError: No module named 'pkg_resources'
# Run: pip3 install setuptools

source .zshrc
```
# About
## Settings
PFM will automatically generate a default configuration file and update new settings to their default values.


### show_schema_link
Toggle the ability to show/hide the schema when showing the list of schemas.
### wait_after_start 
How long, in seconds, to wait after starting sessions.
### table_border
Toggle the table border
### show_pid
Toggle the screen PID

Example settings file:
```
schemas:
    local_proxy:
      - hostname: some.proxy.host
        remote_port: 8888
        type: local
    remote-server:
      - hostname: example.host
        local_port: 1234
        remote_port: 8080
        type: local
      - hostname: example.host
        local_port: 8888
        remote_port: 8888
        type: local
show_pid: 'false'
show_schema_link: 'false'
table_border: 'true'
wait_after_start: '0.5'
wait_after_stop: 0.5
```

## Commands
### config
Show active sessions
### forward
Start a forwarding session
### schemas
List configured schemas
### shutdown
Stop all active sessions
### start
Start a schema of forwarding sessions
### status
Show active sessions
### stop
Stop sessions from active schema, host or port
###version
Show installed version

# Development
Setup development environment
```
git clone git@github.com:kxiros/port-forward-manager.git
cd port-forward-manager
poetry shell
poetry install
```

Building python package

```
python -m build
```


To Install development version:

```
pip install -e cloned_directory_path
```

Release
```
#Example to github
gh release create 1.3 dist/port-forward-manager-1.3.tar.gz -t "Minor fixes" --generate-notes

#Publish on Pypi
# Configure pypi token
# poetry config pypi-token.pypi <token>
poetry publish
```