import json
import ipaddress
import requests
from flask import Flask, abort, request
import git

app = Flask(__name__)


@app.route('/hooks',methods=['POST'])
def hook():
    print("Hook Recieved")
    request_ip = ipaddress.ip_address(u'{0}'.format(request.remote_addr))
    hook_blocks = requests.get('https://api.github.com/meta').json()['hooks']
    for block in hook_blocks:
        if ipaddress.ip_address(request_ip) in ipaddress.ip_network(block):
            break
    else:
        abort(403)
    data = json.loads(request.data)
    repo_name = data["repository"]["name"]
    g = git.cmd.Git("~/develop/" + repo_name)
    g.pull()
    # print "New commit by: {}".format(data['commits'][0]['author']['name'])

if __name__ == "__main__":
  app.run(host="0.0.0.0", port="4200")
