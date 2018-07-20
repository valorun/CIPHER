#!/usr/bin/python
# coding: utf-8

import logging
from flask_socketio import SocketIO, emit
from .. import socketio
from app.model import Relay

#Met a jour l'etat des relais cote client à la demande d'un client
@socketio.on('update_relays_state', namespace='/client')
def update_relays_state():
	logging.info("Updating relay status on client")
	for relay in Relay.query.distinct(Relay.pin):
		pin=relay.pin
		emit("update_state", pin, namespace="/relay", broadcast=True)

#Met a jour l'etat des relais cote client à la demande d'un raspberry
@socketio.on('update_state_for_client', namespace='/relay')
def update_state_for_client(pin, state):
	logging.info("Updating relay status on client")
	for relay in Relay.query.filter_by(pin=pin):
		label=relay.label
		emit("update_relay_state", {'label':label, 'state':state}, namespace="/client", broadcast=True)