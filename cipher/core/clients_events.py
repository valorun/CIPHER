import logging
from flask import request
from flask_socketio import SocketIO
from .actions import motion
from cipher import socketio

@socketio.on('connect', namespace='/client')
def client_connect():
    """
    Function called when a client connects.
    """
    logging.info('Client ' + str(request.remote_addr) + ' connected.')

@socketio.on('disconnect', namespace='/client')
def client_disconnect():
    """
    Function called when a client disconnects.
    """
    logging.info('Client ' + str(request.remote_addr) + ' disconnected.')
    motion('stop', 0)

@socketio.on_error_default
def default_error_handler(e):
    logging.error(e)
