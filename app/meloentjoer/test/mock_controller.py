from app.meloentjoer import main_component
from flask import Blueprint, render_template
from flask.app import Flask

meloentjoer = Blueprint('meloentjoer', __name__)


@meloentjoer.route('/')
def index():
    return render_template('autocomplete.html', host_url=main_component.general_config.get_host_url())

meloentjoer_app = Flask(__name__)
meloentjoer_app.register_blueprint(meloentjoer, url_prefix='/meloentjoer')
