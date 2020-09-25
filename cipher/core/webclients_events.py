import traceback
from flask import request
from flask_socketio import SocketIO, emit
from .actions import MotionAction
from .clients_events import clients
from cipher import socketio
from . import core


@socketio.on('connect', namespace='/client')
def webclient_connect():
    """
    Function called when a client connects.
    """
    core.log.info("Webclient " + str(request.remote_addr) + " connected.")
    emit('receive_clients', clients, namespace='/client', broadcast=False)


@socketio.on('disconnect', namespace='/client')
def webclient_disconnect():
    """
    Function called when a client disconnects.
    """
    core.log.info("Webclient " + str(request.remote_addr) + " disconnected.")
    MotionAction.execute('stop', 0)


@socketio.on_error_default
def default_error_handler(e):
    core.log.error("".join(traceback.TracebackException.from_exception(e).format()))
