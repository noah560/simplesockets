import socket, threading
import constants as const
import serverlogs as SLogs
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


class DataRepeatServer:
    def __init__(self, port, server, header=64):
        self.PORT = port
        self.SERVER = server
        self.HEADER = header
        self.ADDR = (server, port)
        self.clients  = []
    

    def init(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
    

    def _send(self, conn, msg):
        __send(conn, msg, self.HEADER)
    

    def _recv(self, conn):
        return __recv(conn, self.HEADER)
    

    def sendToAllClients(self, msg):
        for conn in self.clients:
            self._send(conn, msg)
    

    def handle_client(self, conn, addr):
        self.clients.append(conn)
        self.logs.append(SLogs.ConnectionOpened(addr))

        connected = True
        while connected:
            try:
                msg = self._recv(conn)
            except ConnectionResetError:
                break
            except socket.error:
                break
            msg_type = msg[0]
            msg = msg[1:]
            if msg_type == const.SPECIAL:
                if msg == const.DISCONNECT:
                    connected = False
            else:
                self.logs.append(SLogs.DataSent(addr, msg))
                self.sendToAllClients(msg)
        self.clients.remove(conn)
        conn.close()
        self.logs.append(SLogs.ConnectionClosed(addr))
    

    def run(self, selfConnStops=False):
        self.logs = []
        self.server.listen()
        running = True
        while running:
            conn, addr = self.server.accept()
            if self.SERVER in addr and selfConnStops:
                for client in self.clients:
                    client.close()
                self.clients = []
                running = False
            else:
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
        return self.logs