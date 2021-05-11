import logging
from flask import Flask, Response, flash, render_template, redirect, request, session
from flask_bcrypt import Bcrypt
from cipher.model import db, User
from . import security

@security.route('/login', methods=['GET'])
def login_page():
    session['logged_in'] = False
    return render_template('login.html')


@security.route('/login', methods=['POST'])
def login():
    db_user = User.query.filter_by(username=request.form['username']).first()
    if db_user is not None and db_user.active:
        if Bcrypt().check_password_hash(db_user.password, request.form['password']):
            session['username'] = request.form['username']
            session['logged_in'] = True
        else:
            flash("L'utilisateur ou le mot de passe est incorrect.")
    else:
        flash("L'utilisateur ou le mot de passe est incorrect.")
    next_url = request.form['next'] or '/'
    return redirect(next_url)


@security.route('/register', methods=['POST'])
def register():
    if not request.form['username'] or ' ' in request.form['username']:
        flash("Le nom d'utilisateur ne doit pas contenir d'espace.")
        return redirect('/register_page')
    if User.query.filter_by(username=request.form['username']).first() is None:
        hashed_password = Bcrypt().generate_password_hash(request.form['password'])
        new_db_user = User(username=request.form['username'], password=hashed_password, active=True)
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
