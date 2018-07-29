#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, redirect, render_template, request, session, abort
from . import main
from app.model import db, Button
import re

@main.route('/save_button', methods=['POST'])
def save_button():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        rel_label = request.form.get("rel_label")
        btn_label = request.form.get("btn_label")
        btn_left = request.form.get("btn_left")
        btn_top = request.form.get("btn_top")
        if re.match(r"^$|\s+", rel_label):
            return "Un label de relai ne doit pas être vide ou contenir d'espace.", 400
        if re.match(r"^$|\s+", btn_label):
            return "Un label de bouton ne doit pas être vide ou contenir d'espace.", 400
        if btn_left.isdigit() and btn_top.isdigit():
            return "Les coordonnées du boutons sont invalides.", 400
        logging.info("Saving button "+btn_label)
        db_button = Button(relay_label=rel_label, label=btn_label, left=btn_left, top=btn_top)
        db.session.merge(db_button)
        db.session.commit()
        return render_template('commands.html')

@main.route('/delete_button', methods=['POST'])
def delete_button():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        rel_label = request.form.get("rel_label")
        if re.match(r"^$|\s+", rel_label):
            return "Un label de relai ne doit pas être vide ou contenir d'espace.", 400
        logging.info("Deleting relay "+rel_label)
        db_btn = Button.query.filter_by(relay_label=rel_label).first()
        if db_btn != None:
            db.session.delete(db_btn)
            db.session.commit()
        return render_template('commands.html')