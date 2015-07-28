from flask import Flask, jsonify,request



def parseDate(date):
	if(date>=10):
		return '{0}'.format(date)
	elif(date>=0 or date<=10):
		return '0{0}'.format(date)
	else: 
		return '{0}'.format(date)
	

app = Flask(__name__)

@app.route('/')
def index():
	return "Hello"

@app.route('/json')
def jsontest():
	return jsonify(username='Rizki',password='test')


if(__name__=="__main__"):
	app.run()

