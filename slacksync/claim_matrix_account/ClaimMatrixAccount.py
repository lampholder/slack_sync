"""Docstring"""
import hmac
import hashlib

from flask import request
from flask import render_template

from slacksync import app
from slacksync import config
from slacksync.interfaces import Matrix 
mount = config['local']['mount']

def passgen(mxid):
    """Function for translating a mxid into a known-but-unguessable password.
    Some element of this bad boy needs to be excluded from version control."""
    return hashlib.md5(mxid + config['local']['password_gen_secret']).hexdigest()

@app.route(mount + '/app/claim')
def claim_form():
    user = request.args.get('user')
    team = request.args.get('team')
    code = request.args.get('code')
    homeserver = request.args.get('homeserver')

    mac = hmac.new(key=config['local']['sync_secret'],
                   digestmod=hashlib.sha1)
    mac.update(user)
    mac.update('\x00')
    mac.update(team)
    mac.update('\x00')
    mac.update(homeserver)

    if code != mac.hexdigest():
        return 'Invalid request', 400

    return render_template('claim.html',
                            mount=mount,
                            slack_team=team,
                            slack_username='@%s' % user,
                            matrix_homeserver=homeserver,
                            code=code,
                            matrix_id=user)

@app.route(mount + '/api/claim', methods=['POST'])
def claim():
    request_body = request.get_json()

    import json
    print json.dumps(request_body)
 
    user = request_body['user']
    password = request_body['password']
    homeserver = request_body['homeserver']
    team = request_body['team']
    code = request_body['code']

    mac = hmac.new(key=config['local']['sync_secret'],
                   digestmod=hashlib.sha1)
    mac.update(user)
    mac.update('\x00')
    mac.update(team)
    mac.update('\x00')
    mac.update(homeserver)

    if code != mac.hexdigest():
        print code, '!=', mac.hexdigest()
        return 'Invalid request', 400

    matrix = Matrix(homeserver)

    print matrix.change_password(user, passgen(user), password)
    return 'Success!'
