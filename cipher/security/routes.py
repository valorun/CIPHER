#!/usr/bin/python
# coding: utf-8

import logging
from flask import Flask, Response, flash, render_template, redirect, request, session
from . import security

@security.route('/login', methods=['GET'])
def login_page():
    session['logged_in'] = False
    return render_template('login.html')

@security.route('/login', methods=['POST'])
def login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['username'] = request.form['username']
        session['logged_in'] = True
    else:
        flash('L\'utilisateur ou le mot de passe est incorrect.')
    return redirect('/')

@security.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect('/')