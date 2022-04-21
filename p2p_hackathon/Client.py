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
    socket_server = socket.socket()
    server_host = socket.gethostname()
    ip = socket.gethostbyname(server_host)
    sport = 8080

    socket_server.connect((ip, sport))
 
    socket_server.send(name.encode())
    server_name = socket_server.recv(1024)
    server_name = server_name.decode()
 
    print(server_name,' has joined...')
    while True:
        message = (socket_server.recv(1024)).decode()
        print(server_name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ':\n', message)
        message = input("Me : ")
        socket_server.send(message.encode()) 

if __name__ == "__main__":
    login()