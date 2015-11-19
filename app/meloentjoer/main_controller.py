import json

from app.meloentjoer.services.entity.BuswayMode import BuswayMode
from flask.app import Flask
import main_component
from flask import Blueprint, render_template, jsonify, request

meloentjoer = Blueprint('meloentjoer', __name__)


@meloentjoer.route('/retrieve/<string:word>', methods=['GET'])
def retrieve_route(word):
    word_list = main_component.autocomplete_service.get_words(word)
    return json.dumps(word_list)


def __get_next_bus(data, station):
    """
    :type data: list
    :param data:
    :return:
    """
    next_bus = None
    if len(data) > 0 and len(data[0].mode_list) > 0:
        first_bus_route = data[0].mode_list[0]
        assert isinstance(first_bus_route, BuswayMode)
        next_bus = main_component.search_service.get_next_bus(first_bus_route.heading_from, first_bus_route.heading_to,
                                                              station)
    return next_bus


@meloentjoer.route('/search', methods=['POST'])
def search_route():
    json_return = request.get_json()
    source = json_return['source']
    destination = json_return['destination']
    data = main_component.search_service.get_direction(source, destination)
    next_bus = __get_next_bus(data, source)
    rendered_element = render_template('response.html', entries=data, next_bus=next_bus)
    return jsonify(data=rendered_element)


@meloentjoer.route('/')
def index():
    return render_template('autocomplete.html', host_url=main_component.general_config.get_host_url())


meloentjoer_app = Flask(__name__)
meloentjoer_app.register_blueprint(meloentjoer, url_prefix='/meloentjoer')
