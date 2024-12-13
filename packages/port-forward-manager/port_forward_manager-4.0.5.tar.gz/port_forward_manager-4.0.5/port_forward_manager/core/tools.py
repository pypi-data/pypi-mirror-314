import os
import yaml
from rich import print

from typing import List
from pydantic import BaseModel


class Settings(BaseModel):
    ports_active: List = []
    show_schema_link: bool = False
    show_table_border: bool = True
    wait_after_start: float = 0.5
    wait_after_stop: float = 0.5


base_path = os.path.expanduser('~/.pfm')
if not os.path.isdir(base_path):
    os.mkdir(base_path)

settings_file_location = os.path.join(base_path, 'pfm3.settings.yaml')

_settings: Settings = Settings()


def settings():
    return _settings


def load_yaml_file(filename: str):
    with open(os.path.expanduser(filename), "r") as stream:
        try:
            return yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)


def write_file(filename: str, data):
    with open(os.path.expanduser(filename), "w") as stream:
        try:
            stream.write(data)
        except yaml.YAMLError as exc:
            print(exc)


def load_settings():
    global _settings, settings_file_location
    # print("Load settings")

    if not os.path.isfile(settings_file_location):
        save_settings()

    loaded_settings = load_yaml_file(settings_file_location)
    _settings = Settings(**loaded_settings)
    # settings.update(loaded_settings)

    # if loaded_settings != settings:
    #    save_settings()


def save_settings():
    global _settings, settings_file_location

    print(f"[b]Updating configuration file on '{settings_file_location}'[/b]")
    with open(settings_file_location, "w") as stream:
        try:
            settings_data = _settings.dict()
            yaml.dump(settings_data, stream)
            print(settings_data)
        except yaml.YAMLError as exc:
            print(exc)


def set_ports_active(ports):
    _settings.ports_active = ports


def get_ports_active():
    return _settings.ports_active

