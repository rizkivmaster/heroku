from flask import Flask, jsonify,request
from bs4 import BeautifulSoup
import urllib2


def scrap(url):
        html = urllib2.urlopen(url).read()
        scrapper = BeautifulSoup(html,"html.parser")
        return scrapper

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

