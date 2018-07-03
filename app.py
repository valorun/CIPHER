#!/usr/bin/python
# coding: utf-8

from app import create_app, socketio

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app, host = "0.0.0.0", port = 5000, certfile='cert.pem', keyfile='key.pem')
    #socketio.run(app, host = "0.0.0.0", port = 5000)
