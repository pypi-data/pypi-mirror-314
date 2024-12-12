import os
import sys

from pathlib import Path


class DataDirs:

    def __init__(self, vendor_name, app_name):
        if sys.platform == "win32":
            _datadir = Path.home() / "AppData/Local"
        elif sys.platform == "linux":
            _datadir = Path.home() / ".local/share"
        elif sys.platform == "darwin":
            _datadir = Path.home() / "Library/Application Support"
        else:
            raise ValueError("Unsupported platform")

        app_data_dir = Path(_datadir).joinpath(vendor_name).joinpath(app_name)
        os.makedirs(app_data_dir, exist_ok=True)

        self.config_dir = app_data_dir
        os.makedirs(self.config_dir, exist_ok=True)

        self.log_dir = app_data_dir.joinpath('logs')
        os.makedirs(self.log_dir, exist_ok=True)
