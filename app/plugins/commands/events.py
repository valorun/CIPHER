import logging
import json
from flask_socketio import SocketIO, emit
from flask_mqtt import Mqtt
from app import socketio, mqtt
from app.model import Relay

@socketio.on('update_relays_state', namespace='/client')
def update_relays_state():
	"""
	Update the state of the relays on the raspberry side at the request of a client.
	"""
	logging.info("Updating relay status on client")
	for relay in Relay.query.distinct(Relay.pin):
		pin=relay.pin
		emit("update_state", pin, namespace="/relay", broadcast=True)

@mqtt.on_topic('server/update_relay')
def update_state_for_client(client, userdata, msg):
	"""
	Update the state of the relays on the client side at the request of a raspberry.
	"""
	data = json.loads(msg.payload.decode('utf-8'))
	raspi_id = data['raspi_id']
	pin = data['gpio']
	state = data['state']
	logging.info("Updating relay status on client")
	for relay in Relay.query.filter_by(pin=pin, raspi_id=raspi_id):
		label=relay.label
		emit("update_relay_state", {'label':label, 'state':state}, namespace="/client", broadcast=True)
