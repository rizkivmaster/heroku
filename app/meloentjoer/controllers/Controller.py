import json
from flask import Blueprint, render_template, jsonify, request


class MeloentjoerController(object):
    meloentjoer = Blueprint('meloentjoer', __name__)

    def __init__(self, common_config, search_transducer, autocomplete):
        """
        :type autocomplete: app.meloentjoer.search.AutocompleteService.AutocompleteService
        :type common_config: app.meloentjoer.config.CommonConfig.CommonConfig
        :type search_transducer: app.meloentjoer.search.SearchService.SearchService
        :param common_config:
        :return:
        """
        self.host_url = common_config.get_host_name()
        self.search_transducer = search_transducer
        self.autocomplete = autocomplete

    @meloentjoer.route('/retrieve/<string:word>')
    def retrieve_route(self, word):
        word_list = self.autocomplete.get_words(word)
        return json.dumps(word_list)

    @meloentjoer.route('/search', methods=['POST'])
    def search_route(self):
        json_return = request.get_json()
        source = json_return['source']
        destination = json_return['destination']
        data = self.search_transducer.get_direction(source, destination)
        return jsonify(data=render_template('response.html', entries=data))

    @meloentjoer.route('/')
    def index(self):
        return render_template('autocomplete.html', host_url=self.host_url)
