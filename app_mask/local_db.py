from flask import g
import sqlite3
import json
from app_mask import app, config


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(config.DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def class_add_photo(name, path, lesson, time, annotation):
    t_id = name_to_trans_id(name)
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO SYSTEM (TYPE,STUDENT_ID,PATH,LESSON,annotation,TIME)"
              + "VALUES ('CLASS','"+str(t_id) + "','" + str(path) + "','" + str(lesson)
              + "','" + str(annotation) + "','" + str(time) + "');")
    conn.commit()
    conn.close()


def enter(student_id, path, is_mask, position, time):
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO SYSTEM (TYPE, STUDENT_ID, PATH, is_mask, POSITION, TIME) "
              + "VALUES ( 'MASK', '" + str(student_id) + "','" + str(path) + "', " +
              str(is_mask) + ",'" + str(position) + "','" + str(time) + "');")
    conn.commit()
    conn.close()


def register_trans(name, path):
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO TRANS (trans_id, NAME, PATH) VALUES (NULL, '"+name+"', '"+path+"')")
    sc = c.execute("SELECT * from TRANS")
    for row in sc:
        if row[1] == name:
            return_data = row[0]
    conn.commit()
    conn.close()
    return str(return_data)


def register_delete(trans_id):
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM TRANS WHERE trans_id = "+str(trans_id))
    conn.commit()
    conn.close()


def add_homework(name, path, subject, homework, is_commit, time):
    t_id = name_to_trans_id(name)
    if t_id == -1:
        return {'msg': 'FAIL'}
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO SYSTEM (TYPE,STUDENT_ID,PATH,LESSON,HOMEWORK,is_commit,TIME) VALUES ('HOMEWORK','"
              + str(t_id)+"','"
              + str(path)+"','"
              + str(subject) + "','"
              + str(homework)+"','"
              + str(is_commit) + "','"
              + str(time) + "');")
    conn.commit()
    conn.close()
    return {'msg': 'SUCCESS'}
# ---------------- 以下是统计模块 ---------------------- #
# def mask_num():
#     mask_wp = mask_nwp = 0
#     return {'mask_wearing_percent':  mask_wp, 'mask_not_wearing_percent': mask_nwp}


# def get_stu_info():
#     conn = sqlite3.connect(config.DATABASE)
#     c = conn.cursor()
#     stu_info = c.execute("SELECT * FROM NAME WHERE NAME IS NOT NULL")
#     return stu_info
#
#
# def count_person():
#     conn = sqlite3.connect(config.DATABASE)
#     c = conn.cursor()
#     num = c.execute('SELECT count(*) FROM TRANS')
#     return num

# ---------------- 以下是查询模块 ------------------ #

def trans_id_to_name(trans_id):
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    sc = c.execute('SELECT * FROM TRANS WHERE NAME IS NOT NULL')
    for row in sc:
        if row[0] == trans_id:
            return row[1]
    return 'NaN'


def name_to_trans_id(name):
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    sc = c.execute('SELECT * FROM TRANS WHERE NAME IS NOT NULL')
    for row in sc:
        if row[1] == name:
            return row[0]
    return -1


if __name__ == '__main__':
    register_delete("5")