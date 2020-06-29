from flask import Flask, request, jsonify, session
import json
from . import commands
from .model import UserCommandPanel
from cipher.model import db, Sequence, Relay, User, resources
from cipher.config import core_config
from cipher.security import login_required
from cipher.core.actions import CUSTOM_ACTIONS


@commands.route('/commands')
@login_required
def commands_page():
    sequences = Sequence.query.all()
    relays = Relay.query.all()
    camera_url = core_config.get_camera_url()
    sounds = resources.get_sounds()
    motion_raspi_id = core_config.get_motion_raspi_id()  # used to check if a raspi is specified, if not, then hide the motion panel
    enable_motion = core_config.get_enable_motion()  #
    return commands.render_page('commands.html', sequences=sequences, relays=relays, sounds=sounds, camera_url=camera_url, motion_raspi_id=motion_raspi_id, enable_motion=enable_motion, custom_actions=CUSTOM_ACTIONS)


@commands.route('/save_buttons', methods=['POST'])
@login_required
def save_buttons():
    """
    Save the grid of buttons on the server.
    """
    commands.log.info("Saving buttons grid for user '" + session['username'] + "'.")
    data = request.json.get('data')
    new_db_command_panel = UserCommandPanel(username=session['username'], grid=str(data))
    db.session.merge(new_db_command_panel)
    db.session.commit()
    return jsonify("Grille sauvegardée."), 200


@commands.route('/load_buttons', methods=['POST'])
@login_required
def load_buttons():
    """
    Load the grid of buttons from the server.
    """
    db_command_panel = UserCommandPanel.query.filter_by(username=session['username']).first()
    if db_command_panel is not None:
        commands.log.info("Loading buttons grid for user '" + session['username'] + "'.")
        grid = json.loads(db_command_panel.grid)
        return jsonify(grid), 200
    return jsonify("Aucune grille associée à l'utilisateur"), 400
