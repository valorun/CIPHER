#!/usr/bin/python
# coding: utf-8

from app import create_app, create_logger, socketio
import os
import logging

app = create_app(debug=False)
logger = create_logger()

certfile=os.path.join(os.path.dirname(__file__), 'cert.pem')
keyfile=os.path.join(os.path.dirname(__file__), 'key.pem')

if __name__ == '__main__':
    #socketio.run(app, host = "0.0.0.0", port = 5000, certfile=certfile, keyfile=keyfile)
    socketio.run(app, host = "0.0.0.0", port = 5000, log=logger)
    logging.info("Application started")