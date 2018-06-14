#!/usr/bin/python
# coding: utf-8

from flask import Flask, flash, redirect, render_template, request, session, abort
from threading import Thread
from . import main
from app.model import db, Sequence
import json


@main.route('/')
def index():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('index.html')

@main.route('/debug')
def debug():
	return render_template('debug.html')


@main.route('/graph')
def graph():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('graph.html')

@main.route('/speech')
def speech():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('speech.html')

@main.route('/save_sequence', methods=['POST'])
def save_sequence():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        seq_name = request.form.get("seq_name")
        seq_data = request.form.get("seq_data")
        print("Saving "+seq_name)
        db_sequence = Sequence(id=seq_name, value=seq_data, enabled=True)
        db.session.add(db_sequence)
        db.session.commit()
        return render_template('graph.html')


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
