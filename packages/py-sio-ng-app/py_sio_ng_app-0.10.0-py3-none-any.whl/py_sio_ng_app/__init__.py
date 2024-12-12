import logging
import socket
from typing import Callable, Any

from .backend import SocketioBackend
from .backend.socketio_server import SioMessage
from .config import Config
from .frontend import WebviewAngularFrontend

logger = logging.getLogger(__name__)


class PySioNgApp:
    def __init__(self, vendor_name, app_name, app_version, ng_dist_path,
                 event_callback: Callable[[SioMessage], None],
                 socketio_port=None, app_config_class=None):
        self._config = Config(vendor_name=vendor_name, app_name=app_name, app_config_class=app_config_class)
        if socketio_port is None:
            socketio_port = self._get_free_tcp_port()
        self._backend = SocketioBackend(event_callback=event_callback,
                                        exception_handler=self.kill, socketio_port=socketio_port)
        self._frontend = WebviewAngularFrontend(title=app_name + ' v' + app_version,
                                                ng_dist_path=ng_dist_path, socketio_port=socketio_port)

    @staticmethod
    def _get_free_tcp_port():
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind(('', 0))
        addr, port = tcp.getsockname()
        tcp.close()
        return port

    def set_event_callback(self, event_callback: Callable[[SioMessage], None]):
        self._backend.set_event_callback(event_callback)

    def emit(self, event: Any, data: Any, sid: str = None):
        serialized_data = 'null'
        try:
            serialized_data = data.to_json()
        except Exception as e:
            pass

        self._backend.emit(message=SioMessage(event_name=event.value, serialized_data=serialized_data, sid=sid))

    def start(self, launch_frontend=True):
        logger.info('Starting backend')
        self._backend.start(blocking=not launch_frontend)
        if launch_frontend:
            logger.info('Starting frontend')
            self._frontend.start_blocking()
        logger.info('App exit')

    def kill(self):
        self._backend.stop()
        self._frontend.web_window.destroy()

    def get_app_config(self):
        return self._config.app.get()

    def update_app_config(self, new_config):
        return self._config.app.update(new_config=new_config)

    def get_app_config_dir(self):
        return self._config.data_dirs.config_dir
