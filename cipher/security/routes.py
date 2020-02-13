import logging
import base64
from flask import Flask, Response, flash, render_template, redirect, request, session
from cipher.model import db, User
from . import security


@security.route('/login', methods=['GET'])
def login_page():
    session['logged_in'] = False
    new_db_user = User(username='admin', password='cGFzc3dvcmQ=', active=True)
    db.session.merge(new_db_user)
    db.session.commit()
    return render_template('login.html')


@security.route('/login', methods=['POST'])
def login():
    db_user = User.query.filter_by(username=request.form['username']).first()
    if db_user is not None and db_user.active:
        decoded_password = base64.b64decode(db_user.password).decode('utf-8', 'ignore')
        if request.form['password'] == decoded_password:
            session['username'] = request.form['username']
            session['logged_in'] = True
        else:
            flash("L'utilisateur ou le mot de passe est incorrect.")
    else:
        flash("L'utilisateur ou le mot de passe est incorrect.")
    return redirect('/')


@security.route('/register', methods=['POST'])
def register():
    if not request.form['username'] or ' ' in request.form['username']:
        flash("Le nom d'utilisateur ne dois pas contenir d'espace.")
        return redirect('/register_page')
    if User.query.filter_by(username=request.form['username']).first() is None:
        encoded_password = base64.b64encode(bytes(request.form['password']))
        new_db_user = User(username=request.form['username'], password=encoded_password, active=True)
        db.session.merge(new_db_user)
        db.session.commit()
        return redirect('/')
    else:
        flash("L'utilisateur existe déjà.")
        return redirect('/register_page')


@security.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect('/')
