#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, redirect, render_template, request, session, abort, jsonify
import json
from os import listdir, makedirs
from os.path import isfile, join, exists
from . import commands
from app.constants import SOUNDS_LOCATION, SCRIPTS_LOCATION
from app.model import Sequence, Relay, config

@commands.route('/commands')
def commands_page():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        sequences=Sequence.query.all()
        relays=Relay.query.all()
        cameraUrl=config.getCameraUrl()
        if not exists(SOUNDS_LOCATION):
            makedirs(SOUNDS_LOCATION)
        sounds=[f for f in listdir(SOUNDS_LOCATION) if isfile(join(SOUNDS_LOCATION, f))]
        return render_template('commands.html', sequences=sequences, relays=relays, sounds=sounds, cameraUrl=cameraUrl)


@commands.route('/save_buttons', methods=['POST'])
def save_buttons():
    """
    Save the grid of buttons on the server.
    """
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        logging.info("Saving buttons grid")
        data=request.form.get("data")
        try:
            data = json.loads(data)
        except (ValueError, Exception):
            data = None
        config.setCommandsGrid(data)
        return "Grille sauvegardée.", 200

@commands.route('/load_buttons', methods=['POST'])
def load_buttons():
    """  
    Load the grid of buttons from the server.
    """
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        logging.info("Loading buttons grid")
        grid = config.getCommandsGrid()
        return jsonify(grid)
