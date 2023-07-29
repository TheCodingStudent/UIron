import json
from UIron.utils import prettify

class ConfigError(Exception):
    ...


class Config:
    def __init__(
            self, config_path: str, auto_save: bool=True, indent: int=4,
            create_new: bool=True
    ):
        
        # PROPERTIES
        self.indent = indent
        self.path = config_path
        self.config = self.load(create_new)
        self.auto_save = auto_save
    
    def load(self, create_new: bool=True) -> None:
        """Loads the configutation from json to dictionary"""
        try:
            with open(self.path, 'r') as f: config = json.load(f)
        except json.decoder.JSONDecodeError:
            raise ConfigError('Invalid json content. Please verify file...')
        except FileNotFoundError:
            if create_new: return self.new()
            raise ConfigError('No such file or directory')
        return config
    
    def new(self):
        self.config = dict()
        self.save()
        return self.config

    def save(self) -> None:
        """Saves the configuration based on dictionary"""
        with open(self.path, 'w') as f:
            json.dump(self.config, f, indent=self.indent)
    
    def __getitem__(self, key: str) -> object:
        if not key in self.config: raise ConfigError(f'Attribute "{key}" does not exist.')
        return self.config[key]
    
    def __setitem__(self, key: str, value: object) -> None:
        self.config[key] = value
        if self.auto_save: self.save()
    
    def __repr__(self) -> None:
        return prettify(self.config)