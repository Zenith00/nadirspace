import json
# from urllib import request
import ipaddress
import requests
# from flask import Flask, abort, request
import flask
app = flask.Flask(__name__)

@app.route("/")
def hello():
    print("Recieved")
    return "lol"
    # return flask.render_template('index.html')

@app.route("/tchat")
def tchat():
    return flask.render_template('trusted-data.html')


if __name__ == "__main__":
  app.run(host="0.0.0.0", port="5000")

