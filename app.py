#!/usr/bin/python
# coding: utf-8

from app import create_app, create_logger, socketio, mqtt
import os
import logging

app = create_app(debug=False)
logger = create_logger()

certfile=os.path.join(os.path.dirname(__file__), 'cert.pem')
keyfile=os.path.join(os.path.dirname(__file__), 'key.pem')

if __name__ == '__main__':
    logging.info("Application started")
    print("Application started")
    #socketio.run(app, host = "0.0.0.0", port = 5000, certfile=certfile, keyfile=keyfile, log=logger)
    socketio.run(app, host = "0.0.0.0", port = 5000, log=logger)