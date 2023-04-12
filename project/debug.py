from datetime import datetime
import re, socket

DATETIME_FORMAT = "[%Y/%m/%d %H:%M:%S]:\n"
ENCODING = "utf-8"
MAX_SIZE = 16384

CMD_CHECK = re.compile(r"\S.*")

class Console:

    def __init__(self, chost="127.0.0.1", cport=3333):
        self.host = chost
        self.port = cport
        self.sobj = socket.socket()
        self.sobj.connect((chost, cport))

    def report(self, text: str, data=True, add_tab=False):
        if add_tab:
            text = "".join(["\t" + x + "\n" for x in text.split("\n")])
        return (datetime.now().strftime(DATETIME_FORMAT) if data is True else "") + text
    
    def send(self, cmd):
        self.sobj.send(cmd.encode(ENCODING))
    
    def recv(self):
        return self.sobj.recv(MAX_SIZE).decode(ENCODING)
    

    def terminal(self):
        while True:
            command = input(">>>")
            print(self.command(command))
    
    def command(self, cmd):
        if CMD_CHECK.fullmatch(cmd):
            self.send(cmd)
            if cmd == "exit":
                exit(0)
            return self.report(self.recv())

console = Console()
console.terminal()