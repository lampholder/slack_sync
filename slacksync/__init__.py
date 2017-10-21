import yaml
from flask import Flask

app = Flask(__name__,
            static_url_path='/migrator/static',
            static_folder='static')
config = yaml.load(open('config.yaml', 'r'))
