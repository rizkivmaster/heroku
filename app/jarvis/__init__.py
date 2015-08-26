__author__ = 'traveloka'

from controllers import listDocument
from flask import Blueprint,jsonify,render_template

jarvis = Blueprint('jarvis',__name__)


@jarvis.route('/update')
def update():
    results = listDocument()
    ret = dict(data=results)
    return jsonify(ret)

@jarvis.route('/')
def open():
    return render_template('jarvis.html')