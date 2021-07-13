import sys

APP_PATH = sys.path[0]
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'raw', 'png', 'bmp', 'PNG', 'JPG', 'BMP', 'RAW']
HOST = '0.0.0.0'
PORT = '8080'
is_commit_word = {'是否提交', '提交', '作业', '作业提交'}
DATABASE = APP_PATH + r'/app_mask/database/database.db'

