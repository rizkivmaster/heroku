from flask import Flask
from app.shalat.controllers import shalat
from app.main.controllers import main
from app.jarvis import jarvis
from app.journalia import journalia

app = Flask(__name__)

#app.register_blueprint(main,url_prefix='/')
app.register_blueprint(shalat,url_prefix='/shalat')
app.register_blueprint(jarvis,url_prefix='/jarvis')
app.register_blueprint(journalia,url_prefix='/joernalia')
