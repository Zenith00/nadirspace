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
from juggernaut import Juggernaut
from werkzeug.contrib.fixers import ProxyFix
jug = Juggernaut()
from flask import escape
import time
from gevent.wsgi import WSGIServer
from utils import utils_text, utils_file
app = flask.Flask(__name__)
app.debug = True

# app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.before_request
def before_request():
    print('before request')


@app.route("/")
def hello():
    print("Recieved")
    return "Bip Bop. Working!"
    # return flask.render_template('index.html')

@app.route("/tchat")
def tchat():
    print("Recieved")
    return flask.render_template('trusted-data.html')

@app.route("/tchat-ratio")
def tchat_ratio():
    print("Recieved")
    return flask.render_template('trusted-ratio-data.html')

@app.route("/gear")
def gear():
    print("Recieved")
    return flask.render_template('geartimer.html')

@app.route('/logs')
def index():
    LOG_FILE = "/home/austin/develop/discbots/logfile.txt"
    MAX_LEN = -500
    with open(LOG_FILE, 'r') as f:
        log_buffer = f.readlines()
    return flask.render_template('logger.html', log_buffer=log_buffer[MAX_LEN:])



def follow(follow_file):
    follow_file.seek(0, 2)
    while True:
        line = follow_file.readline()
        if not line:
            time.sleep(0.1)
            continue
        line = escape(line)
        jug.publish('logger', line)


@run_with_reloader
def run_server():
    print("Running...")
    app.wsgi_app = ProxyFix(app.wsgi_app)
    # app.run(host="0.0.0.0", port="80")
    server = WSGIServer(('0.0.0.0', 5000),  app)
    jobs = [gevent.spawn(follow, open(LOG_FILE)),
            gevent.spawn(http_server.serve_forever)]
    print("Run2")
    # server.serve_forever()


if __name__ == '__main__':
    run_server()

#test