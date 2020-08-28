import json
from flask_socketio import SocketIO, emit
from flask_mqtt import Mqtt
from cipher import socketio, mqtt
from cipher.model import Relay
from . import core

clients = []

@mqtt.on_topic('client/connect')
def on_client_connect(client, userdata, msg):
    """
    Function called when a client connects.
    """
    global clients
    data = json.loads(msg.payload.decode('utf-8'))
    new_client = {}
    new_client['id'] = data['id']
    new_client['icon'] = data['icon']
    core.log.info("Client " + new_client['id'] + " connected.")
    mqtt.subscribe('client/' + new_client['id'] + '/#')
    clients = [c for c in clients if c['id'] != new_client['id']]  # delete already existing one with the same id
    clients.append(new_client)

    relays_list = []
    # add its relays to the list ...
    for relay in Relay.query.filter_by(raspi_id=new_client['id']):
        pin = relay.pin
        relays_list.append(pin)
    # then ask the state of these relays to the raspberry
    mqtt.publish('client/' + new_client['id'] + '/relay/update_state', json.dumps({'gpios': relays_list}))

    socketio.emit('client_connect', new_client, namespace='/client', broadcast=True)


@mqtt.on_topic('server/client_disconnect')
def on_client_disconnect(client, userdata, msg):
    """
    Function called when a client disconnects.
    """
    global clients
    data = json.loads(msg.payload.decode('utf-8'))
    client_id = data['id']
    old_client = next(c for c in clients if c['id'] == client_id)
    core.log.info("Client " + client_id + " disconnected.")
    clients = [c for c in clients if c['id'] != client_id]
    mqtt.unsubscribe('client/' + client_id + '/#')
    socketio.emit('client_disconnect', old_client, namespace='/client', broadcast=True)


@socketio.on('shutdown', namespace='/client')
def shutdown():
    core.log.info("Shutdown rasperries")
    mqtt.publish('raspi/shutdown', 'shutdown')


@socketio.on('reboot', namespace='/client')
def reboot():
    core.log.info("Reboot rasperries")
    mqtt.publish('raspi/reboot', 'reboot')


@socketio.on('get_clients', namespace='/client')
def get_clients():
    emit('receive_clients', clients, namespace='/client', broadcast=False)
