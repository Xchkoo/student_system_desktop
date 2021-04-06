from app_mask import app, config, local_db, face_detect, ocr
from flask import render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import json


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/home/', methods=["GET"])
def home():
    return render_template('index.html')


@app.route('/about/', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/console/', methods=["GET", "POST"])
def console():
    return render_template('console.html')


@app.route('/face_view/', methods=['GET', 'POST'])
def face_view():
    return render_template('face_view.html')


# check
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


# face_register
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + 'REGISTER/', filename))
            # 转到数据库存储
            trans_id = local_db.register_trans(name=name, path=app.config['UPLOAD_FOLDER'] + 'REGISTER/' + filename)
            # 上传百度云
            result = face_detect.face_register(path=app.config['UPLOAD_FOLDER'] + "REGISTER/" + filename,
                                               trans_id=trans_id)
            # 如果检测失败了，就应该把刚刚的数据删掉
            if result == 'SUCCESS':
                return jsonify({'msg': 'SUCCESS'})
            elif result == 'face already exist':
                local_db.register_delete(trans_id)
                return jsonify({'msg': 'face already exist'})
            else:
                return jsonify({'msg': 'ILLEGAL'})
        return render_template("register.html")
    return render_template('register.html')


@app.route('/check_add_photo/', methods=['GET', 'POST'])
def check_add_photo():
    if request.method == 'POST':
        file = request.files['photo']
        pos = request.form['position']
        time = request.form['time']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER']+'ADD_PHOTO/check/', filename))
            res = face_detect.mask_detect(path=app.config['UPLOAD_FOLDER'] + "ADD_PHOTO/check/" + filename)
            if res['msg'] == 'SUCCESS':
                for n in range(res['num']):
                    local_db.enter(student_id=res['info'][n]['student_id'], path=str(app.config['UPLOAD_FOLDER'] + "ADD_PHOTO/" + filename),
                                   is_mask=res['info'][n]['is_mask'], position=pos, time=time)
                    return jsonify({"msg": "SUCCESS"})
        else:
            return jsonify({'msg': 'FILE ILLEGAL'})
    else:
        return render_template('check_add_photo.html')


@app.route('/check_result/', methods=['GET'])
def check_result():
    return render_template('check_result.html')


# homework
@app.route('/homework_add_photo/', methods=['GET', 'POST'])
def homework_add_photo():
    if request.method == 'POST':
        subject = request.form['subject']
        homework = request.form['homework']
        time = request.form['time']
        file = request.files['photo']
        homework = request.form['homework']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/ADD_PHOTO/homework/', filename))
            res = ocr.ocr(path=app.config['UPLOAD_FOLDER'] + "/ADD_PHOTO/homework/" + filename)
            res = json.loads(res)
            # 处理部分
            data = res['forms'][0]['body']
            people_num = 0  # 一共有多少人
            is_commit_row = 0
            name_row = 0  # 名字矩形的序号,这个要到第一个名字就加 1
            for i in data:
                if i['column'][0] == 1:
                    if people_num < i['row'][0]:
                        people_num = i['row'][0]
                else:
                    break
            people_num = people_num - 1
            for i, element in enumerate(data):
                if element['word'] == '姓名':
                    name_row = i  # name_row = 4
                    break

            for i, element in enumerate(data):
                if element['word'] in config.is_commit_word:
                    is_commit_row = i  # is_commit_row = 8
                    break

            for i in range(people_num):  # 因为这个range默认从0开始 所以要加 1
                if data[is_commit_row + i + 1]['word'] == '1':
                    is_commit = 1
                else:
                    is_commit = 0
                ldb_res = local_db.add_homework(name=data[name_row + i + 1]['word'],
                                                path=app.config['UPLOAD_FOLDER'] + "/ADD_PHOTO/homework/" + filename,
                                                subject=subject, homework=homework,
                                                is_commit=is_commit, time=time)
                if ldb_res['msg'] == 'FAIL':
                    return jsonify({'msg': 'Fail: unregister name!'})

            return jsonify({'msg': 'SUCCESS'})
        else:
            return jsonify({'msg': 'FILE ILLEGAL'})
    return render_template('homework_add_photo.html')


@app.route('/homework_result/', methods=['GET', 'POST'])
def homework_result():
    return render_template("homework_result.html")


# class
@app.route('/class_add_photo/', methods=['GET', 'POST'])
def class_add_photo():
    if request.method == 'POST':
        file = request.files['photo']
        name = request.form['name']
        lesson = request.form['lesson']
        reason = request.form['reason']
        time = request.form['time']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/ADD_PHOTO/', filename))
            local_db.class_add_photo(name=name, path=app.config['UPLOAD_FOLDER'] + "ADD_PHOTO/" + filename,
                                     lesson=lesson, time=time, annotation=reason)
            return jsonify({'msg': 'SUCCESS'})
        else:
            return jsonify({'msg': 'FILE ILLEGAL'})
    return render_template('class_add_photo.html')


@app.route('/class_result/', methods=['GET', 'POST'])
def class_result():
    return render_template('class_result.html')


# student
@app.route('/search/', methods=['GET', 'POST'])
def search():
    return render_template('search.html')


@app.errorhandler(404)
def page_unauthorized(error):
    return render_template('pages-404.html')


@app.route('/database/api_get_data/<path:need>', methods=['POST'])
def api_get_data(need):
    if need == 'face_view/':
        info = local_db.get_stu_info()
        num = local_db.count_person()
        return jsonify({'data': info, 'num': num})
