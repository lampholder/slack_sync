# coding=utf-8
"""Docstring"""

from migrator import app
from migrator.slack_app_registration import SlackAppRegistration
from migrator.matrix_user_claim import MatrixUserClaim

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=23865)
