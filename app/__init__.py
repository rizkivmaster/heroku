from flask import Flask
from app.shalat.controllers import shalat
from app.main.controllers import main
from app.jarvis.controllers import jarvis

app = Flask(__name__)

app.register_blueprint(main,url_prefix='/')
app.register_blueprint(shalat,url_prefix='/shalat')
app.register_blueprint(jarvis,url_prefix='/jarvis')
