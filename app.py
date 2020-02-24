#!/usr/bin/python3
# coding: utf-8

from cipher import create_app, setup_logger, socketio, mqtt
from cipher.config import core_config
from os.path import join, dirname
import logging

certfile = join(dirname(__file__), 'cert.pem')
keyfile = join(dirname(__file__), 'key.pem')

DEBUG = core_config.get_debug_mode()
if __name__ == '__main__':
    setup_logger(debug=DEBUG)
    app = create_app(debug=DEBUG)
    logging.info("Application started")
    if DEBUG:
        socketio.run(app, host='0.0.0.0', port=5000)
    else:
        socketio.run(app, host='0.0.0.0', port=5000, certfile=certfile, keyfile=keyfile)
