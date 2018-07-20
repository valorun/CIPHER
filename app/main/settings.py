#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, redirect, render_template, request, session, abort
from . import main
from app.model import db, Relay

@main.route('/save_relay', methods=['POST'])
def save_relay():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        rel_label = request.form.get("rel_label")
        rel_pin = request.form.get("rel_pin")
        rel_parity = request.form.get("rel_parity")
        logging.info("Saving relay "+rel_label)
        db_relay = Relay(label=rel_label, pin=rel_pin, enabled=True, parity=rel_parity)
        db.session.add(db_relay)
        db.session.commit()
        return render_template('settings.html')

@main.route('/enable_relay', methods=['POST'])
def enable_relay():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        rel_label = request.form.get("rel_label")
        logging.info("Updating relay "+rel_label)
        db_rel = Relay.query.filter_by(label=rel_label).first()
        db_rel.enabled = not db_rel.enabled
        db.session.commit()
        return render_template('settings.html')

@main.route('/delete_relay', methods=['POST'])
def delete_relay():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        rel_label = request.form.get("rel_label")
        logging.info("Deleting relay "+rel_label)
        db_rel = Relay.query.filter_by(label=rel_label).first()
        db.session.delete(db_rel)
        db.session.commit()
        return render_template('settings.html')