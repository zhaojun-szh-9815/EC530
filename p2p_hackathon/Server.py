import time, socket, sys
sys.path.append("../Project2") 
from device_api import check_user_password
 
def login():
    username = input("username: ")
    password = input("password: ")
    res = check_user_password(username, password)
    if res["State"] == "Success":
        user = res["Content"]
        print(user["First_Name"], user["Last_Name"], "login!")
        run(username)
    else:
        print("Login unsuccessfully!" + res["State"])

def run(name):
    new_socket = socket.socket()
    host_name = socket.gethostname()
    s_ip = socket.gethostbyname(host_name)
 
    port = 8080
 
    new_socket.bind((host_name, port))
    print("Binding successful!")
 
    new_socket.listen(1) 
 
    conn, add = new_socket.accept()
 
    print("Received connection from ", add[0])
    print('Connection Established. Connected From: ',add[0])
 
    client = (conn.recv(1024)).decode()
    print(client + ' has connected.')
 
    conn.send(name.encode())
    while True:
        message = input('Me : ')
        conn.send(message.encode())
        message = conn.recv(1024)
        message = message.decode()
        print(client, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ':\n', message)

if __name__ == "__main__":
    login()