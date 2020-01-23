import logging
from flask import Flask, session, redirect
from . import dashboard
from cipher.model import config
from cipher.security import login_required

@dashboard.route('/')
@dashboard.route('/dashboard')
@login_required
def dashboard_page():
    camera_url = config.get_camera_url() or ''
    return dashboard.render_page('dashboard.html', camera_url=camera_url)
