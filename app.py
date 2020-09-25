#!/usr/bin/python3
# coding: utf-8

from cipher import create_app, setup_logger, socketio, mqtt
from cipher.config import core_config
from os.path import join, dirname
import logging

DEBUG = core_config.DEBUG
if __name__ == '__main__':
    setup_logger(debug=DEBUG)
    app = create_app(debug=DEBUG)
    logging.info("Application started")
    socketio.run(app, host='0.0.0.0', port=5000)
