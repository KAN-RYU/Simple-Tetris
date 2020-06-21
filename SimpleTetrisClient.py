from socket import *
import threading
from queue import Queue
import time

class SimpleTetrisClient():
    def __init__(self, ip):
        self.clientSock = socket(AF_INET, SOCK_STREAM)
        self.server_ip = ip

        self.network = threading.Thread(target = self.networkRunner, args = ())
        self.connected = False
        self.ready = False
        self.lock = threading.Lock()
        self.logFlag = 0
        self.log = Queue()
        self.seed = 0

        self.oppoField = []
        for i in range(27):
            self.oppoField.append([0]*12)

        for i in range(27):
            self.oppoField[i][10] = 8
            self.oppoField[i][11] = 8

        for i in range(12):
            self.oppoField[25][i] = 8
            self.oppoField[26][i] = 8
        
        self.attackQueue = []
        self.winFlag = False

        self.network.daemon = True
        self.networkFlag = True
        self.network.start()

    def printLog(self, message):
        self.lock.acquire()
        self.logFlag += 1
        self.lock.release()
        self.log.put(message)

    def networkRunner(self):
        port = 12346

        while True:
            try:
                self.clientSock.connect((self.server_ip, port))
            except:
                self.printLog('Server Connection failed. retry...')
            else:
                break
        self.printLog('Server Connected, Wait opponent.')
        self.connected = True
        
        firstData = self.clientSock.recv(len('Connected.'.encode('utf-8')))
        self.printLog(firstData.decode('utf-8'))
        seed = self.clientSock.recv(len(str(int(time.time())).encode('utf-8')))
        self.seed = int(seed.decode('utf-8'))
        time.sleep(3)
        self.ready = True
        
        self.clientSock.settimeout(1)
        
        tmp = b''
        while True:
            self.lock.acquire()
            flag = self.networkFlag
            self.lock.release()
            if not flag:
                self.clientSock.close()
                break
            
            try:
                recvData = self.clientSock.recv(1024)
            except:
                pass
            else:
                tmp += recvData
            if len(tmp) < 4:
                continue
            mesLength = int.from_bytes(tmp[0:4], "little")
            if len(tmp[4:]) < mesLength:
                continue
            recvData = tmp[4:4+mesLength].decode('utf-8')
            tmp = tmp[4+mesLength:]
            if recvData[4:4+6] == 'ATTACK':
                print(recvData)
                self.lock.acquire()
                self.attackQueue.append(int(recvData[4+6:]))
                self.lock.release()
            elif recvData[4:4+6] == 'YOUWIN':
                print(recvData)
                self.lock.acquire()
                self.winFlag = True
                self.lock.release()
            else:
                self.lock.acquire()
                for i, s in enumerate(recvData[4:]):
                    self.oppoField[4 + i // 10][i % 10] = int(s)
                self.lock.release()
    
    def sendData(self, data):
        self.clientSock.send(len(data.encode('utf-8')).to_bytes(4, byteorder = 'little'))
        self.clientSock.send(data.encode('utf-8'))
    
    def close(self):
        self.lock.acquire()
        self.networkFlag = False
        self.lock.release()
        self.network.join()