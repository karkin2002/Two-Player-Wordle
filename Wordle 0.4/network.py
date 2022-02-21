import socket
import pickle
from player import Player

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        f = open("ipAddress.txt", "r")
        self.host = f.readline()
        self.port = 5555
        self.addr = (self.host, self.port)
        self.p = self.connect()
    
    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(8048)) # recieveing object, decomposing it
        except socket.error as e:
            print(e)
    
    def send(self, data): # Send data to server
        try:
            self.client.send(pickle.dumps(data)) # sending object, encrypt it
            return pickle.loads(self.client.recv(8048))
    
        except socket.error as e:
            print(e)