from flask import Flask, render_template, send_file, request, abort
from datetime import datetime
import socket, threading, os, _thread

app = Flask(__name__, template_folder=r"C:\Users\unknown\Documents\code\code\project\templates", static_folder=r"C:\Users\unknown\Documents\code\code\project\static")

BANNED_IP = []

#for remote console
MAX_SIZE = 1024
ENCODING = "utf-8"
RUNNING = True

STATS = {
    "Started" : datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
    "Requests": 0,
    "Running" : RUNNING,
    "BANNED_IP" : BANNED_IP
}



@app.before_request
def before_request():
    if not RUNNING:
        abort(503)
    if request.remote_addr in BANNED_IP:
        abort(403)
    STATS.update({"Requests" : STATS["Requests"] + 1})


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/reg")
def reg():
    return render_template("reg.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")


#================
#css

@app.route("/css/index.css")
def css_index():
    return send_file("static\\css\\index.css")

@app.route("/css/login.css")
def css_login():
    return send_file("static\\css\\login.css")

@app.route("/css/profile.css")
def css_profile():
    return send_file("static\\css\\profile.css")


#=================error templates

@app.errorhandler(503)
def e503(e):
    return render_template("503.html")


#================remote console

class Server:

    def __init__(self, host="127.0.0.1", port=3333, ConsoleAutoStart=True):
        self.host = host
        self.port = port
        self.sobj = socket.socket()
        self.CAS = ConsoleAutoStart
        
    def start(self):
        self.sobj.bind((self.host, self.port))
        self.sobj.listen()

        try:
            while True:
                conn, addr = self.sobj.accept()
                try:
                    while True:
                        cmd = self.recv(conn)
                        if cmd == "leave": #if remote console sent "leave" command, closing conn and waition for another conn
                            conn.close()
                            break
                        ret = self.do(cmd)
                        self.send(conn, ret)
                except Exception as e: 
                    print("Connection lost")
                    print(e)
                    self.sobj.close()
                    exit(0)
        except Exception as e:
            print(e)
            self.sobj.close()
            exit(0)
    
    def send(self, conn, data):
        conn.send(data.encode(ENCODING))
    
    def recv(self, conn):
        return conn.recv(MAX_SIZE).decode(ENCODING)

    def do(self, cmd):
        global RUNNING

        if cmd == "stop":
            if RUNNING == False:
                return "already stopped"
            RUNNING = False
            return "stopped"
        elif cmd == "continue":
            if RUNNING == True:
                return "alreday running"
            RUNNING = True
            return "continued"
        elif cmd == "exit":
            _thread.interrupt_main()
            exit(0)
        
        elif cmd[:3] == "ban":
            if cmd[4:] not in BANNED_IP:
                BANNED_IP.append(cmd[4:])
                return f"now, {cmd[4:]} is banned "
            return f"{cmd[4:]} is already banned"
        
        elif cmd[:5] == "unban":
            if cmd[6:] in BANNED_IP:
                BANNED_IP.remove(cmd[6:])
                return f"now, {cmd[6:]} is unbanned"
            else:
                return f"{cmd[6:]} is not banned"
        elif cmd == "BANNED_IP":
            return "|".join(BANNED_IP) if BANNED_IP != [] else "No banned IPs yet"
        
        elif cmd == "STATS":
            return f"""STATS:
    Started:   {STATS['Started']}
    Requests:  {STATS['Requests']}
    Banned IP: {'|'.join(BANNED_IP) if BANNED_IP != [] else 'No banned IPs yet'}
    Running:   {STATS['Running']}"""
        else:
            return "no such command as " + cmd


if __name__ == "__main__":
    server = Server()
    Tserver = threading.Thread(target=server.start)
    Tserver.start()
    try:
        app.run(host="127.0.0.1", port=80)
    except KeyboardInterrupt:
        print("Stopped by remote console")