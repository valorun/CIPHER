#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, flash, redirect, render_template, request, session, abort
from threading import Thread
from . import main
from app.model import db, Sequence, Relay, Button
import json

@main.route('/')
@main.route('/index')
def index():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('index.html')

@main.route('/debug')
def debug():
	return render_template('debug.html')


@main.route('/commands')
def commands():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        sequences=Sequence.query.all()
        relays=Relay.query.all()
        buttons=Button.query.all()
        return render_template('commands.html', sequences=sequences, relays=relays, buttons=buttons)

@main.route('/sequences')
def sequences():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        relays=Relay.query.all()
        sequences=Sequence.query.all()
        return render_template('sequences.html', sequences=sequences, relays=relays)

@main.route('/speech')
def speech():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        sequences=Sequence.query.all()
        return render_template('speech.html', sequences=sequences)

@main.route('/settings')
def settings():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        relays=Relay.query.all()
        return render_template('settings.html', relays=relays)

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

@main.route('/save_button', methods=['POST'])
def save_button():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        rel_label = request.form.get("rel_label")
        btn_label = request.form.get("btn_label")
        btn_left = request.form.get("btn_left")
        btn_top = request.form.get("btn_top")
        logging.info("Saving button "+btn_label)
        db_button = Button(relay_label=rel_label, label=btn_label, left=btn_left, top=btn_top)
        db.session.merge(db_button)
        db.session.commit()
        return render_template('commands.html')

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

@main.route('/delete_button', methods=['POST'])
def delete_button():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        rel_label = request.form.get("rel_label")
        logging.info("Deleting relay "+rel_label)
        db_btn = Button.query.filter_by(relay_label=rel_label).first()
        db.session.delete(db_btn)
        db.session.commit()
        return render_template('commands.html')


@main.route('/login', methods=['POST'])
def admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['username'] = request.form['username']
        session['logged_in'] = True
    else:
        flash('L\'utilisateur ou le mot de passe est incorrect')
    return index()

@main.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

@main.errorhandler(404)
def page_not_found(e):
    return "Cette page n'existe pas"

@main.errorhandler(405)
def method_not_allowed(e):
    return "Cette page n'existe pas"
