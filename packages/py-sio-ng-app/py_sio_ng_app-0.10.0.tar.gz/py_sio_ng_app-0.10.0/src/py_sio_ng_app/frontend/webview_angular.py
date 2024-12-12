import logging
from pathlib import Path

import webview

logger = logging.getLogger(__name__)


class JsApi:

    def __init__(self, socketio_port):
        self._socketio_port = socketio_port

    def get_socketio_port(self):
        return self._socketio_port


class WebviewAngularFrontend:

    def __init__(self, title, ng_dist_path: Path, socketio_port: int) -> None:
        self._js_api = JsApi(socketio_port=socketio_port)
        self.web_window = webview.create_window(title,
                                                str(ng_dist_path.joinpath('index.html')),
                                                height=750, width=1024, js_api=self._js_api)

    @staticmethod
    def start_blocking():
        logger.info('Starting WebviewAngularFrontend')
        webview.start()  # Blocks until app exit
