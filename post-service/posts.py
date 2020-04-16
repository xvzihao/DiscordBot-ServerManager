import socket
from threading import Thread

IPADDR = 1026

class Server:
    def __init__(self, blit_table: dict):
        self.ip = socket.gethostbyname_ex(socket.gethostname())[-1][-1]
        self.table = blit_table
        self.run = True

    def client(self, conn: socket.socket, addr):
        try:
            recv = conn.recv(512).decode('utf8')
            if recv == 'stop':
                self.run = False
            if recv not in self.table:
                conn.send(b'[]')
            else:
                obj = self.table[recv]
                if type(obj) in (int, float, list, dict, tuple, set):
                    obj = str(obj)

                if type(obj) == str:
                    conn.send(bytes(obj, 'utf8'))

                else:
                    conn.send(bytes(str(obj()), 'utf8'))
                conn.close()
        except:
            conn.send(b'[]')
            conn.close()

    def loop(self):
        s = socket.socket()
        s.bind((self.ip, IPADDR))
        s.listen(128)
        s.settimeout(1)

        while self.run:
            try:
                conn, addr = s.accept()
                conn.settimeout(10)
                Thread(target=self.client, args=(conn, addr)).start()
            except socket.timeout:
                pass
        s.close()

def get(addr='127.0.0.1', post=''):
    s = socket.socket()
    s.connect((addr, IPADDR))
    s.send(post.encode('utf8'))
    recv = s.recv(512).decode('utf8')
    s.close()
    return recv
