import logging
from flask_socketio import SocketIO, emit
from app import socketio
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

@socketio.on('update_state_for_client', namespace='/relay')
def update_state_for_client(pin, state, raspi_id):
	"""
	Update the state of the relays on the client side at the request of a raspberry.
	"""
	logging.info("Updating relay status on client")
	for relay in Relay.query.filter_by(pin=pin, raspi_id=raspi_id):
		label=relay.label
		emit("update_relay_state", {'label':label, 'state':state}, namespace="/client", broadcast=True)
