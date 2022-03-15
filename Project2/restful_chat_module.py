import json
import os
import base64
import time
import restful_device_module as dev
import pymongo
from flask import Flask, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

db = './ec530_p2.db'
chat_path = './chat.json'
media_history = './history/'

class init(Resource):
    def get(self):
        dev.init_dataset()
        return dev.init_data()

class chat(Resource):
    def get(self, end1, end2):
        return print_chat_history(end1, end2)
    def delete(self, end1, end2):
        return clean_chat_history(end1, end2)
    def post(self, end1, end2):
        return post_chat(end1, end2)

class select_media(Resource):
    def get(self, end1, end2, media_name):
        return read_media(end1, end2, media_name)

class media(Resource):
    def get(self, end1, end2):
        return print_media_history(end1, end2)
    def delete(self, end1, end2):
        return clean_media(end1, end2)

class medical(Resource):
    def get(self, end1, end2):
        return create_chat(end1, end2)

def exist_db_check(end1, end2):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    dblist = myclient.list_database_names()
    if f"chat_record_{end2}_{end1}" in dblist:
        return f"chat_record_{end2}_{end1}"
    else:
        return f"chat_record_{end1}_{end2}"

def create_chat(end1, end2):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db_name = exist_db_check(end1, end2)
    chat_record = myclient[db_name]
    medical_record = chat_record["medical_record"]
    x = medical_record.delete_many({})
    
    conn = dev.create_connection(db)
    cur = conn.cursor()
    cur.execute("SELECT * FROM device_assignment where Responsible_Person = ? AND Assign_to = ?", (end1, end2))
    rows = cur.fetchall()
    respp = dev.select_user(end1)
    assto = dev.select_user(end2)
    
    for row in rows:
        cur.execute("SELECT * FROM record where Assignment = ?", (row[0],))
        records = cur.fetchall()
        cur.execute("SELECT * FROM devices where D_ID = ?", (row[3],))
        device = cur.fetchall()
        for record in records:
            try:
                info = {"R_ID": record[0], "Responsible_Person": respp["First_Name"], "Assign_to": assto["First_Name"], "Device": device[0][2], "Record_time": record[2], "Value": record[3]}
                medical_record.insert_one(info)
            except Exception as e:
                print("Error")
    return print_medical_history(end1, end2)

def send_media(end1, end2, media_name):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db_name = exist_db_check(end1, end2)
    chat_record = myclient[db_name]
    media_record = chat_record["media_record"]
    chat_history = chat_record["chat_record"]
    date = time.strftime("%Y-%m-%d", time.localtime())
    now = time.strftime("%H:%M:%S", time.localtime())

    with open('./' + media_name, 'rb') as f:
        img_byte = base64.b64encode(f.read())
    f.close()
    img_str = img_byte.decode('ascii')

    media = {"Name": media_name, "Image": img_str}
    info = {"From": end1, "To": end2, "Date": date, "Time": now, "Message_Type": "Image", "Message": media_name}
    media_record.insert_one(media)
    chat_history.insert_one(info)
    return f"Media {media_name} uploaded successed"

def read_media(end1, end2, media_name):
    if not os.path.exists(media_history):
        os.mkdir(media_history)
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db_name = exist_db_check(end1, end2)
    chat_record = myclient[db_name]
    media_record = chat_record["media_record"]
    for media in media_record.find({"Name": media_name}):
        img_str = media["Image"].encode('ascii')
        img_byte = base64.b64decode(img_str)
        with open(media_history + media_name, 'wb') as f:
            f.write(img_byte)
        f.close()
        response = make_response(img_byte)
        response.headers['Content-Type'] = 'image/png'
        return response

def clean_media(end1, end2):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db_name = exist_db_check(end1, end2)
    chat_record = myclient[db_name]
    media_record = chat_record["media_record"]
    media_record.delete_many({})
    return print_media_history(end1, end2)

def print_media_history(end1, end2):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db_name = exist_db_check(end1, end2)
    chat_record = myclient[db_name]
    media_record = chat_record["media_record"]
    history = dict()
    num = 0
    for information in media_record.find({}, {"_id": 0}):
        num += 1
        history[f"media_record_{num}"] = information["Name"]
    return history
    
def post_chat(end1, end2):
    if not os.path.exists(chat_path):
        print("No chat information. It should be a json file.")
        return
    with open(chat_path,'r') as f:
        file = json.load(f)
    f.close()
    for key in file.keys():
        chat_record = file[key]
        if chat_record["Message_Type"] == "Text":
            insert_chat_record(chat_record["From"], chat_record["To"], chat_record["Message"])
        elif chat_record["Message_Type"] == "Image":
            send_media(chat_record["From"], chat_record["To"], chat_record["Message"])
        else:
            return "Only can handle text and images"
    return print_chat_history(end1, end2)

def insert_chat_record(end1, end2, text):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db_name = exist_db_check(end1, end2)
    chat_record = myclient[db_name]
    chat_history = chat_record["chat_record"]
    date = time.strftime("%Y-%m-%d", time.localtime())
    now = time.strftime("%H:%M:%S", time.localtime())
    info = {"From": end1, "To": end2, "Date": date, "Time": now, "Message_Type": "Text",  "Message": text}
    x = chat_history.insert_one(info)
    return print_chat_history(end1, end2)

def print_medical_history(end1, end2):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db_name = exist_db_check(end1, end2)
    chat_record = myclient[db_name]
    medical_record = chat_record["medical_record"]
    history = dict()
    num = 0
    for information in medical_record.find({}, {"_id": 0}):
        num += 1
        history[f"medical_record_{num}"] = information
    return history

def print_chat_history(end1, end2):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db_name = exist_db_check(end1, end2)
    chat_record = myclient[db_name]
    chat_history = chat_record["chat_record"]
    history = dict()
    num = 0
    for information in chat_history.find({}, {"_id": 0}):
        num += 1
        history[f"chat_record_{num}"] = information
    return history

def clean_chat_history(end1, end2):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db_name = exist_db_check(end1, end2)
    chat_record = myclient[db_name]
    chat_history = chat_record["chat_record"]
    chat_history.delete_many({})
    return print_chat_history(end1, end2)

api.add_resource(init, '/chats')
api.add_resource(chat, '/chats/<int:end1>_<int:end2>/chat')
api.add_resource(select_media, '/chats/<int:end1>_<int:end2>/media/<media_name>')
api.add_resource(media, '/chats/<int:end1>_<int:end2>/media')
api.add_resource(medical, '/chats/<int:end1>_<int:end2>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug = True)