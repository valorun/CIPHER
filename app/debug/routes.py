#!/usr/bin/python
# coding: utf-8

import logging
from flask import render_template
from . import debug

@debug.route('/debug')
def debug_page():
	return render_template('debug.html')