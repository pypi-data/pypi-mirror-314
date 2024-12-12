import json
import os
from typing import Any


class AppConfig:

    def __init__(self, config_dir, app_config_class):
        self.config_dir = config_dir
        self.current_config: Any = None

        # Check if file exist
        if os.path.exists(config_dir.joinpath('config.json')):
            with open(config_dir.joinpath('config.json'), 'r') as f:
                self.current_config = app_config_class(**json.load(f))
        else:
            self.update(new_config=app_config_class())

    def get(self):
        return self.current_config

    def update(self, new_config: Any):
        with open(self.config_dir.joinpath('config.json'), 'w') as f:
            f.write(new_config.to_json(indent=4))
        self.current_config = new_config
