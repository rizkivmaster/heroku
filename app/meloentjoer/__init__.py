from flask import Blueprint, render_template, jsonify,request
from controllers import retrieveSuggestion,node,getDirection
import json
import os
	
host_url = os.environ['HOST_URL']

meloentjoer = Blueprint('meloentjoer',__name__)
@meloentjoer.route('/retrieve/<string:word>')
def get(word):
	wordList = retrieveSuggestion(node,word)
	return json.dumps(wordList)



# @meloentjoer.route('/search',methods=['POST'])
# def search():
# 	json = request.get_json()
# 	source = json['source']
# 	destination = json['destination']
# 	return jsonify(data=getDirection(source,destination))

@meloentjoer.route('/search',methods=['POST'])
def search():
	json = request.get_json()
	source = json['source']
	destination = json['destination']
	data=getDirection(source,destination)
	return jsonify(data=render_template('response.html',entries=data))

@meloentjoer.route('/')
def index():
	return render_template('autocomplete.html',host_url=host_url)