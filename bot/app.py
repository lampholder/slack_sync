# coding=utf-8
"""Docstring"""

import yaml
from flask import Flask, request

from Slack import Slack

app = Flask(__name__)
config = yaml.load(open('config.yaml', 'r'))

@app.route("/begin_auth", methods=["GET"])
def pre_install():
    """Slack OAuth gubbins"""
    return '''
        <a href="https://slack.com/oauth/authorize?scope={0}&client_id={1}">
            Add to Slack
        </a>
    '''.format('chat:write:bot', config['slack']['client_id'])

@app.route("/finish_auth", methods=["GET", "POST"])
def post_install():
    """Slack OAuth gubbins"""
    auth_code = request.args['code']

    return Slack.complete_oauth(config['slack']['client_id'],
                                config['slack']['secret'],
                                auth_code)
