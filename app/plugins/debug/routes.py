#!/usr/bin/python
# coding: utf-8

import logging
from . import debug

@debug.route('/debug')
def debug_page():
	return debug.render_page('debug.html')