import logging
import json
from flask_socketio import SocketIO, emit
from flask_mqtt import Mqtt
from cipher import socketio, mqtt
from cipher.model import Relay

@socketio.on('update_all_relays_state', namespace='/client')
def update_all_relays_state():
	"""
	Update the state of the relays on the raspberry side at the request of a client.
	"""
	logging.info("Request relay status update from client")
	# for each known raspberry ...
	for raspi in Relay.query.distinct(Relay.raspi_id):
		raspi_id=raspi.raspi_id
		relays_list = []
		# add its relays to the list ...
		for relay in Relay.query.filter_by(raspi_id=raspi_id):
			pin=relay.pin
			relays_list.append(pin)
		# then ask the state of these relays to the raspberry
		mqtt.publish('raspi/' + raspi_id + '/relay/update_state', json.dumps({'gpios':relays_list}))

@mqtt.on_topic('server/update_relays_state')
def update_relays_state_for_client(client, userdata, msg):
	"""
	Update the state of the relays on the client side at the request of a raspberry.
	"""
	logging.info("Updating relay status on client")
	relays_list = [] # relays to update on client 
	data = json.loads(msg.payload.decode('utf-8'))
	# for each specified relay ...
	for relay in data['relays']:
		raspi_id = relay['raspi_id']
		pin = relay['gpio']
		state = relay['state']
		# retrieve the missing information: the label corresponding to the pin
		for relay in Relay.query.filter_by(pin=pin, raspi_id=raspi_id):
			label=relay.label
			relays_list.append({'relay':label, 'state':state})
	# finally send the list of the relays to update on the client
	socketio.emit('update_relays_state', relays_list, namespace="/client", broadcast=True)
