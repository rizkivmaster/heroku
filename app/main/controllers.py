from flask import Blueprint, render_template, jsonify
import os

main = Blueprint('main',__name__)

@main.route('/')
def index():
	return os.environ["DATABASE_URL"]

@main.route('json')
def jsontest():
	return jsonify(username='Rizki',password='test')


	
