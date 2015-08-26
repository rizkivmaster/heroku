from flask import Flask
from app.shalat.controllers import shalat
from app.main.controllers import main
from app.jarvis import jarvis
from app.journalia import joernalia
from app.meloentjoer import meloentjoer

app = Flask(__name__)

app.logger.info('Loading meloentjoer')
app.register_blueprint(meloentjoer,url_prefix='/meloentjoer')

# app.register_blueprint(main,url_prefix='/')
app.register_blueprint(shalat,url_prefix='/shalat')
app.register_blueprint(jarvis,url_prefix='/jarvis')
app.register_blueprint(joernalia,url_prefix='/joernalia')