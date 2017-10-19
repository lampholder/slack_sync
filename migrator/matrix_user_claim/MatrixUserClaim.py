"""Docstring"""
from migrator import app

from flask import render_template

@app.route('/migrator/claim/')
def claim_form():
    return render_template('claim.html',
                            slack_team='https://openmarket.slack.com',
                            slack_username='@lampholder',
                            matrix_homeserver='https://matrix.org',
                            matrix_id='@mxid:matrix.org')
