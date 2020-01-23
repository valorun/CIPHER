#!/usr/bin/python3
# coding: utf-8

from cipher import create_app, setup_logger, socketio, mqtt
import os
import logging

certfile = os.path.join(os.path.dirname(__file__), 'cert.pem')
keyfile = os.path.join(os.path.dirname(__file__), 'key.pem')

DEBUG = True

if __name__ == '__main__':
    setup_logger(debug=DEBUG)
    app = create_app(debug=DEBUG)
    logging.info("Application started")
    if DEBUG:
        socketio.run(app, host='0.0.0.0', port=5000)
    else:
        socketio.run(app, host='0.0.0.0', port=5000, certfile=certfile, keyfile=keyfile)
