#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, redirect, render_template, request, session, abort, jsonify
import json
from . import main
from .. import COMMANDS_GRID


#sauvegarde la grille de boutons sur le serveur
@main.route('/save_buttons', methods=['POST'])
def save_buttons():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        data=request.form.get("data")
        with open(COMMANDS_GRID, 'w') as file:
            file.write(data)
        return "Grille sauvegardée.", 200

#charge la grille de boutons depuis le serveur
@main.route('/load_buttons', methods=['POST'])
def load_buttons():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        try:
            with open(COMMANDS_GRID, 'r') as f:
                grid = json.load(f)
                return jsonify(grid)
        except IOError:
            with open(COMMANDS_GRID, 'w') as f:
                f.write("[]")
                return "Aucun fichier a charger.", 500
        except ValueError:
            return "Le format de fichier n'est pas reconnu.", 500
