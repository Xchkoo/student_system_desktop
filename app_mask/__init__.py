from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['UPLOAD_FOLDER'] = 'app_mask/UPLOAD/'

from app_mask import views
