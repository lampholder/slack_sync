# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='slacksync',
    version='0.1',
    description='Slack->Riot.im account sync',
    author='Thomas Lant',
    author_email='lampholder@gmail.com',
    url='https://github.com/lampholder/slack_sync',
    packages=find_packages(exclude=('tests', 'docs'))
)
