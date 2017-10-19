# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='migrator',
    version='0.1',
    description='Slack->Riot.im migrator',
    author='Thomas Lant',
    author_email='lampholder@gmail.com',
    url='https://github.com/lampholder/slack_migrator',
    packages=find_packages(exclude=('tests', 'docs'))
)
