import random
import copy
import time
from SimpleTetrisConstant import *

class SimpleTetrisGame():
    def __init__(self, multiPlay = False):
        self.field = []
        for i in range(27):
            self.field.append([0]*12)

        self.ghostField = []
        for i in range(27):
            self.ghostField.append([0]*12)

        for i in range(27):
            self.field[i][10] = 8
            self.field[i][11] = 8
            self.ghostField[i][10] = 8
            self.ghostField[i][11] = 8
        
        for i in range(12):
            self.field[25][i] = 8
            self.field[26][i] = 8
            self.ghostField[25][i] = 8
            self.ghostField[26][i] = 8

        self.minoQueue = self.NextMinoQueue()
        for i in self.NextMinoQueue():
            self.minoQueue.append(i)

        self.NextMino()
        self.curHold = 0

        self.posShadow = [0, 0]
        self.rotShadow = 0
        
        self.seed = 0

        self.lastLineCleared = 0
        self.lastLineClearedDelay = 0

        self.moveDelay = 0
        self.softDropDelay = 0
        self.hardDropDelay = 0
        self.clearDelay = 0
        
        self.gravityCount = 0
        self.BTBCount = 0
        self.recentComboCount = 0
        self.comboCount = 0
        self.totalLineCleared = 0
        
        self.lineClearFlag = False
        self.spinCWDelay = False
        self.spinCCWDelay = False
        self.holdFlag = False
        self.softDropFlag = False
        self.hardDropFlag = False
        self.gameOverFlag = False
        self.tSpinFlag = False
        self.lastTSpinFlag = False
        self.lockFlag = False
        self.softLockFlag = False

    def NextMinoQueue(self):
        nextMinoQueue = ['T', 'S', 'Z', 'L', 'J', 'O', 'I']
        return random.sample(nextMinoQueue, 7)

    def tick(self):
        self.gravityDrop()
        
        self.processDrop()

        self.clearLine()

        if len(self.minoQueue) < 6:
                for i in self.NextMinoQueue():
                    self.minoQueue.append(i)

        self.moveDelay = self.moveDelay - 1 if self.moveDelay > 0 else 0
        self.hardDropDelay = self.hardDropDelay - 1 if self.hardDropDelay > 0 else 0
        self.softDropDelay = self.softDropDelay - 1 if self.softDropDelay > 0 else 0
        self.clearDelay = self.clearDelay - 1 if self.clearDelay > 0 else 0
        self.lastLineClearedDelay = self.lastLineClearedDelay - 1 if self.lastLineClearedDelay - 1 > 0 else 0
        self.gravityCount = self.gravityCount - 1 if self.gravityCount > 0 else DELAY_GRAVITY

    def NextMino(self):
        nextMino = self.minoQueue.pop(0)
        nextPos = [0, 0]
        nextRot = 0
        if nextMino == 'I':
            nextPos = [4, 4]
        else:
            nextPos = [5, 4]
        for state in MINO_STATE[nextMino][nextRot]:
            if self.field[nextPos[0] + state[0]][nextPos[1] + state[1]] != 0:
                self.gameOverFlag = True
            self.field[nextPos[0] + state[0]][nextPos[1] + state[1]] = MINO_DICT[nextMino]
        self.curMino = nextMino
        self.curPos = nextPos
        self.curRot = nextRot
        self.holdFlag = False
        self.tSpinFlag = False
        self.lockFlag = False
        self.softLockFlag = False
        self.gravityCount = DELAY_GRAVITY
        self.getMinoFlag = True

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

    def move(self, direction):
        if self.moveDelay > 2 or self.clearDelay > 0:
            pass
        else:
            try:
                if self.moveDelay == 0:
                    self.moveDelay = DELAY_FIRST
                else :
                    self.moveDelay = DELAY_V
                if not self.Collide(self.curMino, [self.curPos[0], self.curPos[1] + direction],
                                    self.curRot, self.curRot, False):
                    for state in MINO_STATE[self.curMino][self.curRot]:
                        self.field[self.curPos[0] + state[0]][self.curPos[1] + state[1]] = 0

                    self.curPos[1] = self.curPos[1] + direction

                    for state in MINO_STATE[self.curMino][self.curRot]:
                        self.field[self.curPos[0] + state[0]][self.curPos[1] + state[1]] = MINO_DICT[self.curMino]
                    
                    self.tSpinFlag = False
                    self.lockFlag = self.Collide(self.curMino, [self.curPos[0] + 1, self.curPos[1]],
                                    self.curRot, self.curRot, False)
            except:
                pass

    def moveLeft(self):
        self.move(-1)

    def moveRight(self):
        self.move(1)

    def spin(self, direction):
        if self.spinCWDelay or self.spinCCWDelay or self.clearDelay > 0:
            pass
        else:
            try:
                if direction == 1:
                    self.spinCWDelay = True
                elif direction == -1:
                    self.spinCCWDelay = True
                newPos, newRot =  self.Collide(self.curMino, self.curPos, self.curRot,
                                                (self.curRot + direction) % 4, True)
                for state in MINO_STATE[self.curMino][self.curRot]:
                        self.field[self.curPos[0] + state[0]][self.curPos[1] + state[1]] = 0

                self.curPos = copy.deepcopy(newPos)
                self.curRot = newRot

                for state in MINO_STATE[self.curMino][self.curRot]:
                    self.field[self.curPos[0] + state[0]][self.curPos[1] + state[1]] = MINO_DICT[self.curMino]
                
                if self.curMino == 'T':
                    tSpinCount = 0
                    tSpinCount += 1 if self.field[self.curPos[0] - 1][self.curPos[1] - 1] != 0 else 0
                    tSpinCount += 1 if self.field[self.curPos[0] - 1][self.curPos[1] + 1] != 0 else 0
                    tSpinCount += 1 if self.field[self.curPos[0] + 1][self.curPos[1] - 1] != 0 else 0
                    tSpinCount += 1 if self.field[self.curPos[0] + 1][self.curPos[1] + 1] != 0 else 0
                    if tSpinCount >= 3:
                        self.tSpinFlag = True
                
                if self.Collide(self.curMino, [self.curPos[0] + 1, self.curPos[1]],
                                    self.curRot, self.curRot, False):
                    self.gravityCount = DELAY_GRAVITY
            except:
                pass

    def spinCW(self):
        self.spin(1)

    def spinCCW(self):
        self.spin(-1)

    def hold(self):
        if self.holdFlag or self.clearDelay > 0:
            pass
        else:
            if self.curHold == 0:
                self.curHold = self.curMino
                for state in MINO_STATE[self.curMino][self.curRot]:
                    self.field[self.curPos[0] + state[0]][self.curPos[1] + state[1]] = 0

                self.NextMino()
            else:
                for state in MINO_STATE[self.curMino][self.curRot]:
                    self.field[self.curPos[0] + state[0]][self.curPos[1] + state[1]] = 0
                tmp = self.curMino
                self.curMino = self.curHold
                self.curHold = tmp
                self.curRot = 0
                if self.curMino == 'I':
                    self.curPos = [4, 4]
                else:
                    self.curPos = [5, 4]
                for state in MINO_STATE[self.curMino][self.curRot]:
                    if self.field[self.curPos[0] + state[0]][self.curPos[1] + state[1]] != 0:
                        self.gameOverFlag = True
                    self.field[self.curPos[0] + state[0]][self.curPos[1] + state[1]] = MINO_DICT[self.curMino]
            self.holdFlag = True

    def softDrop(self):
        if self.softDropDelay > 2 or self.clearDelay > 0 or self.lockFlag:
            pass
        else:
            try:
                if self.softDropDelay == 0:
                    self.softDropDelay = DELAY_FIRST
                else :
                    self.softDropDelay = DELAY_V
                if not self.Collide(self.curMino, [self.curPos[0] + 1, self.curPos[1]],
                                    self.curRot, self.curRot, False):
                    for state in MINO_STATE[self.curMino][self.curRot]:
                        self.field[self.curPos[0] + state[0]][self.curPos[1] + state[1]] = 0

                    self.curPos[0] += 1

                    for state in MINO_STATE[self.curMino][self.curRot]:
                        self.field[self.curPos[0] + state[0]][self.curPos[1] + state[1]] = MINO_DICT[self.curMino]
                    
                    self.tSpinFlag = False
                    self.softLockFlag = False
                else:
                    self.gravityCount = DELAY_GRAVITY
                    self.lockFlag = self.Collide(self.curMino, [self.curPos[0] + 1, self.curPos[1]],
                                    self.curRot, self.curRot, False)
            except:
                pass

    def hardDrop(self):
        if self.hardDropDelay > 0 or self.clearDelay > 0:
            pass
        else:
            self.hardDropFlag = True
            self.hardDropDelay = 10

    def shadowCalc(self):
        self.posShadow = copy.deepcopy(self.curPos)
        self.rotShadow = self.curRot
        try:
            while True:
                if not self.Collide(self.curMino, [self.posShadow[0] + 1, self.posShadow[1]],
                                    self.rotShadow, self.curRot, False):
                    self.posShadow[0] += 1
                else:
                    break
        except:
            pass
    
    def gravityDrop(self):
        if self.gravityCount == 0:
            self.lockFlag = False
            self.softDrop()
            if self.lockFlag == True:
                self.softDropFlag = True
                self.lockFlag = False
    
    def processDrop(self):
        if self.softDropFlag or self.hardDropFlag:
            self.lineClearFlag = True

        if self.hardDropFlag:
            for state in MINO_STATE[self.curMino][self.curRot]:
                self.field[self.curPos[0] + state[0]][self.curPos[1] + state[1]] = 0

            for state in MINO_STATE[self.curMino][self.curRot]:
                self.field[self.posShadow[0] + state[0]][self.posShadow[1] + state[1]] = MINO_DICT[self.curMino]

            for state in MINO_STATE[self.curMino][self.curRot]:
                self.ghostField[self.posShadow[0] + state[0]][self.posShadow[1] + state[1]] = MINO_DICT[self.curMino]

            self.hardDropFlag = False
            self.softDropFlag = False

        if self.softDropFlag:
            for state in MINO_STATE[self.curMino][self.curRot]:
                self.field[self.curPos[0] + state[0]][self.curPos[1] + state[1]] = MINO_DICT[self.curMino]
                self.ghostField[self.curPos[0] + state[0]][self.curPos[1] + state[1]] = MINO_DICT[self.curMino]

            self.hardDropFlag = False
            self.softDropFlag = False
    
    def clearLine(self):
        if self.lineClearFlag:
            lineCleared = 0
            for i in range(4, 25):
                fullLine = True
                for j in range(10):
                    fullLine = False if self.field[i][j] == 0 else fullLine
                if fullLine:
                    lineCleared += 1
                    for j in range(10):
                        self.field[i][j] = 0
                        self.ghostField[i][j] = 0
            self.lineClearFlag = False
            self.clearDelay = 0
            if lineCleared != 0:
                print(lineCleared, "Line Clear", 'Tspin' if self.tSpinFlag else '', self.comboCount, "Combo", self.BTBCount)
                self.comboCount += 1
                self.recentComboCount = self.comboCount
                if lineCleared == 4 or self.tSpinFlag:
                    self.BTBCount = self.BTBCount + 1 if self.BTBCount < 2 else 2
                else:
                    self.BTBCount = 0
                self.lastLineCleared = lineCleared
                self.totalLineCleared += lineCleared
                self.lastTSpinFlag = self.tSpinFlag
                self.lastLineClearedDelay = 60 * 1
                self.clearDelay = 10
            else:
                self.comboCount = 0
                self.NextMino()

        if self.clearDelay == 1:
            flag = False
            for i in range(24):
                for j in range(10):
                    if self.field[i][j] != 0:
                        flag = True
                        break
                if flag:
                    break
            top = i
            i = 24
            while i >= top:
                emptyLine = True
                for j in range(10):
                    emptyLine = False if self.field[i][j] != 0 else emptyLine
                if emptyLine:
                    top += 1
                    for k in range(i, 2, -1):
                        for j in range(10):
                            self.field[k][j] = self.field[k - 1][j]
                            self.ghostField[k][j] = self.ghostField[k - 1][j]
                    i += 1
                i -= 1

            self.NextMino()
    
    def zipData(self):
        data = ''
        for i in range(4, 25):
            for j in range(10):
                    data += str(self.field[i][j])
        return data
    
    def newLine(self, line):
        flag = False
        for i in range(24):
            for j in range(10):
                if self.ghostField[i][j] != 0:
                    flag = True
                    break
            if flag:
                break
        top = i
        i = max(top - line, 0)
        hole = int(time.time()) % 10
        while i < 25:
            if i < 25 - line:
                for j in range(10):
                    self.field[i][j] = self.field[top][j] if self.field[top][j] == self.ghostField[top][j] else self.field[i][j]
                    self.ghostField[i][j] = self.field[top][j] if self.field[top][j] == self.ghostField[top][j] else self.ghostField[i][j]
            else:
                for j in range(10):
                    self.field[i][j] = 0 if j == hole else 8
                    self.ghostField[i][j] = 0 if j == hole else 8
            i += 1
            top += 1