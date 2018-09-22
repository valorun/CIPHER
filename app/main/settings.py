#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from . import main
from app.model import db, Relay, config, chatbot
import json
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
        value = json.loads(request.form.get("value"))
        if re.match(r"^$|\s+", rel_label):
            return "Un label de relai ne doit pas être vide ou contenir d'espace.", 400
        logging.info("Updating relay "+rel_label)
        db_rel = Relay.query.filter_by(label=rel_label).first()
        db_rel.enabled = value
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

@main.route('/update_camera_url', methods=['POST'])
def update_camera_url():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        url = request.form.get("camera_url")
        print(url)
        if re.match(r"^$|\s+", url):
            return "L'url ne doit pas être vide ou contenir d'espace.", 400
        logging.info("Updating camera URL: "+url)
        config.setCameraUrl(url)
        return render_template('settings.html')

@main.route('/update_motion_mode', methods=['POST'])
def update_motion_mode():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        value = json.loads(request.form.get("value"))
        logging.info("Updating wheels mode")
        config.setWheelsMode(value)
        return render_template('settings.html')

@main.route('/get_motion_mode', methods=['POST'])
def get_wheels_mode():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return jsonify(config.getWheelsMode())

@main.route('/update_chatbot_learning_mode', methods=['POST'])
def update_chatbot_learning_mode():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        value = json.loads(request.form.get("value"))
        logging.info("Updating chatbot learning mode")
        config.setChatbotReadOnlyMode(value)
        chatbot.instantiateChatBot(config.getChatbotReadOnlyMode())
        return render_template('settings.html')