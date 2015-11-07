import json

from flask.app import Flask
import main_component
from flask import Blueprint, render_template, jsonify, request

meloentjoer = Blueprint('meloentjoer', __name__)


@meloentjoer.route('/retrieve/<string:word>', methods=['GET'])
def retrieve_route(word):
    word_list = main_component.autocomplete_service.get_words(word)
    return json.dumps(word_list)


@meloentjoer.route('/search', methods=['POST'])
def search_route():
    json_return = request.get_json()
    source = json_return['source']
    destination = json_return['destination']
    data = main_component.search_service.get_direction(source, destination)
    next_bus = main_component.search_service.get_next_bus(source, destination, source)
    rendered_element = render_template('response.html', entries=data, next_bus=next_bus)
    return jsonify(data=rendered_element)


@meloentjoer.route('/')
def index():
    return render_template('autocomplete.html', host_url=main_component.general_config.get_host_url())


meloentjoer_app = Flask(__name__)
meloentjoer_app.register_blueprint(meloentjoer, url_prefix='/meloentjoer')
