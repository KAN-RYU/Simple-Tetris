import random
from SimpleTetrisConstant import *

class SimpleTetrisGame():
    def __init__(self):
        self.field = []
        for i in range(25):
            self.field.append([0]*12)

        self.ghostField = []
        for i in range(25):
            self.ghostField.append([0]*12)

        for i in range(25):
            self.field[i][10] = 8
            self.field[i][11] = 8
            self.ghostField[i][10] = 8
            self.ghostField[i][11] = 8
        
        self.minoQueue = self.NextMinoQueue()
        for i in self.NextMinoQueue():
            self.minoQueue.append(i)
        
        self.NextMino()
        self.curHold = 0
        
        self.moveDelay = 0
        self.softDropDelay = 0
        self.hardDropDelay = 0
        self.clearDelay = 0
        
        self.lineClearFlag = False
        self.spinCWDelay = False
        self.spinCCWDelay = False
        self.holdFlag = False
        self.softDropFlag = False
        self.hardDropFlag = False
        self.gameOverFlag = False
    
    def NextMinoQueue(self):
        nextMinoQueue = ['T', 'S', 'Z', 'L', 'J', 'O', 'I']
        return random.sample(nextMinoQueue, 7)
    
    def tick(self):
        self.moveDelay = self.moveDelay - 1 if self.moveDelay > 0 else 0
        self.hardDropDelay = self.hardDropDelay - 1 if self.hardDropDelay > 0 else 0
        self.softDropDelay = self.softDropDelay - 1 if self.softDropDelay > 0 else 0
        self.clearDelay = self.clearDelay - 1 if self.clearDelay > 0 else 0
    
    def NextMino(self):
        curMino = self.minoQueue.pop(0)
        curPos = [0, 0]
        curRot = 0
        if curMino == 'I':
            curPos = [4, 4]
        else:
            curPos = [5, 4]
        for state in MINO_STATE[curMino][curRot]:
            if self.field[curPos[0] + state[0]][curPos[1] + state[1]] != 0:
                self.gameOverFlag = True
            self.field[curPos[0] + state[0]][curPos[1] + state[1]] = MINO_DICT[curMino]
        self.curMino = curMino
        self.curPos = curPos
        self.curRot = curRot
        self.holdFlag = False
    
    def Collide(self, mino, pos, rot, newrot, kick):
        if not mino == 'I' and (pos[0] > 25 or pos [1] < 0 or pos[1] > 9):
            raise
        collideFlag = True
        if kick:
            for test in WALL_KICK['I' if mino == 'I' else 'X'][rot][newrot]:
                collideFlag = True
                newPos = [pos[0] + test[0], pos[1] + test[1]]
                for state in MINO_STATE[mino][newrot]:
                    if newPos[1] + state[1] < 0:
                        collideFlag = False
                    collideFlag = collideFlag and (self.ghostField[newPos[0] + state[0]][newPos[1] + state[1]] == 0)
                if collideFlag:
                    return newPos, newrot
            return pos, rot
        else:
            for state in MINO_STATE[mino][rot]:
                if not mino == 'I' and pos[1] + state[1] < 0:
                    collideFlag = False
                collideFlag = collideFlag and (self.ghostField[pos[0] + state[0]][pos[1] + state[1]] == 0)

            return not collideFlag