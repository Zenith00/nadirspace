# from urllib import request

# from flask import Flask, abort, request
import hashlib
import traceback
from ipinfodb import API as ipapi
import TOKENS
from flask_sse import sse
from gevent import monkey
from werkzeug.wrappers import Response

monkey.patch_all()
import flask
import index2
import pymongo

from functools import wraps
from flask import request, Response

import jinja2

mongo = pymongo.MongoClient("mongodb://{usn}:{pwd}@nadir.space".format(usn=TOKENS.MONGO_USN, pwd=TOKENS.MONGO_PASS))
auth_collection = mongo.get_database("website").get_collection("authentication")


# from utils import utils_text, utils_file

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


import sys, os

os.environ["PYTHONUNBUFFERED"] = "True"

sys.stdout = Unbuffered(sys.stdout)

app = flask.Flask(__name__)

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader('/home/austin/develop/textbasedproject'),
])
app.jinja_loader = my_loader

app.debug = True
app.register_blueprint(sse, url_prefix="/logger")
app.config["REDIS_URL"] = "redis://localhost"
# app.config["TEMPLATES_AUTO_RELOAD"] = True
LOG_FILE = "/home/austin/develop/discbots/logfile.txt"
MAX_LEN = -1000


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    print("Checking!!")
    input_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
    # print(input_hash)

    result = auth_collection.find_one({"username": username, "password": input_hash})
    # return username == 'admin' and password == 'secret'
    if result:
        print("Auth Success")
        return True
    else:
        print("Auth Failure")
        return False


def authenticate():
    """Sends a 401 response that enables basic auth"""
    print("FAILED AUTH")
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            print("Failed TO Authenticatae")
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@app.route("/")
def hello():
    print("Recieved")
    return "Bip Bop. Working!\n"
    # return flask.render_template('index.html')

@app.route("/new")
def new():
    print("Recieved")
    # return "Bip Bop. Working!\n"
    return flask.render_template('new.html')


@app.route("/tchat")
def tchat():
    print("Recieved")
    return flask.render_template('trusted-data.html')


@app.route("/tchat-ratio")
def tchat_ratio():
    print("Recieved")
    return flask.render_template('trusted-ratio-data.html')


@app.route("/prison")
def prison():
    return flask.render_template('prison.html')

@app.route("/tbag")
def tbag():
    return flask.render_template('tbag.html')


@app.route("/gear")
def gear():
    print("Recieved")
    return flask.render_template('geartimer.html')


@app.route('/logstr')
@requires_auth
def index():
    with open(LOG_FILE, 'r') as f:
        log_buffer = f.readlines()
    return flask.render_template('logger.html', log_buffer=log_buffer[MAX_LEN:])


@app.route('/config')
def config():
    print("aaaa")

    return flask.render_template('parser.html')

@app.route('/hackmedaddy')
def hack():
    try:
        ipinfoapi = ipapi(TOKENS.ip_api)
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        data_dict = ipinfoapi.GetCity(ip)

        ua = request.headers.get('User-Agent')
        return ip + "\r\n" + ua + "\r\n" + str(data_dict)
    except:
        return traceback.format_exc()

@app.route('/config', methods=['POST'])
def parser():
    print("Asdf")
    print(dict(request.form))
    text = request.form.get('taname')
    print(text)
    print("bb")
    processed_text = index2.parse(text)
    return str(processed_text)

log_obj = open(LOG_FILE, "r")

def tail_F(some_file):
    first_call = True
    try:
        while True:
            try:
                if first_call:
                    log_obj.seek(0, 2)
                    first_call = False
                latest_data = log_obj.read()
                while True:
                    if '\n' not in latest_data:
                        latest_data += log_obj.read()
                        if '\n' not in latest_data:
                            yield ''
                            if not os.path.isfile(some_file):
                                break
                            continue
                    latest_lines = latest_data.split('\n')
                    if latest_data[-1] != '\n':
                        latest_data = latest_lines[-1]
                    else:
                        latest_data = log_obj.read()
                    for line in latest_lines[:-1]:
                        yield line + '\n'
            except IOError:
                yield ''
            except:
                pass
                yield traceback.format_exc()
    except:
        yield traceback.format_exc()

@app.route('/logstream')
def logger():
    return Response(tail_F(LOG_FILE), mimetype="text/event-stream")


# @run_with_reloader
# def run_server():
#     app.run(debug=True,
#             host='0.0.0.0',
#             port=8000,
#             threaded=True)
#     # print("Running...")
#     # # app.wsgi_app = ProxyFix(app.wsgi_app)
#     # http_server = WSGIServer(('0.0.0.0', 8000), DebuggedApplication(app))
#     # http_server.serve_forever()


if __name__ == '__main__':
    app.run()