#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, Response, flash, redirect, render_template, request, session, send_from_directory
from os.path import isfile, join
from . import main
from app.constants import SOUNDS_LOCATION

@main.route("/login", methods=['POST'])
def admin_login_page():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['username'] = request.form['username']
        session['logged_in'] = True
    else:
        flash('L\'utilisateur ou le mot de passe est incorrect.')
    return redirect("/")

@main.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect("/")


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