#!/usr/bin/python3
# coding: utf-8

from app import create_app, setup_logger, socketio, mqtt
import os
import logging

certfile=os.path.join(os.path.dirname(__file__), 'cert.pem')
keyfile=os.path.join(os.path.dirname(__file__), 'key.pem')

if __name__ == '__main__':
    setup_logger(debug=True)
    app = create_app(debug=True)
    logging.info("Application started")
    #print("Application started")
    #socketio.run(app, host = "0.0.0.0", port = 5000, certfile=certfile, keyfile=keyfile)
    socketio.run(app, host = "0.0.0.0", port = 5000)