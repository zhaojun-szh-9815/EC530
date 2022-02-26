import sqlite3

db_dir = './db_ec530_p2.db'

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
    rows = select_all_users(conn)
    new_user = (len(rows)+1, fn, ln, gender, role, phone, dob, h, w)
    sql = ''' INSERT INTO users (U_ID, First_Name, Last_Name, Gender, Role, Phone, Date_of_Birth, Height_in_cm, Weight_in_kg)
              VALUES(?,?,?,?,?,?,?,?,?) '''
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
    rows = select_all_devices(conn)
    new_device = (len(rows)+1, dor, dt)
    sql = ''' INSERT INTO devices (D_ID, Date_of_Registration, Data_type)
              VALUES(?,?,?) '''
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
    rows = select_all_assignments(conn)
    new_assignment = (len(rows)+1, rp, at, dev)
    sql = ''' INSERT INTO device_assignment (A_ID, Responsible_Person, Assign_to, Device)
              VALUES(?,?,?,?) '''
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
    rows = select_all_records(conn)
    new_record = (len(rows)+1, assignment, rectime, value)
    sql = ''' INSERT INTO record (R_ID, Assignment, Record_time, Value)
              VALUES(?,?,?,?) '''
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
