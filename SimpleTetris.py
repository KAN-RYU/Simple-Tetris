import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *
import random
import copy
from SimpleTetrisConstant import *
from SimpleTetrisGame import SimpleTetrisGame
from SimpleTetrisHelper import *

if __name__ == "__main__":
    pygame.init()

    size = [1280, 720]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Simple Tetris")

    done = False
    clock = pygame.time.Clock()

    imageBackground = pygame.image.load(resource_path(BACKGROUND))
    imageMino = ['']
    for i in range(1, 8):
        imageMino.append(pygame.image.load(resource_path(IMAGE_MINO[i])))
    imageNextMino = ['']
    for i in range(1, 8):
        imageNextMino.append(pygame.image.load(resource_path(IMAGE_NEXT_MINO[i])))
    imageBlock = ['']
    for i in range(1, 8):
        imageBlock.append(pygame.image.load(resource_path(IMAGE_BLOCK[i])))
    imageShadow = ['']
    for i in range(1, 8):
        imageShadow.append(pygame.image.load(resource_path(IMAGE_SHADOW[i])))
    
    random.seed(42)
    curGame = SimpleTetrisGame()

    while not done:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        #Processing key input
        #Shift movement
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            if curGame.moveDelay > 2 or curGame.clearDelay > 0:
                pass
            else:
                try:
                    if curGame.moveDelay == 0:
                        curGame.moveDelay = DELAY_FIRST
                    else :
                        curGame.moveDelay = DELAY_V
                    if not curGame.Collide(curGame.curMino, [curGame.curPos[0], curGame.curPos[1] - 1],
                                           curGame.curRot, curGame.curRot, False):
                        for state in MINO_STATE[curGame.curMino][curGame.curRot]:
                            curGame.field[curGame.curPos[0] + state[0]][curGame.curPos[1] + state[1]] = 0

                        curGame.curPos[1] -= 1

                        for state in MINO_STATE[curGame.curMino][curGame.curRot]:
                            curGame.field[curGame.curPos[0] + state[0]][curGame.curPos[1] + state[1]] = MINO_DICT[curGame.curMino]
                except:
                    pass

        elif pressed[pygame.K_d]:
            if curGame.moveDelay > 2 or curGame.clearDelay > 0:
                pass
            else:
                try:
                    if curGame.moveDelay == 0:
                        curGame.moveDelay = DELAY_FIRST
                    else :
                        curGame.moveDelay = DELAY_V
                    if not curGame.Collide(curGame.curMino, [curGame.curPos[0], curGame.curPos[1] + 1], 
                                           curGame.curRot, curGame.curRot, False):
                        for state in MINO_STATE[curGame.curMino][curGame.curRot]:
                            curGame.field[curGame.curPos[0] + state[0]][curGame.curPos[1] + state[1]] = 0

                        curGame.curPos[1] += 1

                        for state in MINO_STATE[curGame.curMino][curGame.curRot]:
                            curGame.field[curGame.curPos[0] + state[0]][curGame.curPos[1] + state[1]] = MINO_DICT[curGame.curMino]
                except:
                    pass

        elif not pressed[pygame.K_k] or not pressed[pygame.K_d]:
            curGame.moveDelay = 0

        #Spin Movement
        if pressed[pygame.K_j]:
            if curGame.spinCWDelay or curGame.clearDelay > 0:
                pass
            else:
                try:
                    curGame.spinCWDelay = True
                    newPos, newRot =  curGame.Collide(curGame.curMino, curGame.curPos, curGame.curRot, 
                                                      (curGame.curRot + 1) % 4, True)
                    for state in MINO_STATE[curGame.curMino][curGame.curRot]:
                            curGame.field[curGame.curPos[0] + state[0]][curGame.curPos[1] + state[1]] = 0

                    curGame.curPos = copy.deepcopy(newPos)
                    curGame.curRot = newRot

                    for state in MINO_STATE[curGame.curMino][curGame.curRot]:
                        curGame.field[curGame.curPos[0] + state[0]][curGame.curPos[1] + state[1]] = MINO_DICT[curGame.curMino]
                except:
                    pass

        if not pressed[pygame.K_j]:
            curGame.spinCWDelay = False

        if pressed[pygame.K_l]:
            if curGame.spinCCWDelay or curGame.clearDelay > 0:
                pass
            else:
                try:
                    curGame.spinCCWDelay = True
                    newPos, newRot =  curGame.Collide(curGame.curMino, curGame.curPos, curGame.curRot, 
                                                      (curGame.curRot - 1) % 4, True)
                    for state in MINO_STATE[curGame.curMino][curGame.curRot]:
                            curGame.field[curGame.curPos[0] + state[0]][curGame.curPos[1] + state[1]] = 0

                    curGame.curPos = copy.deepcopy(newPos)
                    curGame.curRot = newRot

                    for state in MINO_STATE[curGame.curMino][curGame.curRot]:
                        curGame.field[curGame.curPos[0] + state[0]][curGame.curPos[1] + state[1]] = MINO_DICT[curGame.curMino]
                except:
                    pass

        if not pressed[pygame.K_l]:
            curGame.spinCCWDelay = False

        #Hold Function
        if pressed[pygame.K_k]:
            if curGame.holdFlag or curGame.clearDelay > 0:
                pass
            else:
                curGame.holdFlag = True
                if curGame.curHold == 0:
                    curGame.curHold = curGame.curMino
                    for state in MINO_STATE[curGame.curMino][curGame.curRot]:
                        curGame.field[curGame.curPos[0] + state[0]][curGame.curPos[1] + state[1]] = 0

                    curGame.NextMino()
                    curGame.holdFlag = True
                else:
                    for state in MINO_STATE[curGame.curMino][curGame.curRot]:
                        curGame.field[curGame.curPos[0] + state[0]][curGame.curPos[1] + state[1]] = 0
                    tmp = curGame.curMino
                    curGame.curMino = curGame.curHold
                    curGame.curHold = tmp
                    curGame.curRot = 0
                    if curGame.curMino == 'I':
                        curGame.curPos = [4, 4]
                    else:
                        curGame.curPos = [5, 4]
                    for state in MINO_STATE[curGame.curMino][curGame.curRot]:
                        curGame.field[curGame.curPos[0] + state[0]][curGame.curPos[1] + state[1]] = MINO_DICT[curGame.curMino]

        #Soft Drop
        if pressed[pygame.K_s]:
            if curGame.softDropDelay > 0 or curGame.clearDelay > 0:
                pass
            else:
                try:
                    curGame.softDropDelay = DELAY_V
                    if not curGame.Collide(curGame.curMino, [curGame.curPos[0] + 1, curGame.curPos[1]], 
                                           curGame.curRot, curGame.curRot, False):
                        for state in MINO_STATE[curGame.curMino][curGame.curRot]:
                            curGame.field[curGame.curPos[0] + state[0]][curGame.curPos[1] + state[1]] = 0

                        curGame.curPos[0] += 1

                        for state in MINO_STATE[curGame.curMino][curGame.curRot]:
                            curGame.field[curGame.curPos[0] + state[0]][curGame.curPos[1] + state[1]] = MINO_DICT[curGame.curMino]
                    else:
                        curGame.softDropFlag = True
                except:
                    curGame.softDropFlag = True

        if not pressed[pygame.K_s]:
            curGame.softDropDelay = 0

        #Hard Drop
        if pressed[pygame.K_SPACE]:
            if curGame.hardDropDelay > 0 or curGame.clearDelay > 0:
                pass
            else:
                curGame.hardDropFlag = True
                curGame.hardDropDelay = 10

        if not pressed[pygame.K_SPACE]:
            curGame.hardDropDelay = 0

        #Draw Screen
        screen.blit(imageBackground, (0, 0))

        posShadow = copy.deepcopy(curGame.curPos)
        rotShadow = curGame.curRot
        try:
            while True:
                if not curGame.Collide(curGame.curMino, [posShadow[0] + 1, posShadow[1]],
                                       rotShadow, curGame.curRot, False):
                    posShadow[0] += 1
                else:
                    break
        except:
            pass
        finally:
            if curGame.clearDelay == 0:
                if curGame.curMino == 'I':
                    screen.blit(pygame.transform.rotate(imageShadow[MINO_DICT[curGame.curMino]], SHADOW_ROTATION[curGame.curRot][0]),
                                (180 + 30 * (posShadow[1] - 1 + SHADOW_ROTATION_I[curGame.curRot][1][1]),
                                50 + 30 * (posShadow[0] - 5 + SHADOW_ROTATION_I[curGame.curRot][1][0])))
                elif curGame.curMino == 'O':
                    screen.blit(imageShadow[MINO_DICT[curGame.curMino]], (180 + 30 * (posShadow[1] - 0), 50 + 30 * (posShadow[0] - 5)))
                else:
                    screen.blit(pygame.transform.rotate(imageShadow[MINO_DICT[curGame.curMino]], SHADOW_ROTATION[curGame.curRot][0]),
                                (180 + 30 * (posShadow[1] - 1 + SHADOW_ROTATION[curGame.curRot][1][1]),
                                50 + 30 * (posShadow[0] - 5 + SHADOW_ROTATION[curGame.curRot][1][0])))
        if curGame.softDropFlag or curGame.hardDropFlag:
            curGame.lineClearFlag = True

        if curGame.hardDropFlag:
            for state in MINO_STATE[curGame.curMino][curGame.curRot]:
                curGame.field[curGame.curPos[0] + state[0]][curGame.curPos[1] + state[1]] = 0

            for state in MINO_STATE[curGame.curMino][curGame.curRot]:
                curGame.field[posShadow[0] + state[0]][posShadow[1] + state[1]] = MINO_DICT[curGame.curMino]

            for state in MINO_STATE[curGame.curMino][curGame.curRot]:
                curGame.ghostField[posShadow[0] + state[0]][posShadow[1] + state[1]] = MINO_DICT[curGame.curMino]

            curGame.hardDropFlag = False
            curGame.softDropFlag = False

        if curGame.softDropFlag:
            for state in MINO_STATE[curGame.curMino][curGame.curRot]:
                curGame.field[curGame.curPos[0] + state[0]][curGame.curPos[1] + state[1]] = MINO_DICT[curGame.curMino]
                curGame.ghostField[curGame.curPos[0] + state[0]][curGame.curPos[1] + state[1]] = MINO_DICT[curGame.curMino]

            curGame.hardDropFlag = False
            curGame.softDropFlag = False

        if curGame.lineClearFlag:
            lineCleared = 0
            for i in range(4, 25):
                fullLine = True
                for j in range(10):
                    fullLine = False if curGame.field[i][j] == 0 else fullLine
                if fullLine:
                    lineCleared += 1
                    for j in range(10):
                        curGame.field[i][j] = 0
                        curGame.ghostField[i][j] = 0
            curGame.lineClearFlag = False
            curGame.clearDelay = 0
            if lineCleared != 0:
                print(lineCleared, "Line Clear")
                curGame.clearDelay = 10
            else:
                curGame.NextMino()

        if curGame.clearDelay == 1:
            flag = False
            for i in range(24):
                for j in range(10):
                    if curGame.field[i][j] != 0:
                        flag = True
                        break
                if flag:
                    break
            top = i
            i = 24
            while i >= top:
                emptyLine = True
                for j in range(10):
                    emptyLine = False if curGame.field[i][j] != 0 else emptyLine
                if emptyLine:
                    top += 1
                    for k in range(i, 2, -1):
                        for j in range(10):
                            curGame.field[k][j] = curGame.field[k - 1][j]
                            curGame.ghostField[k][j] = curGame.ghostField[k - 1][j]
                    i += 1
                i -= 1

            curGame.NextMino()


        if len(curGame.minoQueue) < 6:
            for i in curGame.NextMinoQueue():
                curGame.minoQueue.append(i)

        for i in range(5):
            screen.blit(imageNextMino[MINO_DICT[curGame.minoQueue[i]]], (510 + 10, 110 + 10 + 90 * i))

        if curGame.curHold != 0:
            size = imageMino[MINO_DICT[curGame.curHold]].get_rect().size
            screen.blit(imageMino[MINO_DICT[curGame.curHold]], (100 - size[0] // 2, 175 - size[1] // 2))

        if curGame.holdFlag:
            s = pygame.Surface((130, 130), pygame.SRCALPHA)
            s.fill((0, 0, 0, 128))
            screen.blit(s, (35, 110))

        for i in range(4, 25):
            for j in range(10):
                if curGame.field[i][j] != 0:
                    screen.blit(imageBlock[curGame.field[i][j]], (180 + 30 * j, 50 + 30 * (i - 4)))

        curGame.tick()
        # print(curGame.curMino, curGame.curPos, curGame.curRot, curGame.moveDelay, curGame.softDropDelay, curGame.hardDropDelay)
        pygame.display.flip()

    pygame.quit()

