import logging
from flask import Flask, flash, redirect, request, session, jsonify
from . import settings
from app.model import db, Relay, Servo, config
import json
from app.security import login_required

@settings.route('/settings')
@login_required
def settings_page():
    relays=Relay.query.all()
    servos=Servo.query.all()
    cameraUrl=config.getCameraUrl() or ""
    audioOnServer=config.getAudioOnServer()
    motionRaspiId=config.getMotionRaspiId() or ""
    return settings.render_page('settings.html', relays=relays, servos=servos, cameraUrl=cameraUrl, audioOnServer=audioOnServer, motionRaspiId=motionRaspiId)

@settings.route('/save_relay', methods=['POST'])
@login_required
def save_relay():
	rel_label = request.form.get("rel_label")
	rel_pin = request.form.get("rel_pin")
	rel_parity = request.form.get("rel_parity")
	raspi_id = request.form.get("raspi_id")
	if not rel_label or ' ' in rel_label:
		return "Un label de relai ne doit pas être vide ou contenir d'espace.", 400
	if not rel_pin or ' ' in rel_pin:
		return "Un pin ne doit pas être vide ou contenir d'espace.", 400
	if not rel_parity or ' ' in rel_parity:
		return "Une parité ne doit pas contenir d'espace.", 400
	if not raspi_id or ' ' in raspi_id:
		return "Un id de raspberry ne doit pas être vide ou contenir d'espace.", 400
	if Relay.query.filter_by(label=rel_label).first() is not None:
		return "Un relai portant le même label existe déjà.", 400
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
    if not rel_label or ' ' in rel_label:
        return "Un label de relai ne doit pas être vide ou contenir d'espace.", 400
    logging.info("Updating relay "+rel_label)
    db_rel = Relay.query.filter_by(label=rel_label).first()
    if db_rel is None:
        return "Le relai est inconnu.", 400
    db_rel.enabled = value
    db.session.commit()
    return settings.render_page('settings.html')

@settings.route('/delete_relay', methods=['POST'])
@login_required
def delete_relay():
    rel_label = request.form.get("rel_label")
    if not rel_label or ' ' in rel_label:
        return "Un label de relai ne doit pas être vide ou contenir d'espace.", 400
    logging.info("Deleting relay "+rel_label)
    db_rel = Relay.query.filter_by(label=rel_label).first()
    if db_rel is None:
        return "Le relai est inconnu.", 400
    db.session.delete(db_rel)
    db.session.commit()
    return settings.render_page('settings.html')

@settings.route('/save_servo', methods=['POST'])
@login_required
def save_servo():
	servo_label = request.form.get("servo_label")
	servo_pin = request.form.get("servo_pin")
	raspi_id = request.form.get("raspi_id")
	if not servo_label or ' ' in servo_label:
		return "Un label de servo moteur ne doit pas être vide ou contenir d'espace.", 400
	if not servo_pin or ' ' in servo_pin:
		return "Un pin ne doit pas être vide ou contenir d'espace.", 400
	if not raspi_id or ' ' in raspi_id:
		return "Un id de raspberry ne doit pas être vide ou contenir d'espace.", 400
	if Servo.query.filter_by(label=servo_label).first() is not None:
		return "Un servomoteur portant le même label existe déjà.", 400
	logging.info("Saving servo "+servo_label)
	db_servo = Servo(label=servo_label, pin=servo_pin, enabled=True, raspi_id=raspi_id)
	db.session.add(db_servo)
	db.session.commit()
	return settings.render_page('settings.html')

@settings.route('/enable_servo', methods=['POST'])
@login_required
def enable_servo():
    servo_label = request.form.get("servo_label")
    value = json.loads(request.form.get("value"))
    if not servo_label or ' ' in servo_label:
        return "Un label de servomoteur ne doit pas être vide ou contenir d'espace.", 400
    logging.info("Updating servo "+servo_label)
    db_servo = Servo.query.filter_by(label=servo_label).first()
    if db_servo is None:
        return "Le servomoteur est inconnu.", 400
    db_servo.enabled = value
    db.session.commit()
    return settings.render_page('settings.html')

@settings.route('/delete_servo', methods=['POST'])
@login_required
def delete_servo():
    servo_label = request.form.get("servo_label")
    if not servo_label or ' ' in servo_label:
        return "Un label de servomoteur ne doit pas être vide ou contenir d'espace.", 400
    logging.info("Deleting servo "+servo_label)
    db_servo = Servo.query.filter_by(label=servo_label).first()
    if db_servo is None:
        return "Le servomoteur est inconnu.", 400
    db.session.delete(db_servo)
    db.session.commit()
    return settings.render_page('settings.html')


@settings.route('/update_camera_url', methods=['POST'])
@login_required
def update_camera_url():
    url = request.form.get("camera_url")
    if url and ' ' in url: #if the string is empty, update is accepted
        return "L'url ne doit pas contenir d'espace.", 400
    logging.info("Updating camera URL: "+url)
    config.setCameraUrl(url)
    return settings.render_page('settings.html')

@settings.route('/update_audio_source', methods=['POST'])
@login_required
def update_audio_source():
    value = json.loads(request.form.get("value"))
    logging.info("Updating audio source")
    config.setAudioOnServer(value)
    return settings.render_page('settings.html')

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

@settings.route('/update_robot_name', methods=['POST'])
@login_required
def update_robot_name():
    name = request.form.get("robot_name")
    logging.info("Updating robot name: "+name)
    config.setRobotName(name)
    return settings.render_page('settings.html')