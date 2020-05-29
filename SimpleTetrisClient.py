from socket import *
import threading
from queue import Queue
import time

class SimpleTetrisClient():
    def __init__(self):
        self.clientSock = socket(AF_INET, SOCK_STREAM)

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

        self.network.daemon = True
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
                self.clientSock.connect(('127.0.0.1', port))
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
        
        while True:
            recvData = self.clientSock.recv(len(('.' * 304).encode('utf-8'))).decode('utf-8')
            self.lock.acquire()
            for i, s in enumerate(recvData[4:]):
                self.oppoField[4 + i // 10][i % 10] = int(s)
            self.lock.release()
    
    def sendData(self, data):
        self.clientSock.send(data.encode('utf-8'))