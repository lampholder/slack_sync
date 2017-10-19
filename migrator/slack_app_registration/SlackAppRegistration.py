# coding=utf-8
"""Handles registration of the app with Slack"""

from flask import request
from slackclient import SlackClient
from migrator import app
from migrator import config

@app.route("/migrator/install", methods=["GET"])
def pre_install():
    """Slack OAuth gubbins"""
    return '''
        <a href="https://slack.com/oauth/authorize?&client_id=255990322436.258854132450&scope=bot"><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>
    '''.format('chat:write:bot', config['slack']['client_id'])

@app.route("/migrator/finish_auth", methods=["GET", "POST"])
def post_install():
    """Slack OAuth gubbins"""
    auth_code = request.args['code']

    slack = SlackClient("")
    print slack.api_call('oauth.access',
                         client_id=config['slack']['client_id'],
                         client_secret=config['slack']['secret'],
                         code=auth_code)

    return 'Successfully installed!'
