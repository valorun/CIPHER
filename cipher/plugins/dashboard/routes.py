import logging
from flask import Flask, session, redirect
from . import dashboard
from cipher.config import core_config
from cipher.security import login_required

@dashboard.route('/')
@dashboard.route('/dashboard')
@login_required
def dashboard_page():
    camera_url = core_config.get_camera_url()
    return dashboard.render_page('dashboard.html', camera_url=camera_url)
