#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, redirect, render_template, request, session, abort
from . import main
from app.model import db, Sequence

@main.route('/save_sequence', methods=['POST'])
def save_sequence():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        seq_name = request.form.get("seq_name")
        seq_data = request.form.get("seq_data")
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
        logging.info("Updating "+seq_name)
        db_seq = Sequence.query.filter_by(id=seq_name).first()
        db_seq.enabled = not db_seq.enabled
        db.session.commit()
        return render_template('sequences.html')

@main.route('/delete_sequence', methods=['POST'])
def delete_sequence():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        seq_name = request.form.get("seq_name")
        logging.info("Deleting "+seq_name)
        db_seq = Sequence.query.filter_by(id=seq_name).first()
        db.session.delete(db_seq)
        db.session.commit()
        return render_template('sequences.html')