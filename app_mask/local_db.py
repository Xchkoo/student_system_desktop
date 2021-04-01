from flask import g
import sqlite3
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


def enter(STUDENT_ID, PATH, is_mask, POSITION, TIME):
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO SYSTEM (TYPE, STUDENT_ID, PATH, is_mask, POSITION, TIME) "
              + "VALUES ( 'MASK', '" + str(STUDENT_ID) + "','" + str(PATH) + "', " +
              str(is_mask) + ",'" + str(POSITION) + "','" + str(TIME) + "');")
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


# ---------------- 以下是统计模块 ---------------------- #
def mask_mask_num():
    mask_wp = mask_nwp = 0
    return {'mask_wearing_percent':  mask_wp, 'mask_not_wearing_percent': mask_nwp}


def get_stu_info():
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    stu_info = c.execute("SELECT * FORM NAME WHERE NAME IS NOT NULL")
    print(stu_info)
    return stu_info


def count_person():
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()
    num = c.execute('SELECT count(*) FROM TRANS')
    return num

# ---------------- end ------------------ #
if __name__ == '__main__':
    register_delete("5")