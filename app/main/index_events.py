#!/usr/bin/python
# coding: utf-8

import logging
import json
from flask import request
from flask_socketio import SocketIO, emit
from .. import socketio, raspies


@socketio.on('raspi_connect', namespace='/raspi')
def raspi_connect(relay_mode, motion_mode, servo_mode):
    logging.info("Raspberry "+str(request.remote_addr)+' connected.')
    print("Raspberry "+str(request.remote_addr)+' connected.')
    newRaspi = {}
    newRaspi['sid'] = request.sid
    newRaspi['address'] = request.remote_addr
    newRaspi['relay_mode'] = relay_mode
    newRaspi['motion_mode'] = motion_mode
    newRaspi['servo_mode'] = servo_mode
    raspies.append(newRaspi)
    get_raspies();

@socketio.on('disconnect', namespace='/raspi')
def raspi_disconnect():
    global raspies
    logging.info("Raspberry "+str(request.remote_addr)+' disconnected.')
    print("Raspberry "+str(request.remote_addr)+' disconnected.')
    raspies = [r for r in raspies if r['sid'] != request.sid]
    get_raspies();



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


@socketio.on('get_raspies', namespace='/client')
def get_raspies():
    emit("get_raspies", raspies, namespace="/client", broadcast=True)

