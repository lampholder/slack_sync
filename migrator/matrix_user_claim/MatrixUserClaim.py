"""Docstring"""
import hmac
import hashlib

from flask import request
from flask import render_template

from migrator import app
from migrator import config
from migrator.slack_bot import Matrix

matrix = Matrix(config['matrix']['homeserver'], config['matrix']['registration_secret'])

@app.route('/migrator/claim')
def claim_form():
    name = request.args.get('name')
    team = request.args.get('team')
    code = request.args.get('code')

    mac = hmac.new(key='ABC123',
                   digestmod=hashlib.sha1)
    mac.update(name)
    if code != mac.hexdigest():
        return 'Invalid request'

    return render_template('claim.html',
                            slack_team=team,
                            slack_username='@%s' % name,
                            matrix_homeserver='https://matrix.lant.uk',
                            matrix_id='@%s:lant.uk' % name)

app.route('/migrator/executeClaim', method=['POST'])
def claim():
    matrix.change_password('lampholder', 'werp', 'nwerp')
    return ''
