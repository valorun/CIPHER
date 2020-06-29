import traceback
from flask import request
from flask_socketio import SocketIO
from .actions import MotionAction
from cipher import socketio
from . import core


@socketio.on('connect', namespace='/client')
def client_connect():
    """
    Function called when a client connects.
    """
    core.log.info("Client " + str(request.remote_addr) + " connected.")


@socketio.on('disconnect', namespace='/client')
def client_disconnect():
    """
    Function called when a client disconnects.
    """
    core.log.info("Client " + str(request.remote_addr) + " disconnected.")
    MotionAction.execute('stop', 0)


@socketio.on_error_default
def default_error_handler(e):
    core.log.error("".join(traceback.TracebackException.from_exception(e).format()))
