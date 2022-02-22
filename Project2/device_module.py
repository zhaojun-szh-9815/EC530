import json
import os
import datetime

data_dir = "./"

def make_json_input():
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    user_dictlist = [dict({"u_id": 1, "full_name": "ZH", "role": "Developer", "gender": "male", "created_at": "2022-02-18", "phone": "1234567890"}),
                         dict({"u_id": 2, "full_name": "AAA", "role": "Doctor", "gender": "male", "created_at": "2022-02-18", "phone": "0123456789"}),
                         dict({"u_id": 3, "full_name": "BBB", "role": "Patient", "gender": "male", "created_at": "2022-02-18", "phone": "1111111111"})]

    device_dictlist = [dict({"d_id": 1, "type": "sphygmomanometer", "value_type": "Blood_Pressure"}),
                       dict({"d_id": 2, "type": "thermometer", "value_type": "Temperature"}),
                       dict({"d_id": 3, "type": "pulse_device", "value_type": "Pulse"}),
                       dict({"d_id": 4, "type": "oximeter", "value_type": "Blood_Oxygen"}),
                       dict({"d_id": 5, "type": "weight_machine", "value_type": "Weight"}),
                       dict({"d_id": 6, "type": "glucometer", "value_type": "Blood_Glucose"})]

    assignment_dictlist = [dict({"a_id": 1, "assign_person": 2, "assigned_to": 3, "device": 1}),
                               dict({"a_id": 2, "assign_person": 2, "assigned_to": 3, "device": 2})]

    data_captured_dictlist = [dict({"r_id": 1, "a_id": 1, "value": 100.0}),
                              dict({"r_id": 2, "a_id": 2, "value": 37.5})]

    store_users(user_dictlist)
    store_devices(device_dictlist)
    store_assignments(assignment_dictlist)
    store_records(data_captured_dictlist)

def store_users(users):
    json_user = json.dumps(users)
    f = open(data_dir + 'user.json','w')
    f.write(json_user)
    f.close()

def store_devices(devices):
    json_device = json.dumps(devices)
    f = open(data_dir + 'device.json','w')
    f.write(json_device)
    f.close()

def store_assignments(assignments):
    json_assignment = json.dumps(assignments)
    f = open(data_dir + 'assignment.json','w')
    f.write(json_assignment)
    f.close()

def store_records(records):
    json_data_captured = json.dumps(records)
    f = open(data_dir + 'data_captured.json','w')
    f.write(json_data_captured)
    f.close()

def load_users():
    load_list = os.listdir(data_dir)
    users = []
    if "user.json" in load_list:
        f = open(data_dir + 'user.json','r')
        users = json.loads(f.read())
        f.close()

    return users

def load_devices():
    load_list = os.listdir(data_dir)
    devices = []
    if "device.json" in load_list:
        f = open(data_dir + 'device.json','r')
        devices = json.loads(f.read())
        f.close()

    return devices

def load_assignments():
    load_list = os.listdir(data_dir)
    assignments = []
    if "assignment.json" in load_list:
        f = open(data_dir + 'assignment.json','r')
        assignments = json.loads(f.read())
        f.close()

    return assignments

def load_records():
    load_list = os.listdir(data_dir)
    records = []
    if "data_captured.json" in load_list:
        f = open(data_dir + 'data_captured.json','r')
        records = json.loads(f.read())
        f.close()

    return records

def user_registration(name, role, gender, phone):
    users = load_users()
    new_sample = dict({"u_id":len(users)+1, "full_name": name, "role": role, "gender": gender, "created_at": datetime.datetime.now().strftime("%Y-%m-%d"), "phone": str(phone)})
    users.append(new_sample)
    store_users(users)
    return users

def device_registration(type, value_type):
    devices = load_devices()
    new_sample = dict({"d_id": len(devices)+1, "type": type, "value_type": value_type})
    devices.append(new_sample)
    store_devices(devices)
    # print(devices)
    return devices

def new_assignment(assign_person, assigned_to, device):
    assignments = load_assignments()
    devices = load_devices()
    users = load_users()
    if (not isinstance(assign_person, int) and (not isinstance(assigned_to, int)) and (not isinstance(device, int))):
        print("expected parameter 1, 2, 3 are integer")
        return assignments

    if (assign_person > len(users) or assigned_to > len(users)):
        print("parameter 1 or 2 is not in user list")
        return assignments

    if (device > len(devices)):
        print("parameter 3 is not in devices list")
        return assignments

    if (users[assign_person-1]["role"] != "Doctor" and users[assign_person-1]["role"] != "Nurse"):
        print("Person who make the assignment should be Doctor or Nurse")
        return assignments

    if (users[assigned_to-1]["role"] != "Patient"):
        print("Only patients could be assigned to devices")
        return assignments

    new_sample = dict({"a_id": len(assignments)+1, "assign_person": assign_person, "assigned_to": assigned_to, "device": device})
    assignments.append(new_sample)
    store_assignments(assignments)
    # print(assignments)
    return assignments

def new_data_captured(assignment, value):
    records = load_records()
    assignments = load_assignments()
    if (not isinstance(assignment, int)):
        print("expected parameter 1 is integer")
        return records
    if (assignment > len(assignments)):
        print(f"Do not have assignment {assignment}")
        return records
    if (not isinstance(value, int)) and (not isinstance(value, float)):
        print("expected parameter 2 is int or float")
        return records

    new_sample = dict({"r_id": len(records)+1, "a_id": assignment, "value": value})
    records.append(new_sample)
    store_records(records)
    # print(records)
    return records

if __name__ == '__main__':
    make_json_input()
    # users = user_registration("CCC","Nurse","Male","2222222222")
    # devices = device_registration("height_machine", "Height")
    # assignments = new_assignment(2, 3, 3)
    # records = new_data_captured(2, 100)
