import logging
from dataclasses import dataclass

from dataclasses_json import dataclass_json
from queue import Queue
from threading import Thread

import eventlet
import socketio


@dataclass_json
@dataclass
class SioMessage:
    event_name: str
    serialized_data: str
    sid: str = None


logger = logging.getLogger(__name__)


class SocketioServer(Thread):

    def __init__(self, name, port):
        logger.info('SocketioServer ' + name + ' created.')

        Thread.__init__(self, name=name, daemon=True)
        self.port = port
        self.queue = Queue()
        self._emitter_queue = Queue()
        self.sio = socketio.Server(cors_allowed_origins='*')
        self.app = socketio.WSGIApp(self.sio, static_files={
            '/': {'content_type': 'text/html', 'filename': 'index.html'}
        })
        self._set_event_handlers()

    def message_available(self):
        return not self.queue.empty()

    def get_message(self):
        if not self.queue.empty():
            message: SioMessage = self.queue.get()
            return message
        return None

    def _set_event_handlers(self):
        @self.sio.event
        def connect(sid, environ):
            logger.info('Connected SID: %s', sid)

        @self.sio.event
        def disconnect(sid):
            logger.info('Disconnected SID: %s', sid)

        @self.sio.on('*')
        def default_handler(event_name, sid, serialized_data):
            try:
                logger.info('Message RX:\n\t>> RX Event: %s\n\t>> RX Data: %s\n\t>> FROM SID: <%s>',
                            event_name, serialized_data, sid)
                message = SioMessage(sid=sid, event_name=event_name, serialized_data=serialized_data)
                self.queue.put(message)
            except Exception as e:
                logger.error(e)

    def _emitter(self):
        while True:
            while not self._emitter_queue.empty():
                try:
                    message: SioMessage = self._emitter_queue.get()
                    logger.info('Message TX:\n\t>> TX Event: %s\n\t>> TX Payload: %s\n\t>> TO SID: <%s>',
                                message.event_name, message.serialized_data, message.sid)
                    self.sio.emit(message.event_name, message.serialized_data, room=message.sid)
                except Exception as e:
                    logger.error(e)
            self.sio.sleep(.01)

    def emit(self, message: SioMessage):
        self._emitter_queue.put(message)

    def run(self):
        self.sio.start_background_task(self._emitter)
        eventlet.wsgi.server(eventlet.listen(('127.0.0.1', self.port)), self.app)
