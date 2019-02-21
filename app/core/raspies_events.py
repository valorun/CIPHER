import logging
import json
from flask_socketio import SocketIO, emit
from flask_mqtt import Mqtt
from app import socketio, mqtt

raspies = []

@mqtt.on_connect()
def on_server_connect(client, userdata, flags, rc):
    """
    Function called when the server connects to the broker.
    """
    mqtt.publish("server/connect")

@mqtt.on_topic('server/raspi_connect')
def on_raspi_connect(client, userdata, msg):
    """
    Function called when a raspberry client connects.
    """
    global raspies
    data = json.loads(msg.payload)
    raspi_id = data['id']
    logging.info('Raspberry '+raspi_id+' connected.')
    newRaspi = {}
    newRaspi['id'] = raspi_id
    #newRaspi['address'] = address
    mqtt.subscribe("raspi/"+raspi_id+"/#")
    raspies = [r for r in raspies if r['id'] != raspi_id] #delete already existing one with the same id
    raspies.append(newRaspi)
    socketio.emit("get_raspies", raspies, namespace="/client", broadcast=True)

@mqtt.on_topic('server/raspi_disconnect')
def on_raspi_disconnect(client, userdata, msg):
    """
    Function called when a raspberry client disconnects.
    """
    global raspies
    data = json.loads(msg.payload)
    raspi_id = data['id']
    logging.info('Raspberry '+raspi_id+' disconnected.')
    raspies = [r for r in raspies if r['id'] != raspi_id]
    mqtt.unsubscribe("raspi/"+raspi_id+"/#")
    socketio.emit("get_raspies", raspies, namespace="/client", broadcast=True)


@socketio.on('shutdown', namespace='/client')
def shutdown():
    logging.info("Shutdown rasperries")
    mqtt.publish('raspi/shutdown', 'shutdown')

@socketio.on('reboot', namespace='/client')
def reboot():
    logging.info("Reboot rasperries")
    mqtt.publish('raspi/reboot', 'reboot')

@socketio.on('get_raspies', namespace='/client')
def get_raspies():
    emit("get_raspies", raspies, namespace="/client", broadcast=True)