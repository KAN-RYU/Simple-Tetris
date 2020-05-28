import random
import copy
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

        self.posShadow = [0, 0]
        self.rotShadow = 0

        self.lastLineCleared = 0
        self.lastLineClearedDelay = 0

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
                print(lineCleared, "Line Clear")
                self.lastLineCleared = lineCleared
                self.lastLineClearedDelay = 60 * 1
                self.clearDelay = 10
            else:
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

        if len(self.minoQueue) < 6:
                for i in self.NextMinoQueue():
                    self.minoQueue.append(i)

        self.moveDelay = self.moveDelay - 1 if self.moveDelay > 0 else 0
        self.hardDropDelay = self.hardDropDelay - 1 if self.hardDropDelay > 0 else 0
        self.softDropDelay = self.softDropDelay - 1 if self.softDropDelay > 0 else 0
        self.clearDelay = self.clearDelay - 1 if self.clearDelay > 0 else 0
        self.lastLineClearedDelay = self.lastLineClearedDelay - 1 if self.lastLineClearedDelay - 1 > 0 else 0

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
            self.holdFlag = True
            if self.curHold == 0:
                self.curHold = self.curMino
                for state in MINO_STATE[self.curMino][self.curRot]:
                    self.field[self.curPos[0] + state[0]][self.curPos[1] + state[1]] = 0

                self.NextMino()
                self.holdFlag = True
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
                    self.field[self.curPos[0] + state[0]][self.curPos[1] + state[1]] = MINO_DICT[self.curMino]

    def softDrop(self):
        if self.softDropDelay > 0 or self.clearDelay > 0:
            pass
        else:
            try:
                self.softDropDelay = DELAY_V
                if not self.Collide(self.curMino, [self.curPos[0] + 1, self.curPos[1]],
                                    self.curRot, self.curRot, False):
                    for state in MINO_STATE[self.curMino][self.curRot]:
                        self.field[self.curPos[0] + state[0]][self.curPos[1] + state[1]] = 0

                    self.curPos[0] += 1

                    for state in MINO_STATE[self.curMino][self.curRot]:
                        self.field[self.curPos[0] + state[0]][self.curPos[1] + state[1]] = MINO_DICT[self.curMino]
                else:
                    self.softDropFlag = True
            except:
                self.softDropFlag = True

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