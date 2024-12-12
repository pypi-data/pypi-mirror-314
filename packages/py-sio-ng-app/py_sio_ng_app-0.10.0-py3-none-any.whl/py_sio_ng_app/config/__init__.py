from .app import AppConfig
from .datadirs import DataDirs
from .logging import initialize_logging


class Config:
    def __init__(self, vendor_name, app_name, app_config_class=None):
        self._vendor_name = vendor_name
        self._app_name = app_name
        self.data_dirs = DataDirs(self._vendor_name, self._app_name)
        initialize_logging(self.data_dirs.log_dir.joinpath(self._app_name + '.log'))
        if app_config_class:
            self.app = AppConfig(config_dir=self.data_dirs.config_dir, app_config_class=app_config_class)
