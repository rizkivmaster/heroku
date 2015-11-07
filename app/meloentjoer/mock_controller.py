import json

from flask import Blueprint, render_template
from flask.app import Flask

meloentjoer = Blueprint('meloentjoer', __name__)


@meloentjoer.route('/retrieve/<string:word>')
def retrieve_route(word):
    word_list = ['ABCDE', 'EFGHI']
    return json.dumps(word_list)


@meloentjoer.route('/')
def index():
    return render_template('autocomplete.html', host_url='http://127.0.0.1:5000/meloentjoer/')


meloentjoer_app = Flask(__name__)
meloentjoer_app.register_blueprint(meloentjoer, url_prefix='/meloentjoer')
