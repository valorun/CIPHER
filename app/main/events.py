#!/usr/bin/python
# coding: utf-8

import logging
from flask import request
from flask_socketio import SocketIO, emit
from .. import socketio


@socketio.on('client_connect', namespace='/client')
def client_connect():
	logging.info("Client "+str(request.remote_addr)+' connected.')

@socketio.on('disconnect', namespace='/client')
def client_disconnect():
    logging.info('Client '+ str(request.remote_addr) +' disconnected')
    emit("stop", namespace="/servo", broadcast=True)


@socketio.on('shutdown', namespace='/client')
def shutdown():
    logging.info("Shutdown rasperries")
    emit("shutdown", namespace="/raspi", broadcast=True)
    #os.system('shutdown -h now')

@socketio.on('reboot', namespace='/client')
def reboot():
    logging.info("Reboot rasperries")
    emit("reboot", namespace="/raspi", broadcast=True)
    #os.system('reboot -h now')

