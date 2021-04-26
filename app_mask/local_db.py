from flask import g
import sqlite3
from app_mask import config


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(config.DATABASE)
    return db


def class_add_photo(name, path, lesson, time, annotation):
    t_id = name_to_trans_id(name)
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO SYSTEM (TYPE,STUDENT_ID,PATH,LESSON,annotation,TIME)"
              + "VALUES ('CLASS','" + str(t_id) + "','" + str(path) + "','" + str(lesson)
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
    c.execute("INSERT INTO TRANS (trans_id, NAME, PATH) VALUES (NULL, '" + name + "', '" + path + "')")
    sc = c.execute("SELECT * from TRANS")
    return_data = 0
    for row in sc:
        if row[1] == name:
            return_data = row[0]
    conn.commit()
    conn.close()
    return str(return_data)


def add_homework(name, path, subject, homework, is_commit, time):
    t_id = name_to_trans_id(name)
    if t_id == -1:
        return {'msg': 'FAIL'}
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO SYSTEM (TYPE,STUDENT_ID,PATH,LESSON,HOMEWORK,is_commit,TIME) VALUES ('HOMEWORK','"
              + str(t_id) + "','"
              + str(path) + "','"
              + str(subject) + "','"
              + str(homework) + "','"
              + str(is_commit) + "','"
              + str(time) + "');")
    conn.commit()
    conn.close()
    return {'msg': 'SUCCESS'}


# ---------------- 以下是统计模块 ---------------------- #


def get_class():
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    res = []
    sc = c.execute("SELECT ID,TYPE,STUDENT_ID,PATH,TIME,LESSON,annotation FROM SYSTEM WHERE TYPE IS 'CLASS'")
    for col in sc:
        pre_data = {"name": trans_id_to_name(int(col[2])), "img": col[3], "time": col[4], "lesson": col[5], "reason": col[6]}
        res.append(pre_data)
    return res


def get_class_num():
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    sc = c.execute("SELECT count(*) FROM SYSTEM WHERE TYPE IS 'CLASS'")
    return sc.fetchone()[0]


def get_homework_data(subject):
    sequence = get_homework_sequence(subject)
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    res = []
    for i in sequence:
        sc = c.execute("SELECT ID, TYPE, STUDENT_ID, PATH, TIME, HOMEWORK, is_commit FROM SYSTEM WHERE TYPE IS 'HOMEWORK' AND LESSON IS '" + subject + "' AND HOMEWORK IS '" + i + "'")
        check = 0
        data = dict(homework_name="", homework_img="", hand_in_num=0, hand_in_name=[], un_hand_in_num=0,
                    un_hand_in_name=[])
        for col in sc:
            if check == 0:
                data["homework_name"] = col[5]
                data["homework_img"] = col[3]
                data["homework_time"] = col[4]
                check = 1
            name = trans_id_to_name(int(col[2]))
            if col[6] == 1:
                data["hand_in_name"].append(name)
                data["hand_in_num"] = data["hand_in_num"] + 1
            if col[6] == 0:
                data["un_hand_in_name"].append(name)
                data["un_hand_in_num"] = data["un_hand_in_num"] + 1
        res.append(data)
    conn.close()
    return res


def get_homework_num(subject):
    s = get_homework_sequence(subject)
    return len(s)


def get_homework_sequence(subject):
    res = []
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    sc = c.execute("SELECT ID, TYPE, STUDENT_ID, PATH, TIME, HOMEWORK, is_commit FROM SYSTEM WHERE TYPE IS 'HOMEWORK' AND LESSON IS '"
                   + subject + "'")
    for i in sc:
        if i[5] not in res and i[5] != '':
            res.append(i[5])
    conn.close()
    return res


def sum_mask():
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    uwc = c.execute("SELECT count(*) FROM SYSTEM WHERE TYPE IS 'MASK' AND is_mask IS 0")
    data_wear = uwc.fetchone()[0]
    wc = c.execute("SELECT count(*) FROM SYSTEM WHERE TYPE IS 'MASK' AND is_mask IS 1")
    data_unwear = wc.fetchone()[0]
    res = {'wear': data_wear, 'unwear': data_unwear, 'all': data_wear + data_unwear}
    return res


def get_date():
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    sc = c.execute("SELECT TIME FROM SYSTEM WHERE TIME IS NOT NULL AND TYPE IS 'MASK'")
    sequence = []
    for col in sc:
        if col[0] not in sequence and col[0] != '':
            sequence.append(col[0])
    return sequence


def count_mask():
    res = []
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    sc = c.execute("SELECT TIME FROM SYSTEM WHERE TIME IS NOT NULL AND TYPE IS 'MASK'")
    sequence = []
    for col in sc:
        if col[0] not in sequence:
            sequence.append(col[0])

    for i, date in enumerate(sequence):
        if date == '':
            continue
        uwc = c.execute("SELECT count(*) FROM SYSTEM WHERE TIME IS NOT NULL AND TYPE IS 'MASK' AND is_mask IS 0 AND "
                        "TIME IS '" + date + "'")
        data_wear = uwc.fetchone()[0]
        wc = c.execute("SELECT count(*) FROM SYSTEM WHERE TIME IS NOT NULL AND TYPE IS 'MASK' AND is_mask IS 1 AND "
                       "TIME IS '" + date + "'")
        data_unwear = wc.fetchone()[0]
        res.append({'date': date, 'wear': data_wear, 'unwear': data_unwear, 'all': data_wear + data_unwear})
    return res


def count_pass(date):
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    sc = c.execute("SELECT * FROM SYSTEM WHERE TYPE IS 'MASK' AND POSITION IS NOT NULL AND TIME IS '" + date + "'")
    res = {"clnum": 0, "rnum": 0, "snum": 0, "cnum": 0}
    for i in sc:
        if i[4] == "校园门口":
            res['snum'] = res['snum'] + 1
        elif i[4] == "食堂门口":
            res['rnum'] = res['rnum'] + 1
        elif i[4] == "机房门口":
            res['cnum'] = res['cnum'] + 1
        elif i[4] == "教室门口":
            res['clnum'] = res['clnum'] + 1
    c.close()
    return res


def count_commuting():
    return count_mask()


def get_students_info():
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    transform = []
    all_stu_info = c.execute("SELECT * FROM TRANS WHERE NAME IS NOT NULL")
    for i, stu in enumerate(all_stu_info):
        transform.append({"name": stu[1], "path": stu[2]})
    conn.close()
    return transform


def count_person():
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    sc = c.execute('SELECT count(*) FROM TRANS')
    num = sc.fetchone()[0]
    conn.close()
    return num


# ---------------- 以下是通用模块 ------------------ #


def delete_trans(trans_id):
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM TRANS WHERE trans_id = " + str(trans_id))
    conn.commit()
    conn.close()


def path_search_by_id(trans_id):
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    sc = c.execute("SELECT PATH FROM TRANS WHERE trans_id IS " + str(trans_id))
    conn.close()
    return sc.fetchone()[0]


def trans_id_to_name(trans_id):
    """
    TIPS: trans_id must be int
    """
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    sc = c.execute("SELECT * FROM TRANS WHERE NAME IS NOT NULL")
    for row in sc:
        if row[0] == trans_id:
            return row[1]
    conn.close()
    return 'NaN'


def name_to_trans_id(name):
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    sc = c.execute('SELECT * FROM TRANS WHERE NAME IS NOT NULL')
    for row in sc:
        if row[1] == name:
            conn.close()
            return row[0]
    conn.close()
    return -1


def homework_update(name, homework, subject):
    tid = name_to_trans_id(name)
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    sc = c.execute("SELECT ID,HOMEWORK,STUDENT_ID FROM SYSTEM WHERE TYPE = 'HOMEWORK' AND LESSON IS '"+str(subject)+"' AND HOMEWORK IS '"+str(homework)+"'AND STUDENT_ID IS '"+str(tid)+"' AND is_commit IS 0")
    for col in sc:
        c.execute("UPDATE SYSTEM SET is_commit = 1 WHERE ID IS "+str(col[0]))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    print(homework_update('张威', '第三周的纠错','政治'))
