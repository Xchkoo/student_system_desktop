from flask import Flask
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['UPLOAD_FOLDER'] = 'app_mask/UPLOAD/'
app.config['JSON_AS_ASCII'] = False
login_manager = LoginManager()
login_manager.init_app(app)

from app_mask import views


