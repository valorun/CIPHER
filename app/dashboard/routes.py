#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, render_template, session
from . import dashboard
from app.model import config

@dashboard.route('/')
@dashboard.route('/dashboard')
def dashboard_page():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        cameraUrl=config.getCameraUrl()
        return render_template('dashboard.html', cameraUrl=cameraUrl)
