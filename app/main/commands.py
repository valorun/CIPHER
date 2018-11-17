#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, redirect, render_template, request, session, abort, jsonify
from app.model import config
import json
from . import main

@main.route('/save_buttons', methods=['POST'])
def save_buttons():
    """
    Sauvegarde la grille de boutons sur le serveur.
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

@main.route('/load_buttons', methods=['POST'])
def load_buttons():
    """
    Charge la grille de boutons depuis le serveur.
    """
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        logging.info("Loading buttons grid")
        grid = config.getCommandsGrid()
        return jsonify(grid)
