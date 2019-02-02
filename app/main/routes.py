#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, Response, flash, redirect, render_template, request, session, abort, send_from_directory
from os import listdir, makedirs
from os.path import isfile, join, exists
from . import main
from app.constants import SOUNDS_LOCATION, SCRIPTS_LOCATION
from app.model import db, Sequence, Relay, config

@main.route('/')
@main.route('/index')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        cameraUrl=config.getCameraUrl()
        return render_template('index.html', cameraUrl=cameraUrl)

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
        cameraUrl=config.getCameraUrl()
        if not exists(SOUNDS_LOCATION):
            makedirs(SOUNDS_LOCATION)
        sounds=[f for f in listdir(SOUNDS_LOCATION) if isfile(join(SOUNDS_LOCATION, f))]
        return render_template('commands.html', sequences=sequences, relays=relays, sounds=sounds, cameraUrl=cameraUrl)

@main.route('/sequences')
def sequences():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        relays=Relay.query.all()
        sequences=Sequence.query.all()
        if not exists(SOUNDS_LOCATION):
            makedirs(SOUNDS_LOCATION)
        if not exists(SCRIPTS_LOCATION):
            makedirs(SCRIPTS_LOCATION)
        sounds=[f for f in listdir(SOUNDS_LOCATION) if isfile(join(SOUNDS_LOCATION, f))]
        scripts=[f for f in listdir(SCRIPTS_LOCATION) if isfile(join(SCRIPTS_LOCATION, f))]
        return render_template('sequences.html', sequences=sequences, relays=relays, sounds=sounds, scripts=scripts)

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
        cameraUrl=config.getCameraUrl()
        wheelsMode=config.getWheelsMode()
        chatbotReadOnlyMode=config.getChatbotReadOnlyMode()
        audioOnServer=config.getAudioOnServer()
        return render_template('settings.html', relays=relays, cameraUrl=cameraUrl, wheelsMode=wheelsMode, chatbotReadOnlyMode=chatbotReadOnlyMode, audioOnServer=audioOnServer)


@main.route('/login', methods=['POST'])
def admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['username'] = request.form['username']
        session['logged_in'] = True
    else:
        flash('L\'utilisateur ou le mot de passe est incorrect.')
    return index()

@main.route("/logout")
def logout():
    session['logged_in'] = False
    return index()


@main.errorhandler(400)
def invalid_page(e):
    return "La requête est invalide", 400

@main.errorhandler(404)
def page_not_found(e):
    return "Cette page n'existe pas", 404

@main.errorhandler(405)
def method_not_allowed(e):
    return "Cette page n'existe pas", 405


@main.route("/play_sound/<sound_name>", methods=['GET'])
def play_sound(sound_name):
    """
    Stream the specified sound to the client.
    """
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        def generate():
            with open(join(SOUNDS_LOCATION,sound_name), "rb") as fwav:
                data = fwav.read(1024)
                while data:
                    yield data
                    data = fwav.read(1024)
        return Response(generate(), mimetype="audio/x-wav")

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(join(main.root_path, 'static'), 'favicon.ico',mimetype='image/vnd.microsoft.icon')