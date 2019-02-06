#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, render_template, session
from . import speech
from app.model import Sequence

@speech.route('/speech')
def speech_page():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        sequences=Sequence.query.all()
        return render_template('speech.html', sequences=sequences)