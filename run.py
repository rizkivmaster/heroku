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

@app.route('/magrib/<int:day>')
def magrib(day):
	halaman = scrap("http://jadwalsholat.pkpu.or.id/")
	tabel = halaman.find('table',{'class':'table_adzan'})
	records = tabel.findAll('tr')
	headers = [fieldName.text for fieldName in records[3].findAll('td')]
	contents = [ [cell.text for cell in row.findAll('td')] for row in records[4:]]
	fullContents = dict()
	for content in contents:
	    fullContents[content[0]]=dict(zip(headers,content))
	return jsonify(fullContents[parseDate(day)])
	
	

if(__name__=="__main__"):
	app.run()

