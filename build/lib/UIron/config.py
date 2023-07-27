import json


class ConfigError(Exception):
    ...


class Config:
    def __init__(self, config_path: str):
        
        # PROPERTIES
        self.path = config_path
        self.config = self.load()
    
    def load(self) -> None:
        """Loads the configutation from json to dictionary"""
        try:
            with open(self.path, 'r') as f: config = json.load(f)
        except json.decoder.JSONDecodeError:
            raise ConfigError('Invalid json content. Please verify file...')
        return config
    
    def save(self) -> None:
        """Saves the configuration based on dictionary"""
        with open(self.path, 'w') as f:
            json.dump(self.config, f)
    
    def __getitem__(self, key: str) -> object:
        if not key in self.config: raise ConfigError(f'Attribute "{key}" does not exist.')
        return self.config[key]