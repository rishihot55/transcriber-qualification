from app.routes import api

from flask import Flask

app = Flask(__name__)
app.config['DATA_DIR']='app/db'
app.config['MAX_CONTENT_LENGTH']=300 * 1024
app.config['SECRET_KEY']='randomstr'
app.register_blueprint(api)
