import logging
from flask import Flask, session, redirect
from . import dashboard
from cipher.model import config
from cipher.security import login_required

@dashboard.route('/')
@dashboard.route('/dashboard')
@login_required
def dashboard_page():
    cameraUrl=config.getCameraUrl()
    return dashboard.render_page('dashboard.html', cameraUrl=cameraUrl)