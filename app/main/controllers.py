from flask import Blueprint, render_template, jsonify

main = Blueprint('main',__name__)

@main.route('/')
def index():
	return render_template('index.html');

@main.route('json')
def jsontest():
	return jsonify(username='Rizki',password='test')

	
