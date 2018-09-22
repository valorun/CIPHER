#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, redirect, render_template, request, session, abort
from . import main
from app.model import db, Sequence
import json
import re

@main.route('/save_sequence', methods=['POST'])
def save_sequence():
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

@main.route('/enable_sequence', methods=['POST'])
def enable_sequence():
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

@main.route('/delete_sequence', methods=['POST'])
def delete_sequence():
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