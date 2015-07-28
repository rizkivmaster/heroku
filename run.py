from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
	return "Hello"

@app.route('/json')
def jsontest():
	return jsonify(username='Rizki',password='test')

if(__name__=="__main__"):
	app.run()

