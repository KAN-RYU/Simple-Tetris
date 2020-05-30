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

        self.homeReceiver = threading.Thread(target=self.receiver, args=(self.homeSock, home[1], True))
        self.awayReceiver = threading.Thread(target=self.receiver, args=(self.awaySock, away[1], False))
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
            try:
                if mes[:4] == 'home':
                    self.awaySock.send(len(mes.encode('utf-8')).to_bytes(4, byteorder = 'little'))
                    self.awaySock.send(mes.encode('utf-8'))
                if mes[:4] == 'away':
                    self.homeSock.send(len(mes.encode('utf-8')).to_bytes(4, byteorder = 'little'))
                    self.homeSock.send(mes.encode('utf-8'))
            except:
                break
    
    def receiver(self, sock, addr, home):
        tmp = b''
        while True:
            try:
                recvData = sock.recv(1024)
                tmp += recvData
                if len(tmp) < 4:
                    continue
                mesLength = int.from_bytes(tmp[0:4], "little")
                if len(tmp[4:]) < mesLength:
                    continue
                self.Message.put(('home' if home else 'away') + tmp[4:4+mesLength].decode('utf-8'))
                tmp = tmp[4+mesLength:]
            except:
                break

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