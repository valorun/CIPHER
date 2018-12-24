#!/usr/bin/python
# coding: utf-8

import logging
import json
from flask import request
from flask_socketio import SocketIO, emit
from flask_mqtt import Mqtt
from .. import socketio, raspies
from .. import mqtt

@mqtt.on_message()
def handle_mqtt_message(client, userdata, msg):
    topic = msg.topic
    data = msg.payload
    if topic == 'server/raspi_connect':
        on_raspi_connect(data['id'], data['address'])
    logging.info(data)
    print(data)

mqtt.subscribe('server/#')

def on_raspi_connect(raspi_id, address):
    logging.info("Raspberry "+str(request.remote_addr)+' connected.')
    newRaspi = {}
    newRaspi['id'] = raspi_id
    newRaspi['address'] = address
    raspies.append(newRaspi)
    get_raspies()

def on_raspi_disconnect(raspi_id):
    global raspies
    logging.info("Raspberry "+str(request.remote_addr)+' disconnected.')
    raspies = [r for r in raspies if r['id'] != raspi_id]
    get_raspies()



@socketio.on('shutdown', namespace='/client')
def shutdown():
    logging.info("Shutdown rasperries")
    mqtt.publish('raspi/shutdown', 'shutdown')
    #emit("shutdown", namespace="/raspi", broadcast=True)

@socketio.on('reboot', namespace='/client')
def reboot():
    logging.info("Reboot rasperries")
    mqtt.publish('raspi/reboot', 'reboot')
    #emit("reboot", namespace="/raspi", broadcast=True)

@socketio.on('get_raspies', namespace='/client')
def get_raspies():
    emit("get_raspies", raspies, namespace="/client", broadcast=True)
