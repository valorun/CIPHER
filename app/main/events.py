#!/usr/bin/python
# coding: utf-8

import logging
from flask import request
from flask_socketio import SocketIO, emit
from .. import socketio

@socketio.on('connect', namespace='/client')
def client_connect():
	logging.info("Client "+str(request.remote_addr)+' connected.')

@socketio.on('disconnect', namespace='/client')
def client_disconnect():
    logging.info('Client '+ str(request.remote_addr) +' disconnected')
    emit("stop", namespace="/motion", broadcast=True)
