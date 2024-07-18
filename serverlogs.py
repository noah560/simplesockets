class ConnectionOpened:
    def __init__(self, addr):
        self.addr = addr



class ConnectionClosed:
    def __init__(self, addr):
        self.addr = addr



class DataSent:
    def __init__(self, addr, data):
        self.addr = addr
        self.data = data


