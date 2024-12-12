import logging
import os
from enum import Enum
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from pathlib import Path

from src.py_sio_ng_app import PySioNgApp, SioMessage

logger = logging.getLogger(__name__)


class EventCodes(Enum):
    REQ_APP_PING = 'REQ_APP_PING'
    REP_APP_PONG = 'REP_APP_PONG'
    REQ_APP_GET_CONFIG = 'REQ_APP_GET_CONFIG'
    REQ_APP_SET_CONFIG = 'REQ_APP_SET_CONFIG'
    REP_APP_CONFIG = 'REP_APP_CONFIG'


@dataclass_json
@dataclass
class SimpleAppConfig:
    username: str = None
    token: str = None


class SimpleApp:

    def __init__(self, sio_port=None, launch_frontend=True):
        ng_dist_path = (Path(os.path.dirname(__file__)).joinpath('ng-project').
                        joinpath('dist').joinpath('ng-project').joinpath('browser'))
        self._ng_app = PySioNgApp(
            vendor_name='Kliskatek',
            app_name='SimpleApp',
            app_version='1.0',
            app_config_class=SimpleAppConfig,
            ng_dist_path=ng_dist_path,
            socketio_port=sio_port,
            event_callback=self._event_callback)
        self._ng_app.start(launch_frontend=launch_frontend)

    def _event_callback(self, message: SioMessage):
        event = EventCodes(message.event_name)
        if event == EventCodes.REQ_APP_PING:
            self._ng_app.emit(event=EventCodes.REP_APP_PONG,
                              data=None,
                              sid=message.sid)
        if event == EventCodes.REQ_APP_GET_CONFIG:
            self._ng_app.emit(event=EventCodes.REP_APP_CONFIG,
                              data=self._ng_app.get_app_config(),
                              sid=message.sid)
            return
        if event == EventCodes.REQ_APP_SET_CONFIG:
            req_config: SimpleAppConfig = SimpleAppConfig.from_json(message.serialized_data)
            self._ng_app.update_app_config(new_config=req_config)
            self._ng_app.emit(event=EventCodes.REP_APP_CONFIG,
                              data=self._ng_app.get_app_config(),
                              sid=message.sid)
            return

