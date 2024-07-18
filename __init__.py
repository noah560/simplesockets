import socket, threading
import constants as const
import server

def __send(conn, msg, header):
    message = msg.encode(const.FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(const.FORMAT)
    send_length += b" " * (header - len(send_length))
    conn.send(send_length)
    conn.send(message)


def __recv(conn, header):
    msg_length = conn.recv(header).decode(const.FORMAT)
    msg_length = int(msg_length)
    msg = conn.recv(msg_length).decode(const.FORMAT)
    return msg




class Client:
    def __init__(self, port, server, header=64):
        self.PORT = port
        self.SERVER = server
        self.HEADER = header
        self.ADDR = (server, port)
    

    def init(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

    def _recv(self):
        return __recv(self.client, self.HEADER)
    

    def _send(self, msg):
        __send(self.client, msg, self.HEADER)
    

    def recv_thread(self):
        while True:
            try:
                msg = self._recv()
            except ConnectionResetError:
                break
            except socket.error:
                break
            self._messages.append(msg)
    

    def connect(self):
        self._messages = []
        self.client.connect(self.ADDR)
        self.thread = threading.Thread(target=self.recv_thread, args=())
        self.thread.start()
    

    def send(self, msg):
        self._send(const.NORMAL + msg)
    

    def disconnect(self):
        self._send(const.SPECIAL + const.DISCONNECT)
    

    @property
    def messages(self):
        messages = self._messages[:]
        self._messages = []
        return messages
    
