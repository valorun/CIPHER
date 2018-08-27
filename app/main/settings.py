#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, flash, redirect, render_template, request, session, abort
from . import main
from app.model import db, Relay
import re

@main.route('/save_relay', methods=['POST'])
def save_relay():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		rel_label = request.form.get("rel_label")
		rel_pin = request.form.get("rel_pin")
		rel_parity = request.form.get("rel_parity")
		raspi_id = request.form.get("raspi_id")
		if re.match(r"^$|\s+", rel_label):
			return "Un label de relai ne doit pas être vide ou contenir d'espace.", 400
		if re.match(r"^$|\s+", rel_pin):
			return "Un pin ne doit pas être vide ou contenir d'espace.", 400
		if re.match(r"\s+", rel_parity):
			return "Une parité ne doit pas contenir d'espace.", 400
		if re.match(r"^$|\s+", raspi_id):
			return "Un id de rapsberry ne doit pas être vide ou contenir d'espace.", 400
		logging.info("Saving relay "+rel_label)
		db_relay = Relay(label=rel_label, pin=rel_pin, enabled=True, parity=rel_parity, raspi_id=raspi_id)
		db.session.add(db_relay)
		db.session.commit()
		return render_template('settings.html')

@main.route('/enable_relay', methods=['POST'])
def enable_relay():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        rel_label = request.form.get("rel_label")
        if re.match(r"^$|\s+", rel_label):
            return "Un label de relai ne doit pas être vide ou contenir d'espace.", 400
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
        if re.match(r"^$|\s+", rel_label):
            return "Un label de relai ne doit pas être vide ou contenir d'espace.", 400
        logging.info("Deleting relay "+rel_label)
        db_rel = Relay.query.filter_by(label=rel_label).first()
        db.session.delete(db_rel)
        db.session.commit()
        return render_template('settings.html')
