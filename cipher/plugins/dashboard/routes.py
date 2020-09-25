from flask import Flask, session, redirect
from . import dashboard
from cipher.security import login_required
from cipher import SocketIOHandler

@dashboard.route('/')
@dashboard.route('/dashboard')
@login_required
def dashboard_page():
    log_records = '\n'.join(SocketIOHandler.log_queue) + '\n'
    return dashboard.render_page('dashboard.html', log_records=log_records)
