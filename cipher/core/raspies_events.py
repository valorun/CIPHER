import json
from flask_socketio import SocketIO, emit
from flask_mqtt import Mqtt
from cipher import socketio, mqtt
from cipher.model import Relay
from . import core

raspies = []


@mqtt.on_connect()
def on_server_connect(client, userdata, flags, rc):
    """
    Function called when the server connects to the broker.
    """
    mqtt.publish('server/connect')


@mqtt.on_topic('server/raspi_connect')
def on_raspi_connect(client, userdata, msg):
    """
    Function called when a raspberry client connects.
    """
    global raspies
    data = json.loads(msg.payload.decode('utf-8'))
    raspi_id = data['id']
    core.log.info("Raspberry " + raspi_id + " connected.")
    new_raspi = {}
    new_raspi['id'] = raspi_id
    mqtt.subscribe('raspi/' + raspi_id + '/#')
    raspies = [r for r in raspies if r['id'] != raspi_id]  # delete already existing one with the same id
    raspies.append(new_raspi)

    relays_list = []
    # add its relays to the list ...
    for relay in Relay.query.filter_by(raspi_id=raspi_id):
        pin = relay.pin
        relays_list.append(pin)
    # then ask the state of these relays to the raspberry
    mqtt.publish('raspi/' + raspi_id + '/relay/update_state', json.dumps({'gpios': relays_list}))

    socketio.emit('raspi_connect', new_raspi, namespace='/client', broadcast=True)


@mqtt.on_topic('server/raspi_disconnect')
def on_raspi_disconnect(client, userdata, msg):
    """
    Function called when a raspberry client disconnects.
    """
    global raspies
    data = json.loads(msg.payload.decode('utf-8'))
    raspi_id = data['id']
    old_raspi = {}
    old_raspi['id'] = raspi_id
    core.log.info("Raspberry " + raspi_id + " disconnected.")
    raspies = [r for r in raspies if r['id'] != raspi_id]
    mqtt.unsubscribe('raspi/' + raspi_id + '/#')
    socketio.emit('raspi_disconnect', old_raspi, namespace='/client', broadcast=True)


@socketio.on('shutdown', namespace='/client')
def shutdown():
    core.log.info("Shutdown rasperries")
    mqtt.publish('raspi/shutdown', 'shutdown')


@socketio.on('reboot', namespace='/client')
def reboot():
    core.log.info("Reboot rasperries")
    mqtt.publish('raspi/reboot', 'reboot')


@socketio.on('get_raspies', namespace='/client')
def get_raspies():
    emit('receive_raspies', raspies, namespace='/client', broadcast=False)
