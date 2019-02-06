#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, render_template, session, request
import json
import re
from os import listdir, makedirs
from os.path import isfile, join, exists
from . import sequences
from app.constants import SOUNDS_LOCATION, SCRIPTS_LOCATION
from app.model import Sequence, Relay, db

@sequences.route('/sequences')
def sequences_page():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        relays=Relay.query.all()
        sequences=Sequence.query.all()
        if not exists(SOUNDS_LOCATION):
            makedirs(SOUNDS_LOCATION)
        if not exists(SCRIPTS_LOCATION):
            makedirs(SCRIPTS_LOCATION)
        sounds=[f for f in listdir(SOUNDS_LOCATION) if isfile(join(SOUNDS_LOCATION, f))]
        scripts=[f for f in listdir(SCRIPTS_LOCATION) if isfile(join(SCRIPTS_LOCATION, f))]
        return render_template('sequences.html', sequences=sequences, relays=relays, sounds=sounds, scripts=scripts)

@sequences.route('/save_sequence', methods=['POST'])
def save_sequence():
    """
    Save a sequence in the database.
    """
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        seq_name = request.form.get("seq_name")
        seq_data = request.form.get("seq_data")
        if re.match(r"^$|\s+", seq_name):
            return "Un nom de séquence ne doit pas être vide ou contenir d'espace.", 400
        if seq_data==None:
            return "La séquence est vide.", 400
        logging.info("Saving sequence "+seq_name)
        db_sequence = Sequence(id=seq_name, value=seq_data, enabled=True)
        db.session.merge(db_sequence)
        db.session.commit()
        return render_template('sequences.html')

@sequences.route('/enable_sequence', methods=['POST'])
def enable_sequence():
    """
    Enable or disable a equence stored in the database.
    """
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        seq_name = request.form.get("seq_name")
        value = json.loads(request.form.get("value"))
        if re.match(r"^$|\s+", seq_name):
            return "Un nom de séquence ne doit pas être vide ou contenir d'espace.", 400
        logging.info("Updating "+seq_name)
        db_seq = Sequence.query.filter_by(id=seq_name).first()
        db_seq.enabled = value
        db.session.commit()
        return render_template('sequences.html')

@sequences.route('/delete_sequence', methods=['POST'])
def delete_sequence():
    """
    Delete a sequence stored in the database.
    """
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        seq_name = request.form.get("seq_name")
        if re.match(r"^$|\s+", seq_name):
            return "Un nom de séquence ne doit pas être vide ou contenir d'espace.", 400
        logging.info("Deleting "+seq_name)
        db_seq = Sequence.query.filter_by(id=seq_name).first()
        db.session.delete(db_seq)
        db.session.commit()
        return render_template('sequences.html')