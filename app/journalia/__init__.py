__author__ = 'rizkivmaster'

from controllers import Record, recordAccessor
from flask import Blueprint, render_template, request,jsonify
import datetime,random
import os


home_url = os.environ['HOME_URL']
joernalia = Blueprint('journalia',__name__)

@joernalia.route('/page/<string:type>')
def page(type):
    postType = type
    entries = recordAccessor.getAllRecords(postType)
    debitSum = sum([entry.amount for entry in entries if entry.accountingType == 'DEBIT'])
    creditSum = sum([entry.amount for entry in entries if entry.accountingType == 'KREDIT'])
    return render_template('joernalia.html', postType=postType, entries=entries, debitSum=debitSum, creditSum=creditSum, home_url=home_url)

@joernalia.route('/bukubesar')
def bigbook():
    entries = recordAccessor.getAllRecords()
    debitSum = sum([entry.amount for entry in entries if entry.accountingType == 'DEBIT'])
    creditSum = sum([entry.amount for entry in entries if entry.accountingType == 'KREDIT'])
    return render_template('bukubesar.html', entries=entries, debitSum=debitSum, creditSum=creditSum, home_url=home_url)

def randomId():
    return random.randint(0,10000)

@joernalia.route('/add',methods=['POST'])
def addRecord():
    json = request.get_json()
    data = json['data']
    postType = json['postType']
    record = Record()
    record.date = datetime.datetime.fromtimestamp(data['time']/1000.0)
    record.accountingType = data['accountingType']
    record.notes = data['notes']
    record.amount = data['amount']
    record.accountingPost = data['accountingPost']
    record.accountingId = str(randomId())
    recordAccessor.addRecord(record)
    return jsonify(dict(postType=postType))



# @journalia.route('/all/sales',methods=['GET'])
# def getSalesRecords():
