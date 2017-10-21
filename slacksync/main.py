# coding=utf-8
"""Docstring"""

from slacksync import app
from slacksync.slack_app import SlackApp
from slacksync.claim_matrix_account import ClaimMatrixAccount

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=23865)
