#!/usr/bin/python
# coding: utf-8

import logging
from flask import request
from flask_socketio import SocketIO, emit
from app import socketio

@socketio.on('connect', namespace='/client')
def client_connect():
    """
    Function called when a client connects.
    """
    logging.info("Client "+str(request.remote_addr)+' connected.')

@socketio.on('disconnect', namespace='/client')
def client_disconnect():
    """
    Function called when a client disconnects.
    """
    logging.info('Client '+ str(request.remote_addr) +' disconnected')
    emit("stop", namespace="/motion", broadcast=True)