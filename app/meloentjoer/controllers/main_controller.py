import json
from app.meloentjoer.accessors import bus_route_accessor, bus_estimate_accessor, bus_state_accessor, next_bus_accessor
from app.meloentjoer.fetcher import transportation_info_fetcher, busway_track_fetcher
from app.meloentjoer.services import autocomplete_service, search_service
from flask import Blueprint, render_template, jsonify, request

meloentjoer = Blueprint('meloentjoer', __name__)

# warming up
bus_estimate_accessor.start()
bus_state_accessor.reset()
next_bus_accessor.reset()
bus_route_accessor.reset()

transportation_info_fetcher.start()
busway_track_fetcher.start()

autocomplete_service.start()


@meloentjoer.route('/retrieve/<string:word>')
def retrieve_route(self, word):
    word_list = autocomplete_service.get_words(word)
    return json.dumps(word_list)


@meloentjoer.route('/search', methods=['POST'])
def search_route(self):
    json_return = request.get_json()
    source = json_return['source']
    destination = json_return['destination']
    data = search_service.get_direction(source, destination)
    return jsonify(data=render_template('response.html', entries=data))


@meloentjoer.route('/')
def index(self):
    return render_template('autocomplete.html', host_url=self.host_url)
