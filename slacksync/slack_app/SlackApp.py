# coding=utf-8
"""Handles registration of the app with Slack"""

import json
import hmac
import urllib
import hashlib

from flask import jsonify
from flask import request
from flask import redirect
from flask import make_response
from flask import render_template

from slacksync import app
from slacksync import config
from slacksync.interfaces import Slack
from slacksync.interfaces import Matrix

mount = config['local']['mount']

@app.route(mount + '/app/install', methods=['GET'])
def pre_install():
    """Slack OAuth gubbins"""
    params = {'client_id': config['slack']['client_id'],
              'scope': 'bot',
              'redirect_uri': 'https://lant.uk/services/slacksync/app/finish_auth'} #TODO: Don't hardcode this

    url = 'https://slack.com/oauth/authorize?&client_id=%s&scope=bot' % urllib.urlencode(params)

    return redirect(url, 302)

@app.route(mount + '/app/finish_auth', methods=['GET', 'POST'])
def post_install():
    """Slack OAuth gubbins"""
    auth_code = request.args['code']

    tokens = Slack.complete_oauth(client_id=config['slack']['client_id'],
                                  client_secret=config['slack']['secret'],
                                  code=auth_code)

    response = make_response(redirect(mount +'/app/sync', 302))

    try:
        response.set_cookie('bot_access_token', tokens['bot']['bot_access_token'])
        response.set_cookie('bot_user_id', tokens['bot']['bot_user_id'])
        response.set_cookie('team_id', tokens['team_id'])
        response.set_cookie('team_name', tokens['team_name'])
    except Exception, e:
        return 'Unable to register app with slack.'

    return response

@app.route(mount + '/app/sync', methods=['GET'])
def init_sync():
    """Show the UX for initating the migration."""

    bot_access_token = request.cookies.get('bot_access_token')
    slack = Slack(bot_access_token)

    slack_users = slack.list_users()['members']
    human_users = [profile for profile in slack_users
                   if profile['is_bot'] is False
                   and profile['id'] != 'USLACKBOT'] # Why is slack's slackbot not a bot?

    users = [{'name': human['real_name'] if 'real_name' in human else human['name'],
              'id': human['id'],
              'img': human['profile']['image_48']}
             for human in human_users]

    return render_template('sync.html',
                           mount=mount,
                           users=users)

@app.route(mount + '/api/users', methods=['GET'])
def list_users():
    """List all of the human users in this Slack team"""
    bot_access_token = request.cookies.get('bot_access_token')

    slack = Slack(bot_access_token)
    slack_users = slack.list_users()['members']
    human_users = [profile for profile in slack_users
                   if profile['is_bot'] is False
                   and profile['id'] != 'USLACKBOT'] # Why is slack's slackbot not a bot?

    return jsonify(human_users)

@app.route(mount + '/api/sync/<string:slack_id>', methods=['POST'])
def sync(slack_id):
    """Sync a Slack id into matrix and advise the Slack user how to claim it"""
    bot_access_token = request.cookies.get('bot_access_token')
    request_body = request.get_json()

    slack = Slack(bot_access_token)

    homeserver = request_body['homeserver']
    registration_secret = request_body['registration_secret']

    user = slack.user(slack_id)
    team = slack.team()

    def assemble_mac(user, team, homeserver, secret):
        """Generate a mac to authenticate the api request."""
        mac = hmac.new(key=secret,
                       digestmod=hashlib.sha1)
        mac.update(user)
        mac.update('\x00')
        mac.update(team)
        mac.update('\x00')
        mac.update(homeserver)

        return mac.hexdigest()

    user_name = user['user']['name']
    team_name = team['team']['name']

    params = {'code': assemble_mac(user=user_name,
                                   team=team_name,
                                   homeserver=homeserver,
                                   secret=config['local']['secret']),
              'user': user_name,
              'team': team_name,
              'homeserver': homeserver}

    url = (config['local']['sync_server'] +
           config['local']['mount'] +
           '/app/claim?%s' % urllib.urlencode(params))

    message = 'Hi, @%s; please go to %s to sync your Slack id with Riot.im!' % (user_name, url)

    try:
        matrix = Matrix(homeserver)
        matrix.create_user(user_name, registration_secret)
        slack.direct_message(user['user']['id'], message)
        return 'SYNC SUCCEEDED'
    except Exception, exc:
        if 'M_USER_IN_USE' in exc.message:
            return 'SYNC FAILED - MXID IN USE', 404
        return 'SYNC FAILED', 404
