# coding=utf-8
"""Handles registration of the app with Slack"""

import json
from flask import request
from flask import make_response
from flask import render_template
from slackclient import SlackClient
from migrator import app
from migrator import config
from migrator.slack_bot import Slack

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
    tokens = slack.api_call('oauth.access',
                            client_id=config['slack']['client_id'],
                            client_secret=config['slack']['secret'],
                            code=auth_code)

    response = make_response(json.dumps(tokens), 200)

    response.set_cookie('bot_access_token', tokens['bot']['bot_access_token'])
    response.set_cookie('bot_user_id', tokens['bot']['bot_user_id'])
    response.set_cookie('team_id', tokens['team_id'])
    response.set_cookie('team_name', tokens['team_name'])

    print 'auth_code', auth_code
    #for token, value in tokens.iteritems():
    #    response.set_cookie(token, value)

    return response

@app.route('/migrator/migrate', methods=['GET'])
def migrate():
    """Show the UX for initating the migration."""

    bot_access_token = request.cookies.get('bot_access_token')
    slack = Slack(bot_access_token)

    slack_users = slack.list_users()['members']
    human_users = [profile for profile in slack_users
                   if profile['is_bot'] is False
                   and profile['id'] != 'USLACKBOT'] # Why is slack's slackbot not a bot?

    users = [{'name': human['real_name'],
              'img': human['profile']['image_48']}
             for human in human_users]

    return render_template('migrate.html',
                           users=users)
