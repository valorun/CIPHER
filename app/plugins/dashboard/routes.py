#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, session, redirect
from . import dashboard
from app.model import config
from app.security import login_required

@dashboard.route('/')
@dashboard.route('/dashboard')
@login_required
def dashboard_page():
    cameraUrl=config.getCameraUrl()
    return dashboard.render_page('dashboard.html', cameraUrl=cameraUrl)