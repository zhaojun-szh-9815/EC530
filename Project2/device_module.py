import sqlite3
import os

db_dir = './ec530_p2.db'

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    # print('connect success')
    return conn

def print_rows(rows):
    for row in rows:
        print(row)

def sqlite_custom_function(id):
    conn = create_connection(db_dir)
    user = select_user(conn, id)
    conn.close()
    return user[4]

def create_table(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Exception as e:
        print(e)

def init_dataset():
    if os.path.exists(db_dir):
        os.remove(db_dir)
        
    conn = create_connection(db_dir)
    conn.create_function("check_role", 1, sqlite_custom_function)

    sql_create_users = '''CREATE TABLE users (U_ID INTEGER PRIMARY KEY AUTOINCREMENT, First_Name TEXT NOT NULL, Last_Name TEXT NOT NULL, Gender TEXT CHECK (Gender IN ('Male', 'Female')) DEFAULT ('Male') NOT NULL, Role TEXT CHECK (Role IN ('Doctor', 'Nurse', 'Patient', 'Family', 'Developer')) NOT NULL DEFAULT ('Patient'), Phone TEXT CHECK (LENGTH(Phone) = 10) DEFAULT (0), Date_of_Birth DATETIME NOT NULL, Height_in_cm INT NOT NULL, Weight_in_kg INT NOT NULL);'''

    sql_create_devices = '''CREATE TABLE devices (D_ID INTEGER PRIMARY KEY AUTOINCREMENT, Date_of_Registration DATETIME NOT NULL, Data_type TEXT NOT NULL CHECK (Data_type IN ('Temperature', 'Blood_Pressure', 'Pluse', 'Blood_Oxygen', 'Blood_Glucose')));'''

    sql_create_assignments = '''CREATE TABLE device_assignment (A_ID INTEGER PRIMARY KEY AUTOINCREMENT, Responsible_Person INT REFERENCES users (U_ID) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL CHECK (check_role(Responsible_Person) = 'Doctor' or check_role(Responsible_Person) = 'Nurse'), Assign_to INT REFERENCES users (U_ID) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL CHECK (check_role(Assign_to) = 'Patient'), Device INT REFERENCES devices (D_ID) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL);'''

    sql_create_records = '''CREATE TABLE record (R_ID INTEGER PRIMARY KEY AUTOINCREMENT, Assignment INT REFERENCES device_assignment (A_ID) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL, Record_time DATETIME NOT NULL, Value DOUBLE NOT NULL);'''

    if conn is not None:
        create_table(conn, sql_create_users)
        create_table(conn, sql_create_devices)
        create_table(conn, sql_create_assignments)
        create_table(conn, sql_create_records)
    else:
        print("Error! cannot create the database connection.")

    insert_user(conn, 'ZH', 'S', 'Male', 'Developer', '0123456789', '1998-01-05', 175, 80)
    insert_user(conn, 'AA', 'A', 'Female', 'Doctor', '1234567890', '1997-04-02', 170, 50)
    insert_user(conn, 'BB', 'B', 'Female', 'Nurse', '0000011111', '1999-02-18', 168, 48)
    insert_user(conn, 'CC', 'C', 'Male', 'Patient', '1111100000', '2000-11-06', 180, 78)

    insert_device(conn, '2019-01-01', 'Temperature')
    insert_device(conn, '2019-01-02', 'Blood_Pressure')
    insert_device(conn, '2019-01-03', 'Pluse')
    insert_device(conn, '2019-02-02', 'Blood_Oxygen')
    insert_device(conn, '2019-02-04', 'Blood_Glucose')

    insert_assignment(conn, 2, 4, 1)
    insert_assignment(conn, 3, 4, 2)

    insert_record(conn, 1, '2022-2-10', 37.5)
    insert_record(conn, 2, '2022-2-12', 130.0)
    insert_record(conn, 1, '2022-2-14', 37.6)

    conn.close()
    print("init successed!")

def select_all_users(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    return rows

def select_user(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users where U_ID = ?", (id,))
    rows = cur.fetchall()
    try:
        return rows[0]
    except Exception as e:
        print(f"No user with U_ID = {id}")
        return None

def insert_user(conn, fn, ln, gender, role, phone, dob, h, w):
    new_user = (fn, ln, gender, role, phone, dob, h, w)
    sql = ''' INSERT INTO users (First_Name, Last_Name, Gender, Role, Phone, Date_of_Birth, Height_in_cm, Weight_in_kg)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, new_user)
        conn.commit()
    except Exception as e:
        print(e)
    return cur.lastrowid

def delete_user(conn, id):
    sql = 'DELETE FROM users WHERE U_ID=?'
    cur = conn.cursor()
    try:
        cur.execute(sql, (id,))
        conn.commit()
    except Exception as e:
        print(e)
    return cur.lastrowid

def update_user(conn, id, phone, h, w):
    update_info = (phone, h, w, id)
    sql = ''' UPDATE users
              SET Phone = ? ,
                  Height_in_cm = ? ,
                  Weight_in_kg = ?
              WHERE U_ID = ?'''
    cur = conn.cursor()
    try:
        cur.execute(sql, update_info)
        conn.commit()
    except Exception as e:
        print(e)
    user = select_user(conn, id)
    print(user)
    return user

def select_all_devices(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM devices")
    rows = cur.fetchall()
    return rows

def select_device(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM devices where D_ID = ?", (id,))
    rows = cur.fetchall()
    try:
        return rows[0]
    except Exception as e:
        print(f"No device with D_ID = {id}")
        return None

def insert_device(conn, dor, dt):
    new_device = (dor, dt)
    sql = ''' INSERT INTO devices (Date_of_Registration, Data_type)
              VALUES(?,?) '''
    cur = conn.cursor()

    try:
        cur.execute(sql, new_device)
        conn.commit()
    except Exception as e:
        print(e)

    return cur.lastrowid

def delete_device(conn, id):
    sql = 'DELETE FROM devices WHERE D_ID=?'
    cur = conn.cursor()
    try:
        cur.execute(sql, (id,))
        conn.commit()
    except Exception as e:
        print(e)
    return cur.lastrowid

def update_device(conn, id, dor, dt):
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
    device = select_device(conn, id)
    print(device)

def select_all_assignments(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM device_assignment")
    rows = cur.fetchall()
    return rows

def select_assignment(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM device_assignment where A_ID = ?", (id,))
    rows = cur.fetchall()
    try:
        return rows[0]
    except Exception as e:
        print(f"No device_assignment with A_ID = {id}")
        return None

def insert_assignment(conn, rp, at, dev):
    new_assignment = (rp, at, dev)
    sql = ''' INSERT INTO device_assignment (Responsible_Person, Assign_to, Device)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, new_assignment)
        conn.commit()
    except Exception as e:
        print(e)

    return cur.lastrowid

def delete_assignment(conn, id):
    sql = 'DELETE FROM device_assignment WHERE A_ID=?'
    cur = conn.cursor()
    try:
        cur.execute(sql, (id,))
        conn.commit()
    except Exception as e:
        print(e)
    return cur.lastrowid

def update_assignment(conn, id, rp, at, dev):
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
    assignment = select_assignment(conn, id)
    print(assignment)

def select_all_records(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM record")
    rows = cur.fetchall()
    return rows

def select_record(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM record where R_ID = ?", (id,))
    rows = cur.fetchall()
    try:
        return rows[0]
    except Exception as e:
        print(f"No record with R_ID = {id}")
        return None

def insert_record(conn, assignment, rectime, value):
    new_record = (assignment, rectime, value)
    sql = ''' INSERT INTO record (Assignment, Record_time, Value)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, new_record)
        conn.commit()
    except Exception as e:
        print(e)

    return cur.lastrowid

def delete_record(conn, id):
    sql = 'DELETE FROM record WHERE R_ID=?'
    cur = conn.cursor()
    try:
        cur.execute(sql, (id,))
        conn.commit()
    except Exception as e:
        print(e)
    return cur.lastrowid

def update_record(conn, id, assignment, rectime, value):
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
    record = select_record(conn, id)
    print(record)


if __name__ == '__main__':
    init_dataset()
    
    conn = create_connection(db_dir)
    conn.create_function("check_role", 1, sqlite_custom_function)

    rows = select_all_users(conn)
    print_rows(rows)
    '''
    last_id = insert_user(conn, 'DD', 'D', 'Male', 'Patient', '3333333333', '2022-02-18', 180, 78)
    last_id = insert_user(conn, 'DD', 'D', 'Male', 'Patient', '3333333333', '2022-02-18', 180, 78)
    last_id = delete_user(conn, 6)
    rows = select_all_users(conn)
    print_rows(rows)
    update_user(conn, 5, "3334443333", 180, 78)
    last_id = delete_user(conn, 5)
    print_rows(rows)
    '''

    rows = select_all_devices(conn)
    print_rows(rows)
    '''
    insert_device(conn, '2022-02-20','Temperature')
    insert_device(conn, '2022-02-21','Pressure')
    insert_device(conn, '2022-02-21','Blood_Pressure')
    delete_device(conn, 7)
    rows = select_all_devices(conn)
    print_rows(rows)
    update_device(conn, 6, '2022-02-20', 'Pluse')
    select_device(conn, 7)
    delete_device(conn, 6)
    rows = select_all_devices(conn)
    print_rows(rows)
    '''
    
    rows = select_all_assignments(conn)
    print_rows(rows)
    '''
    last_id = insert_assignment(conn, 2, 4, 5)
    last_id = insert_assignment(conn, 1, 4, 5)
    last_id = insert_assignment(conn, 3, 4, 5)
    rows = select_all_assignments(conn)
    print_rows(rows)
    last_id = delete_assignment(conn, 4)
    update_assignment(conn, 3, 3, 4, 3)
    rows = select_all_assignments(conn)
    print_rows(rows)
    delete_assignment(conn, 3)
    rows = select_all_assignments(conn)
    print_rows(rows)
    '''

    rows = select_all_records(conn)
    print_rows(rows)
    '''
    last_id = insert_record(conn, 2, '2022-02-19', 140)
    last_id = insert_record(conn, 1, '2022-02-20', 36.5)
    rows = select_all_records(conn)
    print_rows(rows)
    last_id = delete_record(conn, 5)
    update_record(conn, 4, 1, '2022-02-19', 36.9)
    rows = select_all_records(conn)
    print_rows(rows)
    delete_record(conn, 4)
    rows = select_all_records(conn)
    print_rows(rows)
    '''

    conn.close()
