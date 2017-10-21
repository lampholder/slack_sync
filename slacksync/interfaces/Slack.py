# coding=utf-8
"""Handles the Slack side of business."""

import time

from slackclient import SlackClient

class Slack(object):
    """Class for messaging the Slack users"""

    def __init__(self, slack_token):
        self._slack = SlackClient(slack_token)

    def listen(self):
        """Listens for inbound Slack events."""
        if self._slack.rtm_connect():
            while True:
                output = self._slack.rtm_read()
                for event in self._filter_slack_output(output):
                    self._process(event)
                time.sleep(1)

    def team(self):
        """Gets team details"""
        return self._slack.api_call('team.info')

    def list_users(self):
        """Lists all the users in the attached team."""
        return self._slack.api_call('users.list')

    def user(self, user_id):
        """Fetch the details for a specific user."""
        return self._slack.api_call('user.info',
                                    user=user_id)

    def direct_message(self, user, message):
        """Send a direct message to the specified user."""
        self._slack.api_call('chat.postMessage',
                             channel=user,
                             text=message,
                             as_user=True)

    @staticmethod
    def complete_oauth(client_id, client_secret, code):
        """Completes the oauth registrion with the code provided by slack."""
        slack = SlackClient("")

        return slack.api_call('oauth.access',
                              client_id=client_id,
                              client_secret=client_secret,
                              code=code)

    @staticmethod
    def _filter_slack_output(output):
        """We only want to react to messages, and we want to exclude certain users9
        (such as slackbot)"""
        barred_users = ['USLACKBOT']
        entries_to_process = [event for event in output
                              if event['type'] == 'message'
                              and event['user'] not in barred_users]

        return entries_to_process

    def _process(self, event):
        """Processes an inbound Slack event."""
        self.direct_message(event['user'], 'I don\'t understand humans.')
