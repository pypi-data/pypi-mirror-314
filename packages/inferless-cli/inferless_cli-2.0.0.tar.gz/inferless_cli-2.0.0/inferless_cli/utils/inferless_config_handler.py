import rich

from inferless_cli.utils.constants import (
    DEFAULT_INFERLESS_YAML_FILE,
    DEFAULT_YAML_FILE_NAME,
)
from inferless_cli.utils.exceptions import ConfigurationError
from inferless_cli.utils.helpers import create_yaml, log_exception, yaml


class InferlessConfigHandler:
    def __init__(self):
        self.data = self.load_config(False)
        self.regions = []

    @staticmethod
    def load_config(yaml_data):
        try:
            if not yaml_data:
                yaml_data = DEFAULT_INFERLESS_YAML_FILE
            return yaml.load(yaml_data)
        except FileNotFoundError:
            log_exception("Unable to load default error")
            rich.print("[red]Unable to load default error[/red]")
            raise ConfigurationError("Unable to load default error")

    def save_config(self, config_file=None):
        if not config_file:
            config_file = DEFAULT_YAML_FILE_NAME
        if "configuration" in self.data:
            del self.data["configuration"]
        if "env" in self.data:
            del self.data["env"]
        if "optional" in self.data:
            del self.data["optional"]
        if "io_schema" in self.data:
            del self.data["io_schema"]
        
        create_yaml(self.data, config_file)

    def update_config(self, key, value):
        keys = key.split(".")
        config = self.data
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value

    def get_value(self, key):
        keys = key.split(".")
        config = self.data
        for k in keys:
            if k in config:
                config = config[k]
            else:
                return None
        return config

    def set_loaded_config(self, config):
        self.data = config

    def set_regions(self, regions):
        self.regions = regions

    def get_regions(self):
        return self.regions
