import logging
import time
from threading import Thread
from typing import Callable

from .socketio_server import SocketioServer, SioMessage

logger = logging.getLogger(__name__)


class SocketioBackend:

    def __init__(self, socketio_port: int, event_callback: Callable[[SioMessage], None] = None,
                 exception_handler: Callable[[], None] = None):
        self._event_callback: Callable[[SioMessage], None] = event_callback
        self._exception_handler: Callable[[], None] = exception_handler
        self._tcp_port = socketio_port
        self._sio = SocketioServer('sio', self._tcp_port)
        self._thread = Thread(target=self._main, daemon=True)
        self._running = False

    def set_event_callback(self, event_callback: Callable[[SioMessage], None]):
        self._event_callback = event_callback

    def set_exception_handler(self, handler: Callable[[], None]):
        self._exception_handler = handler

    def start_nonblocking(self):
        self._running = True
        self._sio.start()
        self._thread.start()

    def start_blocking(self):
        self._running = True
        self._sio.start()
        self._main()

    def start(self, blocking: bool):
        if blocking:
            self.start_blocking()
        else:
            self.start_nonblocking()

    def stop(self):
        self._running = False

    def emit(self, message: SioMessage):
        self._sio.emit(message)

    def _main(self):
        try:
            logger.info('Starting backend on port {}'.format(self._tcp_port))
            while self._running:
                if self._sio.message_available():
                    message: SioMessage = self._sio.get_message()
                    if self._event_callback:
                        self._event_callback(message)
                time.sleep(0.01)
        except Exception as e:
            logger.error(e)
            if self._exception_handler is not None:
                self._exception_handler()
