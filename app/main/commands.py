#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, redirect, render_template, request, session, abort
from . import main
from app.model import db, Button

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