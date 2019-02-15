#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, session, request, redirect
import json
import re
from os import listdir, makedirs
from os.path import isfile, join, exists
from . import sequences
from app.constants import SOUNDS_LOCATION, SCRIPTS_LOCATION
from app.model import Sequence, Relay, db
from app.security import login_required

@sequences.route('/sequences')
@login_required
def sequences_page():
    relays=Relay.query.all()
    sequences=Sequence.query.all()
    if not exists(SOUNDS_LOCATION):
        makedirs(SOUNDS_LOCATION)
    if not exists(SCRIPTS_LOCATION):
        makedirs(SCRIPTS_LOCATION)
    sounds=[f for f in listdir(SOUNDS_LOCATION) if isfile(join(SOUNDS_LOCATION, f))]
    scripts=[f for f in listdir(SCRIPTS_LOCATION) if isfile(join(SCRIPTS_LOCATION, f))]
    return sequences.render_page('sequences.html', sequences=sequences, relays=relays, sounds=sounds, scripts=scripts)

@sequences.route('/save_sequence', methods=['POST'])
@login_required
def save_sequence():
    """
    Save a sequence in the database.
    """
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
    return sequences.render_page('sequences.html')

@sequences.route('/enable_sequence', methods=['POST'])
@login_required
def enable_sequence():
    """
    Enable or disable a equence stored in the database.
    """
    seq_name = request.form.get("seq_name")
    value = json.loads(request.form.get("value"))
    if re.match(r"^$|\s+", seq_name):
        return "Un nom de séquence ne doit pas être vide ou contenir d'espace.", 400
    logging.info("Updating "+seq_name)
    db_seq = Sequence.query.filter_by(id=seq_name).first()
    db_seq.enabled = value
    db.session.commit()
    return sequences.render_page('sequences.html')

@sequences.route('/delete_sequence', methods=['POST'])
@login_required
def delete_sequence():
    """
    Delete a sequence stored in the database.
    """
    seq_name = request.form.get("seq_name")
    if re.match(r"^$|\s+", seq_name):
        return "Un nom de séquence ne doit pas être vide ou contenir d'espace.", 400
    logging.info("Deleting "+seq_name)
    db_seq = Sequence.query.filter_by(id=seq_name).first()
    db.session.delete(db_seq)
    db.session.commit()
    return sequences.render_page('sequences.html')