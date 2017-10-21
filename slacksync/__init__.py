import yaml
from flask import Flask

config = yaml.load(open('config.yaml', 'r'))
app = Flask(__name__,
            static_url_path=config['local']['mount'] + '/static',
            static_folder='static')
