import app_mask
APP_PATH = r'H:\MyRepository\student_system_web'
APP_PATH = APP_PATH.replace('\\', '/')
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'raw', 'png', 'bmp', 'PNG', 'JPG', 'BMP', 'RAW']
HOST = '0.0.0.0'
PORT = '80'
is_commit_word = {'是否提交', '提交', '作业', '作业提交'}
# PROJECT_ABSOLUTE_PATH = r'H:\MyRepository\student_system_web'
PROJECT_ABSOLUTE_PATH = APP_PATH
DATABASE = PROJECT_ABSOLUTE_PATH + r'\app_mask\database\database.db'
