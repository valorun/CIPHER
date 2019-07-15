import logging
from flask import Flask, request, jsonify, session
import json
from . import commands
from .model import UserCommandPanel
from cipher.model import db, Sequence, Relay, User, config, resources
from cipher.security import login_required

@commands.route('/commands')
@login_required
def commands_page():
    sequences = Sequence.query.all()
    relays = Relay.query.all()
    cameraUrl = config.getCameraUrl()
    sounds = resources.getSounds()
    motionRaspiId = config.getMotionRaspiId() # used to check if a raspi is specified, if not, then hide the motion panel
    return commands.render_page('commands.html', sequences=sequences, relays=relays, sounds=sounds, cameraUrl=cameraUrl, motionRaspiId=motionRaspiId)


@commands.route('/save_buttons', methods=['POST'])
@login_required
def save_buttons():
	"""
	Save the grid of buttons on the server.
	"""
	logging.info("Saving buttons grid for user '" + session['username'] + "'.")
	data = request.form.get('data')
	try:
		json.loads(data) # check if data have correct JSON format
	except (ValueError, Exception):
		data = None
	new_db_command_panel = UserCommandPanel(username=session['username'], grid=str(data))
	db.session.merge(new_db_command_panel)
	db.session.commit()
	return "Grille sauvegardée.", 200

@commands.route('/load_buttons', methods=['POST'])
@login_required
def load_buttons():
	"""  
	Load the grid of buttons from the server.
	"""
	db_command_panel = UserCommandPanel.query.filter_by(username=session['username']).first()
	if db_command_panel is not None:
		logging.info("Loading buttons grid for user '" + session['username'] + "'.")
		grid = json.loads(db_command_panel.grid)
		logging.info(grid)
		return jsonify(grid)
	return "Aucune grille associée à l'utilisateur", 400
