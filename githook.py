import json
import ipaddress
import requests
from flask import Flask, abort, request
import git
import os
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
#s
@app.route('/hooks', methods=['POST'])
def hook():
    print("Hook Recieved", flush=True)
    request_ip = ipaddress.ip_address(u'{0}'.format(request.remote_addr))
    hook_blocks = requests.get('https://api.github.com/meta').json()['hooks']
    for block in hook_blocks:
        if ipaddress.ip_address(request_ip) in ipaddress.ip_network(block):
            break
    else:
        print("failed to authenticate from IP " + str(request_ip), flush=True)
        abort(403)
    data = json.loads(request.data)
    repo_name = data["repository"]["name"].lower()
    g = git.cmd.Git(os.path.expanduser("~/develop/" + repo_name))
    g.pull()
    return "OK"

if __name__ == "__main__":
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
