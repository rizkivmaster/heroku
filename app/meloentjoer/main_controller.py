import json
from flask.app import Flask

import main_component
from flask import Blueprint, render_template, jsonify, request

meloentjoer = Blueprint('meloentjoer', __name__)

main_component.start()


@meloentjoer.route('/retrieve/<string:word>')
def retrieve_route(self, word):
    word_list = main_component.autocomplete_service.get_words(word)
    return json.dumps(word_list)


@meloentjoer.route('/search', methods=['POST'])
def search_route(self):
    json_return = request.get_json()
    source = json_return['source']
    destination = json_return['destination']
    data = main_component.search_service.get_direction(source, destination)
    return jsonify(data=render_template('response.html', entries=data))


@meloentjoer.route('/')
def index(self):
    return render_template('autocomplete.html', host_url=self.host_url)


meloentjoer_app = Flask(__name__)
meloentjoer_app.register_blueprint(meloentjoer, 'meloentjoer/')
