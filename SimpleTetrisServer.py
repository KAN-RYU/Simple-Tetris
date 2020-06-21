from socket import *
import threading
from queue import Queue
import time
import pickle

messageQ = Queue()
client = []
battle = []
lock = threading.Lock()
statics = {} #nickname : [win, lose]

class battleManager():
    def  __init__(self, home, away):
        self.homeSock = home[0]
        self.awaySock = away[0]
        self.homeNickname = home[2]
        self.awayNickname = away[2]
        self.Message = Queue()
        print(home[2], away[2])

        self.homeReceiver = threading.Thread(target=self.receiver, args=(self.homeSock, home[1], True, home[2]))
        self.awayReceiver = threading.Thread(target=self.receiver, args=(self.awaySock, away[1], False, away[2]))
        self.homeReceiver.daemon = True
        self.awayReceiver.daemon = True
        self.homeReceiver.start()
        self.awayReceiver.start()
        
        self.serverSender = threading.Thread(target=self.sender, args=())
        self.serverSender.daemon = True
        self.serverSender.start()
        
        self.homeSock.send('Connected.'.encode('utf-8'))
        self.awaySock.send('Connected.'.encode('utf-8'))
        
        seed = str(int(time.time()))
        self.homeSock.send(seed.encode('utf-8'))
        self.awaySock.send(seed.encode('utf-8'))
        print('battle start!')

    def sender(self):
        while True:
            mes:str = self.Message.get()
            if mes.endswith('YOUWIN'):
                if mes[:4] == 'home':
                    lock.acquire()
                    statics[self.homeNickname][1] += 1
                    statics[self.awayNickname][0] += 1
                    lock.release()
                elif mes[:4] == 'away':
                    lock.acquire()
                    statics[self.homeNickname][0] += 1
                    statics[self.awayNickname][1] += 1
                    lock.release()
            try:
                if len(mes) < 100:
                    print(mes)
                if mes[:4] == 'home':
                    self.awaySock.send(len(mes.encode('utf-8')).to_bytes(4, byteorder = 'little'))
                    self.awaySock.send(mes.encode('utf-8'))
                elif mes[:4] == 'away':
                    self.homeSock.send(len(mes.encode('utf-8')).to_bytes(4, byteorder = 'little'))
                    self.homeSock.send(mes.encode('utf-8'))
            except:
                break
    
    def receiver(self, sock, addr, home, nickname):
        tmp = b''
        sock.settimeout(1)
        while True:
            try:
                try:
                    recvData = sock.recv(1024)
                except timeout:
                    pass
                else:
                    tmp += recvData
                if len(tmp) < 4:
                    continue
                mesLength = int.from_bytes(tmp[0:4], "little")
                if len(tmp[4:]) < mesLength:
                    continue
                self.Message.put(('home' if home else 'away') + tmp[4:4+mesLength].decode('utf-8'))
                tmp = tmp[4+mesLength:]
            except:
                lock.acquire()
                message = 'Disconnected by ' + nickname
                print(message + ' ' + str(addr[0]) + ":" + str(addr[1]))
                lock.release()
                break

if __name__ == "__main__":
    port = 12346

    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(('', port))
    serverSock.listen()
    
    try:
        with open('statics.bin', 'rb') as f:
            statics = pickle.load(f)
    except:
        statics = {}

    print('Server Started.')

    serverSock.settimeout(1)
    while True:
        try:
            try:
                connectionSock, addr = serverSock.accept()
                print(addr)
                lock.acquire()
                time.sleep(1)
                tmp = connectionSock.recv(1024)
                mesLength = int.from_bytes(tmp[0:4], "little")
                nickname = tmp[4:4+mesLength].decode('utf-8')
                print(nickname, 'has connected')
                if not nickname in statics:
                    statics[nickname] = [0, 0]
                print(nickname + ':', statics[nickname][0], 'Wins', statics[nickname][1], 'loses')
                client.append((connectionSock, addr, nickname))
                if len(client) % 2 == 0 and len(client) > 0:
                    print('init battle')
                    battle.append(battleManager(client[-1], client[-2]))
                lock.release()
            except:
                time.sleep(0.01)
        except:
            break
        
    with open('statics.bin', 'wb') as f:
        pickle.dump(statics, f, pickle.HIGHEST_PROTOCOL)

    print('Server Stopped.')
    serverSock.close()