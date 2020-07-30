from flask import Flask, session, redirect
from . import dashboard
from cipher.security import login_required

@dashboard.route('/')
@dashboard.route('/dashboard')
@login_required
def dashboard_page():
    return dashboard.render_page('dashboard.html')
