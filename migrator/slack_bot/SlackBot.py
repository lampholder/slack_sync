# coding=utf-8
"""Handles registration of the app with Slack"""

import hmac
import json
import hashlib
from flask import request
from migrator import app
from migrator import config
from migrator.slack_bot import Slack
from migrator.slack_bot import Matrix

@app.route("/migrator/list", methods=["GET"])
def list_users():
    """List the users"""
    bot_access_token = request.cookies.get('bot_access_token')
    request.cookies.get('bot_user_id')
    request.cookies.get('team_id')
    request.cookies.get('team_name')

    slack = Slack(bot_access_token)
    matrix = Matrix('https://matrix.lant.uk', config['matrix']['registration_secret'])

    slack_users = slack.list_users()['members']
    human_users = [profile for profile in slack_users
                   if profile['is_bot'] is False
                   and profile['id'] != 'USLACKBOT'] # Why is slack's slackbot not a bot?


    for human in human_users:
        mac = hmac.new(key='ABC123',
                       digestmod=hashlib.sha1)
        mac.update(human['name'])

        url = 'https://matrix.org/migrator/claim?code=%s' % mac.hexdigest()

        message = 'Hi %s, please go to %s to claim your Riot.im account!' % (human['name'], url)
        slack.direct_message(human['id'], message)
        print 'Sending ' + message + ' to ' + human['name']

    return json.dumps(human_users)
