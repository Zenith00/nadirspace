import json
# from urllib import request
import ipaddress
import requests
# from flask import Flask, abort, request
from gevent import monkey
monkey.patch_all()
import flask
from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication
from gevent.wsgi import WSGIServer

app = flask.Flask(__name__)
app.debug = True

# app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.before_request
def before_request():
    print('before request')


@app.route("/")
def hello():
    print("Recieved")
    # return "lol"
    return flask.render_template('index.html')

@app.route("/tchat")
def tchat():
    return flask.render_template('trusted-data.html')

@app.route("/tchat-ratio")
def tchat_ratio():
    return flask.render_template('trusted-ratio-data.html')

@app.route("/gear")
def gear():
    return flask.render_template('geartimer.html')

@run_with_reloader
def run_server():
    print("Running...")

    # app.run(host="0.0.0.0", port="80")

    http_server = WSGIServer(('', 5000),  app)
    http_server.serve_forever()

run_server()
#test