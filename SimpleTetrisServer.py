from socket import *
import threading
from queue import Queue
import time

messageQ = Queue()
client = []
battle = []
lock = threading.Lock()

class battleManager():
    def  __init__(self, home, away):
        self.homeSock = home[0]
        self.awaySock = away[0]
        self.Message = Queue()
        print(home[1], away[1])

        self.homeReceiver = threading.Thread(target=self.receiveData, args=(self.homeSock, home[1], True))
        self.awayReceiver = threading.Thread(target=self.receiveData, args=(self.awaySock, away[1], False))
        self.homeReceiver.daemon = True
        self.awayReceiver.daemon = True
        self.homeReceiver.start()
        self.awayReceiver.start()
        print('receiver')
        
        self.serverSender = threading.Thread(target=self.sender, args=())
        self.serverSender.daemon = True
        self.serverSender.start()
        print('sender')
        
        self.homeSock.send('Connected.'.encode('utf-8'))
        self.awaySock.send('Connected.'.encode('utf-8'))
        
        seed = str(int(time.time()))
        self.homeSock.send(seed.encode('utf-8'))
        self.awaySock.send(seed.encode('utf-8'))
        print('battle start!')

    def sender(self):
        while True:
            mes = self.Message.get()
            if mes[:4] == 'home':
                self.awaySock.send(mes.encode('utf-8'))
            if mes[:4] == 'away':
                self.homeSock.send(mes.encode('utf-8'))
    
    def receiveData(self, sock, addr, home):
        while True:
            try:
                recvData = sock.recv(len(('.' * 304).encode('utf-8')))
                self.Message.put(('home' if home else 'away') + recvData.decode('utf-8'))
            except:
                break

def send():
    while True:
        message = messageQ.get()
        lock.acquire()
        for sock, name, addr in client:
            sock.send(message.encode('utf-8'))
        lock.release()

def receive(sock, name, addr):
    while True:
        try:
            recvData = sock.recv(1024)
            decoded = name + " : " + recvData.decode('utf-8')
            messageQ.put(decoded)
            print(decoded)

        except:
            lock.acquire()
            message = 'Disconnected by ' + name
            messageQ.put(message)
            print(message + ' ' + str(addr[0]) + ":" + str(addr[1]))

            for i in range(len(client)):
                if client[i][2][0] == addr[0] and client[i][2][1] == addr[1]:
                    client[i] = ''
                    break
            lock.release()
            break


if __name__ == "__main__":
    port = 12346

    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(('', port))
    serverSock.listen()

    print('Server Started.')
    sender = threading.Thread(target=send, args=())
    sender.daemon = True
    sender.start()

    serverSock.settimeout(1)
    while True:
        try:
            try:
                connectionSock, addr = serverSock.accept()
                lock.acquire()
                client.append((connectionSock, addr))
                if len(client) % 2 == 0 and len(client) > 0:
                    print('init battle')
                    battle.append(battleManager(client[-1], client[-2]))
                lock.release()
            except:
                time.sleep(0.01)
        except:
            break

    print('Server Stopped.')
    serverSock.close()