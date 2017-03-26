import json
# from urllib import request
import ipaddress
import traceback

import requests
# from flask import Flask, abort, request
import gevent
from gevent import monkey
from werkzeug.wrappers import Response
import sh
from flask_sse import sse
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
# from utils import utils_text, utils_file

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)

import sys

sys.stdout = Unbuffered(sys.stdout)



app = flask.Flask(__name__)
app.debug = True
app.register_blueprint(sse, url_prefix="/logger")

# app.config["TEMPLATES_AUTO_RELOAD"] = True
LOG_FILE = "/home/austin/develop/discbots/logfile.txt"
MAX_LEN = -500
@app.before_request
def before_request():
    print('before request')
    return


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

    with open(LOG_FILE, 'r') as f:
        log_buffer = f.readlines()
    return flask.render_template('logger.html', log_buffer=log_buffer[MAX_LEN:])


@app.route('/logger')
def logger(follow_file):

    follow_file.seek(0, 2)
    while True:
        line = follow_file.readline()
        if not line:
            time.sleep(0.1)
            continue
        line = escape(line)
        sse.publish({"message":line}, type="log")
    # def logStream():
    #     import sh
    #     tail = sh.tail("-f", LOG_FILE, _iter=True)
    #     while True:
    #         try:
    #             yield tail.next()
    #         except:
    #             print("Nothing Found")
    #             time.sleep(0.1)
        # while True:
        #     try:
        #         for line in sh.tail("-f", LOG_FILE, _iter=True):
        #             print(line)
        #             yield line
        #     except:
        #         print(traceback.format_exc())
        #         print("None")
        #         time.sleep(0.1)
        #         yield None
    # def generate():
    #     with open('job.log') as f:
    #         while True:
    #             yield f.read()
    #             time.sleep(1)
    # return Response(logStream(), mimetype="text/event-stream")


@run_with_reloader
def run_server():
    print("Running...")
    app.wsgi_app = ProxyFix(app.wsgi_app)
    # app.run(host="0.0.0.0", port="80")
    http_server = WSGIServer(('0.0.0.0', 5000),  app)
    jobs = [gevent.spawn(logger, open(LOG_FILE)),
            gevent.spawn(http_server.serve_forever)]
    http_server.serve_forever()
    print("Run2")
    # server.serve_forever()

if __name__ == '__main__':
    run_server()

#test