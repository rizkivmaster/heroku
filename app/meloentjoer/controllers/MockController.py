from app.meloentjoer.controllers.NextBus import NextBus
from app.meloentjoer.search.MockSearchTransducer import MockSearchTransducer
from flask import Blueprint, render_template, jsonify, request
from app.meloentjoer.config.GeneralConfig import common_config
import json

host_url = common_config.get_host_name()

meloentjoer = Blueprint('meloentjoer', __name__)


@meloentjoer.route('/retrieve/<string:word>')
def retrieve(word):
    word_list = ['Slipi Kemanggisan', 'Slipi Petamburan']
    return json.dumps(word_list)


@meloentjoer.route('/search', methods=['POST'])
def search():
    json_object = request.get_json()
    source = json_object['source']
    destination = json_object['destination']
    search_transducer = MockSearchTransducer()
    data = search_transducer.get_direction(source, destination)

    next_bus = NextBus()
    next_bus.eta = 2
    next_bus.current_stop = 'Slipi Kemanggisan'
    return jsonify(data=render_template('response.html', entries=data, next_bus=next_bus))


@meloentjoer.route('/')
def index():
    return render_template('autocomplete.html', host_url=host_url)
