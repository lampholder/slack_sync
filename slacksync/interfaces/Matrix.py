# coding=utf-8
"""Matrix side of the Slack migrator."""

import json
import hmac
import hashlib
import requests

from matrix_client.client import MatrixClient
from matrix_client.errors import MatrixRequestError

def passgen(mxid):
    """Function for translating a mxid into a known-but-unguessable password.
    Some element of this bad boy needs to be excluded from version control."""
    return hashlib.md5(mxid + '\x00' + 'SALTY').hexdigest()

class Matrix(object):
    """For wrangling the Matrix users."""

    def __init__(self, server, registration_secret):
        self._server = server
        self._registration_secret = registration_secret

    def change_password(self, mxid, old_password, new_password):
        """Change a user's password.
        Warning: this function is slow as balls."""
        matrix = MatrixClient(self._server)
        matrix.login_with_password(username=mxid,
                                   password=old_password)

        body = {
            "auth": {
                "type": "m.login.password",
                "user": mxid,
                "password": old_password
            },
            "new_password": new_password
        }

        try:
            matrix.api._send('POST', '/account/password', body, api_path='/_matrix/client/r0')
            return True

        except MatrixRequestError as exception:
            print exception
            return False

    def create_user(self, mxid, password_function=passgen, admin=False):
        """Creates a user - the password is generated from a function."""

        mac = hmac.new(key=self._registration_secret,
                       digestmod=hashlib.sha1)

        password = password_function(mxid)

        mac.update(mxid)
        mac.update("\x00")
        mac.update(password)
        mac.update("\x00")
        mac.update("admin" if admin else "notadmin")

        body = {
            "user": mxid,
            "password": password,
            "mac": mac.hexdigest(),
            "type": "org.matrix.login.shared_secret",
            "admin": admin,
        }

        response = requests.post('%s/_matrix/client/api/v1/register' % self._server,
                                 data=json.dumps(body),
                                 headers={'Content-Type': 'application/json'})

        if response.code != 200:
            raise Exception(response.code, response.text)
        else:
            return True
