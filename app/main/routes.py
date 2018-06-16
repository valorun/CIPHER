#!/usr/bin/python
# coding: utf-8

from flask import Flask, flash, redirect, render_template, request, session, abort
from threading import Thread
from . import main
from app.model import db, Sequence, Relay
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
		return render_template('commands.html')

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
        print("Saving sequence "+seq_name)
        db_sequence = Sequence(id=seq_name, value=seq_data, enabled=True)
        db.session.add(db_sequence)
        db.session.commit()
        return render_template('sequences.html')

@main.route('/save_relay', methods=['POST'])
def save_relay():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        rel_label = request.form.get("rel_label")
        rel_pin = request.form.get("rel_pin")
        print("Saving relay "+rel_label)
        db_relay = Relay(label=rel_label, pin=rel_pin, enabled=True)
        db.session.add(db_relay)
        db.session.commit()
        return render_template('settings.html')

@main.route('/enable_sequence', methods=['POST'])
def enable_sequence():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        seq_name = request.form.get("seq_name")
        print("Updating "+seq_name)
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
        print("Updating relay "+rel_label)
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
        print("Deleting "+seq_name)
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
        print("Deleting relay "+rel_label)
        db_rel = Relay.query.filter_by(label=rel_label).first()
        db.session.delete(db_rel)
        db.session.commit()
        return render_template('settings.html')


@main.route('/login', methods=['POST'])
def admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
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
