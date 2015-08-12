__author__ = 'traveloka'

from controllers import listDocument,addObject
from flask import Blueprint,jsonify

jarvis = Blueprint('jarvis',__name__)


@jarvis.route('/')
def update():
    results = listDocument()
    return '['+','.join(results)+']'