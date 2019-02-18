import logging
from flask import Flask, flash, redirect, request, session, jsonify
from . import settings
from app.model import db, Relay, config
import json
import re
from app.security import login_required

@settings.route('/settings')
@login_required
def settings_page():
    relays=Relay.query.all()
    cameraUrl=config.getCameraUrl()
    wheelsMode=config.getWheelsMode()
    audioOnServer=config.getAudioOnServer()
    return settings.render_page('settings.html', relays=relays, cameraUrl=cameraUrl, wheelsMode=wheelsMode, audioOnServer=audioOnServer)

@settings.route('/save_relay', methods=['POST'])
@login_required
def save_relay():
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
	return settings.render_page('settings.html')

@settings.route('/enable_relay', methods=['POST'])
@login_required
def enable_relay():
    rel_label = request.form.get("rel_label")
    value = json.loads(request.form.get("value"))
    if re.match(r"^$|\s+", rel_label):
        return "Un label de relai ne doit pas être vide ou contenir d'espace.", 400
    logging.info("Updating relay "+rel_label)
    db_rel = Relay.query.filter_by(label=rel_label).first()
    db_rel.enabled = value
    db.session.commit()
    return settings.render_page('settings.html')

@settings.route('/delete_relay', methods=['POST'])
@login_required
def delete_relay():
    rel_label = request.form.get("rel_label")
    if re.match(r"^$|\s+", rel_label):
        return "Un label de relai ne doit pas être vide ou contenir d'espace.", 400
    logging.info("Deleting relay "+rel_label)
    db_rel = Relay.query.filter_by(label=rel_label).first()
    db.session.delete(db_rel)
    db.session.commit()
    return settings.render_page('settings.html')

@settings.route('/update_camera_url', methods=['POST'])
@login_required
def update_camera_url():
    url = request.form.get("camera_url")
    print(url)
    if re.match(r"^$|\s+", url):
        return "L'url ne doit pas être vide ou contenir d'espace.", 400
    logging.info("Updating camera URL: "+url)
    config.setCameraUrl(url)
    return settings.render_page('settings.html')

@settings.route('/update_motion_mode', methods=['POST'])
@login_required
def update_motion_mode():
    value = json.loads(request.form.get("value"))
    logging.info("Updating wheels mode")
    config.setWheelsMode(value)
    return settings.render_page('settings.html')

@settings.route('/update_audio_source', methods=['POST'])
@login_required
def update_audio_source():
    value = json.loads(request.form.get("value"))
    logging.info("Updating audio source")
    config.setAudioOnServer(value)
    return settings.render_page('settings.html')

@settings.route('/get_motion_mode', methods=['POST'])
@login_required
def get_wheels_mode():
    return jsonify(config.getWheelsMode())

@settings.route('/get_audio_source', methods=['POST'])
@login_required
def get_audio_mode():
    return jsonify(config.getAudioOnServer())

@settings.route('/update_motion_raspi_id', methods=['POST'])
@login_required
def update_motion_raspi_id():
    id = request.form.get("raspi_id")
    logging.info("Updating motion raspi id: "+id)
    config.setMotionRaspiId(id)
    return settings.render_page('settings.html')

@settings.route('/update_servo_raspi_id', methods=['POST'])
@login_required
def update_servo_raspi_id():
    id = request.form.get("raspi_id")
    logging.info("Updating servo raspi id: "+id)
    config.setServoRaspiId(id)
    return settings.render_page('settings.html')