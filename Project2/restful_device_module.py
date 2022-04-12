import sqlite3
import os
import json
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
db = './ec530_p2.db'

class init(Resource):
    def get(self):
        init_dataset()
        return init_data()

class User_Password(Resource):
    def get(self, username):
        return select_user_password(username)

class User_get_del(Resource):
    def get(self, todo_id):
        return select_user(todo_id)
    def delete(self, todo_id):
        return delete_user(todo_id)

class User_related(Resource):
    def get(self, id):
        return select_related(id)

class User_edit_add(Resource):
    def get(self):
        return select_all_users()
    def put(self):
        json_request = json.loads(request.get_data(as_text = True))
        return update_user(json_request["U_ID"], json_request["Username"], json_request["Password"], json_request["Phone"], json_request["Height_in_cm"], json_request["Weight_in_kg"])
    def post(self):
        json_request = json.loads(request.get_data(as_text = True))
        return insert_user(json_request["Username"], json_request["Password"], json_request["First_Name"], json_request["Last_Name"], json_request["Gender"], json_request["Role"],
                        json_request["Phone"], json_request["Date_of_Birth"], json_request["Height_in_cm"], json_request["Weight_in_kg"])

class Device_get_del(Resource):
    def get(self, todo_id):
        return select_device(todo_id)
    def delete(self, todo_id):
        return delete_device(todo_id)

class Device_edit_add(Resource):
    def get(self):
        return select_all_devices()
    def put(self):
        device = json.loads(request.get_data(as_text = True))
        return update_device(device["D_ID"], device["Date_of_Registration"], device["Data_type"])
    def post(self):
        device = json.loads(request.get_data(as_text = True))
        return insert_device(device["Date_of_Registration"], device["Data_type"])

class Assignment_get_del(Resource):
    def get(self, todo_id):
        return select_assignment(todo_id)
    def delete(self, todo_id):
        return delete_assignment(todo_id)

class Assignment_edit_add(Resource):
    def get(self):
        return select_all_assignments()
    def put(self):
        assignment = json.loads(request.get_data(as_text = True))
        return update_assignment(assignment["A_ID"], assignment["Responsible_Person"], assignment["Assign_to"], assignment["Device"])
    def post(self):
        assignment = json.loads(request.get_data(as_text = True))
        return insert_assignment(assignment["Responsible_Person"], assignment["Assign_to"], assignment["Device"])

class Record_get_del(Resource):
    def get(self, todo_id):
        return select_record(todo_id)
    def delete(self, todo_id):
        return delete_record(todo_id)

class Record_edit_add(Resource):
    def get(self):
        return select_all_records()
    def put(self):
        record = json.loads(request.get_data(as_text = True))
        return update_record(record["R_ID"], record["Assignment"], record["Record_time"], record["Value"])
    def post(self):
        record = json.loads(request.get_data(as_text = True))
        return insert_record(record["Assignment"], record["Record_time"], record["Value"])


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def sqlite_custom_function(id):
    conn = create_connection(db)
    #conn.create_function("check_role", 1, sqlite_custom_function)
    cur = conn.cursor()
    cur.execute("SELECT Role FROM users where U_ID = ?", (id,))
    rows = cur.fetchall()
    role = rows[0]
    return role[0]

def create_table(sql):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    try:
        c = conn.cursor()
        c.execute(sql)
    except Exception as e:
        print(e)
    conn.close()

def init_dataset():
    if os.path.exists(db):
        os.remove(db)

    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    sqlite3.enable_callback_tracebacks(True)

    sql_create_users = '''CREATE TABLE users (U_ID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT NOT NULL, Password TEXT NOT NULL, First_Name TEXT NOT NULL, Last_Name TEXT NOT NULL, Gender TEXT CHECK (Gender IN ('Male', 'Female')) DEFAULT ('Male') NOT NULL, Role TEXT CHECK (Role IN ('Doctor', 'Nurse', 'Patient', 'Family', 'Developer')) NOT NULL DEFAULT ('Patient'), Phone TEXT CHECK (LENGTH(Phone) = 10) DEFAULT (0), Date_of_Birth DATETIME NOT NULL, Height_in_cm INT NOT NULL, Weight_in_kg INT NOT NULL);'''

    sql_create_devices = '''CREATE TABLE devices (D_ID INTEGER PRIMARY KEY AUTOINCREMENT, Date_of_Registration DATETIME NOT NULL, Data_type TEXT NOT NULL CHECK (Data_type IN ('Temperature', 'Blood_Pressure', 'Pluse', 'Blood_Oxygen', 'Blood_Glucose')));'''

    sql_create_assignments = '''CREATE TABLE device_assignment (A_ID INTEGER PRIMARY KEY AUTOINCREMENT, Responsible_Person INT REFERENCES users (U_ID) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL CHECK (check_role(Responsible_Person) = 'Doctor' or check_role(Responsible_Person) = 'Nurse'), Assign_to INT REFERENCES users (U_ID) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL CHECK (check_role(Assign_to) = 'Patient'), Device INT REFERENCES devices (D_ID) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL);'''

    sql_create_records = '''CREATE TABLE record (R_ID INTEGER PRIMARY KEY AUTOINCREMENT, Assignment INT REFERENCES device_assignment (A_ID) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL, Record_time DATETIME NOT NULL, Value DOUBLE NOT NULL);'''

    if conn is not None:
        create_table(sql_create_users)
        create_table(sql_create_devices)
        create_table(sql_create_assignments)
        create_table(sql_create_records)
    else:
        print("Error! cannot create the database connection.")
    conn.close()
    return "dataset init successed!"

def init_data():
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    sqlite3.enable_callback_tracebacks(True)

    insert_user('zhaojun', '11111', 'ZH', 'S', 'Male', 'Developer', '0123456789', '1998-01-05', 175, 80)
    insert_user('aa', '222', 'AA', 'A', 'Female', 'Doctor', '1234567890', '1997-04-02', 170, 50)
    insert_user('bb', '333', 'BB', 'B', 'Female', 'Nurse', '0000011111', '1999-02-18', 168, 48)
    insert_user('ccc', '4444', 'CC', 'C', 'Male', 'Patient', '1111100000', '2000-11-06', 180, 78)

    insert_device('2019-01-01', 'Temperature')
    insert_device('2019-01-02', 'Blood_Pressure')
    insert_device('2019-01-03', 'Pluse')
    insert_device('2019-02-02', 'Blood_Oxygen')
    insert_device('2019-02-04', 'Blood_Glucose')

    insert_assignment(2, 4, 1)
    insert_assignment(3, 4, 2)

    insert_record(1, '2022-2-10', 37.5)
    insert_record(2, '2022-2-12', 130.0)
    insert_record(1, '2022-2-14', 37.6)

    conn.close()
    return "data init successed!"

def select_all_users():
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    conn.close()
    ans = dict()
    num = 1
    for row in rows:
        row_ans = dict()
        row_ans["U_ID"] = row[0]
        row_ans["Username"] = row[1]
        row_ans["First_Name"] = row[3]
        row_ans["Last_Name"] = row[4]
        row_ans["Gender"] = row[5]
        row_ans["Role"] = row[6]
        row_ans["Phone"] = row[7]
        row_ans["Date_of_Birth"] = row[8]
        row_ans["Height_in_cm"] = row[9]
        row_ans["Weight_in_kg"] = row[10]
        ans[f"user{num}"] = row_ans
        num += 1
    return ans

def select_user(id):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users where U_ID = ?", (id,))
    rows = cur.fetchall()
    try:
        row = rows[0]
    except Exception as e:
        print(f"No user with U_ID = {id}")
        return None
    ans = dict()
    ans["U_ID"] = row[0]
    ans["Username"] = row[1]
    ans["First_Name"] = row[3]
    ans["Last_Name"] = row[4]
    ans["Gender"] = row[5]
    ans["Role"] = row[6]
    ans["Phone"] = row[7]
    ans["Date_of_Birth"] = row[8]
    ans["Height_in_cm"] = row[9]
    ans["Weight_in_kg"] = row[10]
    return ans

def select_related(id):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    cur = conn.cursor()
    cur.execute("SELECT * FROM device_assignment where Responsible_Person = ? or Assign_to = ?", (id, id,))
    rows = cur.fetchall()
    try:
        r = rows[0]
    except Exception as e:
        print(f"No related user given U_ID = {id}")
        print(rows)
        return None
    resp = dict()
    ans = dict()
    if r[1] == id:
        resp["Title"] = "Your Patients"
        i = 1
        for row in rows:
            ans[f"{i}"] = select_user(row[2])["First_Name"]
        resp["Content"] = ans
    if r[2] == id:
        resp["Title"] = "Your Doctor/Nurse"
        i = 1
        for row in rows:
            ans[f"{i}"] = select_user(row[1])["First_Name"]
        resp["Content"] = ans
    return resp

def select_user_password(username):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    cur = conn.cursor()
    cur.execute("SELECT Password FROM users where Username = ?", (username,))
    rows = cur.fetchall()
    try:
        row = rows[0]
    except Exception as e:
        print(f"No user with Username = {username}")
        return None
    ans = dict()
    ans["Password"] = row[0]
    return ans

def insert_user(un, pw, fn, ln, gender, role, phone, dob, h, w):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    new_user = (un, pw, fn, ln, gender, role, phone, dob, h, w)
    sql = ''' INSERT INTO users (Username, Password, First_Name, Last_Name, Gender, Role, Phone, Date_of_Birth, Height_in_cm, Weight_in_kg)
                VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, new_user)
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()
    return cur.lastrowid

def delete_user(id):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    sql = 'DELETE FROM users WHERE U_ID=?'
    cur = conn.cursor()
    try:
        cur.execute(sql, (id,))
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()
    return select_all_users()

def update_user(un, pw, id, phone, h, w):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    update_info = (un, pw, phone, h, w, id)
    sql = ''' UPDATE users
                SET Username = ? ,
                    Password = ? ,
                    Phone = ? ,
                    Height_in_cm = ? ,
                    Weight_in_kg = ?
                WHERE U_ID = ?'''
    cur = conn.cursor()
    try:
        cur.execute(sql, update_info)
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()
    return select_user(id)

def select_all_devices():
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    cur = conn.cursor()
    cur.execute("SELECT * FROM devices")
    rows = cur.fetchall()
    conn.close()
    ans = dict()
    num = 1
    for row in rows:
        row_ans = dict()
        row_ans["D_ID"] = row[0]
        row_ans["Date_of_Registration"] = row[1]
        row_ans["Data_Type"] = row[2]
        ans[f"device{num}"] = row_ans
        num += 1
    return ans

def select_device(id):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    cur = conn.cursor()
    cur.execute("SELECT * FROM devices where D_ID = ?", (id,))
    rows = cur.fetchall()
    conn.close()
    try:
        row = rows[0]
    except Exception as e:
        print(f"No device with D_ID = {id}")
        return None
    ans = dict()
    ans["D_ID"] = row[0]
    ans["Date_of_Registration"] = row[1]
    ans["Data_Type"] = row[2]
    return ans

def insert_device(dor, dt):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    new_device = (dor, dt)
    sql = ''' INSERT INTO devices (Date_of_Registration, Data_type)
              VALUES(?,?) '''
    cur = conn.cursor()

    try:
        cur.execute(sql, new_device)
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()
    return cur.lastrowid

def delete_device(id):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    sql = 'DELETE FROM devices WHERE D_ID=?'
    cur = conn.cursor()
    try:
        cur.execute(sql, (id,))
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()
    return select_all_devices()

def update_device(id, dor, dt):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    update_info = (dor, dt, id)
    sql = ''' UPDATE devices
              SET Date_of_Registration = ? ,
                  Data_type = ?
              WHERE D_ID = ?'''
    cur = conn.cursor()
    try:
        cur.execute(sql, update_info)
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()
    return select_device(id)
    
def select_all_assignments():
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    cur = conn.cursor()
    cur.execute("SELECT * FROM device_assignment")
    rows = cur.fetchall()
    conn.close()
    ans = dict()
    num = 1
    for row in rows:
        row_ans = dict()
        row_ans["A_ID"] = row[0]
        row_ans["Responsible_Person"] = row[1]
        row_ans["Assign_to"] = row[2]
        row_ans["Device"] = row[3]
        ans[f"assignment{num}"] = row_ans
        num += 1
    return ans

def select_assignment(id):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    cur = conn.cursor()
    cur.execute("SELECT * FROM device_assignment where A_ID = ?", (id,))
    rows = cur.fetchall()
    conn.close()
    try:
        row = rows[0]
    except Exception as e:
        print(f"No device_assignment with A_ID = {id}")
        return None
    ans = dict()
    ans["A_ID"] = row[0]
    ans["Responsible_Person"] = row[1]
    ans["Assign_to"] = row[2]
    ans["Device"] = row[3]
    return ans

def insert_assignment(rp, at, dev):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    new_assignment = (rp, at, dev)
    sql = ''' INSERT INTO device_assignment (Responsible_Person, Assign_to, Device)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, new_assignment)
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()
    return cur.lastrowid

def delete_assignment(id):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    sql = 'DELETE FROM device_assignment WHERE A_ID=?'
    cur = conn.cursor()
    try:
        cur.execute(sql, (id,))
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()
    return select_all_assignments()

def update_assignment(id, rp, at, dev):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    update_info = (rp, at, dev, id)
    sql = ''' UPDATE device_assignment
              SET Responsible_Person = ? ,
                  Assign_to = ?,
                  Device = ?
              WHERE A_ID = ?'''
    cur = conn.cursor()
    try:
        cur.execute(sql, update_info)
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()
    return select_assignment(id)

def select_all_records():
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    cur = conn.cursor()
    cur.execute("SELECT * FROM record")
    rows = cur.fetchall()
    conn.close()
    ans = dict()
    num = 1
    for row in rows:
        row_ans = dict()
        row_ans["R_ID"] = row[0]
        row_ans["A_ID"] = row[1]
        row_ans["Record_Time"] = row[2]
        row_ans["Value"] = row[3]
        ans[f"record{num}"] = row_ans
        num += 1
    return ans

def select_record(id):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    cur = conn.cursor()
    cur.execute("SELECT * FROM record where R_ID = ?", (id,))
    rows = cur.fetchall()
    conn.close()
    try:
        row = rows[0]
    except Exception as e:
        print(f"No record with R_ID = {id}")
        return None
    ans = dict()
    ans["R_ID"] = row[0]
    ans["A_ID"] = row[1]
    ans["Record_Time"] = row[2]
    ans["Value"] = row[3]
    return ans

def insert_record(assignment, rectime, value):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    new_record = (assignment, rectime, value)
    sql = ''' INSERT INTO record (Assignment, Record_time, Value)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, new_record)
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()
    return cur.lastrowid

def delete_record(id):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    sql = 'DELETE FROM record WHERE R_ID=?'
    cur = conn.cursor()
    try:
        cur.execute(sql, (id,))
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()
    return select_all_records()

def update_record(id, assignment, rectime, value):
    conn = create_connection(db)
    conn.create_function("check_role", 1, sqlite_custom_function)
    update_info = (assignment, rectime, value, id)
    sql = ''' UPDATE record
              SET Assignment = ? ,
                  Record_time = ?,
                  Value = ?
              WHERE R_ID = ?'''
    cur = conn.cursor()
    try:
        cur.execute(sql, update_info)
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()
    return select_record(id)

api.add_resource(init, '/')
api.add_resource(User_Password, '/user_password/<username>')
api.add_resource(User_get_del, '/users/<int:todo_id>')
api.add_resource(User_related, '/users/related/<int:id>')
api.add_resource(User_edit_add, '/users')
api.add_resource(Device_get_del, '/devices/<int:todo_id>')
api.add_resource(Device_edit_add, '/devices')
api.add_resource(Assignment_get_del, '/assignments/<int:todo_id>')
api.add_resource(Assignment_edit_add, '/assignments')
api.add_resource(Record_get_del, '/records/<int:todo_id>')
api.add_resource(Record_edit_add, '/records')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug = True)
