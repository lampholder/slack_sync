# coding=utf-8
"""Handles registration of the app with Slack"""

import json
from flask import request
from migrator import app
from migrator import config
from migrator.slack_bot import Slack

@app.route("/migrator/list", methods=["GET"])
def list_users():
    """Slack OAuth gubbins"""
    bot_access_token = request.cookies.get('bot_access_token')
    request.cookies.get('bot_user_id')
    request.cookies.get('team_id')
    request.cookies.get('team_name')

    slack = Slack(bot_access_token)

    slack_users = slack.list_users()['members']
    human_users = [profile for profile in slack_users
                   if profile['is_bot'] == False
                   and profile['id'] != 'USLACKBOT'] # Why is slack's slackbot not a bot?

    for human in human_users:
        slack.direct_message(human['id'], 'hiya!')

    return json.dumps(human_users)
