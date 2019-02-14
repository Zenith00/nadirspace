import json
import ipaddress
from datetime import time
import requests
from flask import Flask, abort, request
import git
import os
from gevent.pywsgi import WSGIServer
from werkzeug.exceptions import ServiceUnavailable, Forbidden

app = Flask(__name__)

def is_github_ip(ip_str):
    """Verify that an IP address is owned by GitHub."""
    if isinstance(ip_str, bytes):
        ip_str = ip_str.decode()

    ip = ipaddress.ip_address(ip_str)
    if ip.version == 6 and ip.ipv4_mapped:
        ip = ip.ipv4_mapped

    for block in load_github_hooks():
        if ip in ipaddress.ip_network(block):
            return True
    return False


def load_github_hooks(github_url='https://api.github.com'):
    """Request GitHub's IP block from their API.
    Return the IP network.
    If we detect a rate-limit error, raise an error message stating when
    the rate limit will reset.
    If something else goes wrong, raise a generic 503.
    """
    try:
        resp = requests.get(github_url + '/meta')
        if resp.status_code == 200:
            return resp.json()['hooks']
        else:
            if resp.headers.get('X-RateLimit-Remaining') == '0':
                reset_ts = int(resp.headers['X-RateLimit-Reset'])
                raise ServiceUnavailable('Rate limited from GitHub')
            else:
                raise ServiceUnavailable('Error reaching GitHub')
    except (KeyError, ValueError, requests.exceptions.ConnectionError):
        raise ServiceUnavailable('Error reaching GitHub')

# s s s

@app.route('/hooks', methods=['POST'])
def hook():
    print("Hook Recieved", flush=True)
    print(request.remote_addr, flush=True)
    if not is_github_ip(request.remote_addr):
        raise Forbidden('Not from github')

    data = json.loads(request.data)
    repo_name = data["repository"]["name"].lower()
    g = git.cmd.Git(os.path.expanduser("~/develop/" + repo_name))
    g.pull()
    return "OK"

if __name__ == "__main__":
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
