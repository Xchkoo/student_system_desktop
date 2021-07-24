from flask import Flask
from flask_login import LoginManager
from flask import Blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['UPLOAD_FOLDER'] = 'app_mask/UPLOAD/'
app.config['JSON_AS_ASCII'] = False


from app_mask import views


