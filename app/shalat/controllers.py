from flask import Blueprint,jsonify
from util.scrapper import *



shalat = Blueprint('shalat',__name__)


@shalat.route('/<int:day>')
def shalatx(day):
	halaman = scrap("http://jadwalsholat.pkpu.or.id/")
	tabel = halaman.find('table',{'class':'table_adzan'})
	records = tabel.findAll('tr')
	headers = [fieldName.text for fieldName in records[3].findAll('td')]
	contents = [ [cell.text for cell in row.findAll('td')] for row in records[4:]]
	fullContents = dict()
	for content in contents:
	    fullContents[content[0]]=dict(zip(headers,content))
	return jsonify(fullContents[parseDate(day)])