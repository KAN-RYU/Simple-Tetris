import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *
import random
import copy

#TODO divide constant into another file, make hold system, line clear

MINO = ['X', 'T', 'S', 'Z', 'L', 'J', 'O', 'I']

MINO_DICT = {'T' : 1,
             'S' : 2,
             'Z' : 3,
             'L' : 4,
             'J' : 5,
             'O' : 6,
             'I' : 7,}

IMAGE_MINO = ['',
              './Sprite/TMino.png',
              './Sprite/SMino.png',
              './Sprite/ZMino.png',
              './Sprite/LMino.png',
              './Sprite/JMino.png',
              './Sprite/OMino.png',
              './Sprite/IMino.png',]

IMAGE_NEXT_MINO = ['',
              './Sprite/NextTMino.png',
              './Sprite/NextSMino.png',
              './Sprite/NextZMino.png',
              './Sprite/NextLMino.png',
              './Sprite/NextJMino.png',
              './Sprite/NextOMino.png',
              './Sprite/NextIMino.png',]

IMAGE_BLOCK = ['',
               './Sprite/TBlock.png',
               './Sprite/SBlock.png',
               './Sprite/ZBlock.png',
               './Sprite/LBlock.png',
               './Sprite/JBlock.png',
               './Sprite/OBlock.png',
               './Sprite/IBlock.png',]

IMAGE_SHADOW = ['',
                './Sprite/TMino_shadow.png',
                './Sprite/SMino_shadow.png',
                './Sprite/ZMino_shadow.png',
                './Sprite/LMino_shadow.png',
                './Sprite/JMino_shadow.png',
                './Sprite/OMino_shadow.png',
                './Sprite/IMino_shadow.png',]

BACKGROUND = './Sprite/Background.png'
MINO_STATE = {'T' : [((-1,  0), ( 0, -1), ( 0,  0), ( 0,  1)),
                     ((-1,  0), ( 0,  0), ( 0,  1), ( 1,  0)),
                     (( 0, -1), ( 0,  0), ( 0,  1), ( 1,  0)),
                     ((-1,  0), ( 0, -1), ( 0,  0), ( 1,  0))],
              'S' : [((-1,  0), (-1,  1), ( 0, -1), ( 0,  0)),
                     ((-1,  0), ( 0,  0), ( 0,  1), ( 1,  1)),
                     (( 0,  0), ( 0,  1), ( 1, -1), ( 1,  0)),
                     ((-1, -1), ( 0, -1), ( 0,  0), ( 1,  0))],
              'Z' : [((-1, -1), (-1,  0), ( 0,  0), ( 0,  1)),
                     ((-1,  1), ( 0,  0), ( 0,  1), ( 1,  0)),
                     (( 0, -1), ( 0,  0), ( 1,  0), ( 1,  1)),
                     ((-1,  0), ( 0, -1), ( 0,  0), ( 1, -1))],
              'L' : [((-1,  1), ( 0, -1), ( 0,  0), ( 0,  1)),
                     ((-1,  0), ( 0,  0), ( 1,  0), ( 1,  1)),
                     (( 0, -1), ( 0,  0), ( 0,  1), ( 1, -1)),
                     ((-1, -1), (-1,  0), ( 0,  0), ( 1,  0))],
              'J' : [((-1, -1), ( 0, -1), ( 0,  0), ( 0,  1)),
                     ((-1,  0), (-1,  1), ( 0,  0), ( 1,  0)),
                     (( 0, -1), ( 0,  0), ( 0,  1), ( 1,  1)),
                     ((-1,  0), ( 0,  0), ( 1,  0), ( 1, -1))],
              'O' : [((-1,  0), (-1,  1), ( 0,  0), ( 0,  1)),
                     ((-1,  0), (-1,  1), ( 0,  0), ( 0,  1)),
                     ((-1,  0), (-1,  1), ( 0,  0), ( 0,  1)),
                     ((-1,  0), (-1,  1), ( 0,  0), ( 0,  1))],
              'I' : [(( 0, -1), ( 0,  0), ( 0,  1), ( 0,  2)),
                     ((-1,  1), ( 0,  1), ( 1,  1), ( 2,  1)),
                     (( 1, -1), ( 1,  0), ( 1,  1), ( 1,  2)),
                     ((-1,  0), ( 0,  0), ( 1,  0), ( 2,  0))],}
WALL_KICK = {'X' : [[(), ((0, 0), (0, -1), (-1, -1), (2, 0), (2, -1)), (), ((0, 0), (0, 1), (-1, 1), (2, 0), (2, 1))],
                    [((0, 0), (0, 1), (1, 1), (-2, 0), (-2, 1)), (), ((0, 0), (0, 1), (1, 1), (-2, 0), (-2, 1)), ()],
                    [(), ((0, 0), (0, -1), (-1, -1), (2, 0), (2, -1)), (), ((0, 0), (0, 1), (-1, 1), (2, 0), (2, 1))],
                    [((0, 0), (0, -1), (1, -1), (-2, 0), (-2, -1)), (), ((0, 0), (0, -1), (1, -1), (-2, 0), (-2, -1)), ()]],
             'I' : [[(), ((0, 0), (0, -2), (0, 1), (1, -2), (-2, 1)), (), ((0, 0), (0, -1), (0, 2), (-2, -1), (1, 2))],
                    [((0, 0), (0, 2), (0, -1), (1, -2), (2, -1)), (), ((0,0), (0, -1), (0, 2), (-2, 1), (1, 2)), ()],
                    [(), ((0,0), (0, 1), (0, -2), (-2, -1), (1, -2)), (), ((0, 0), (0, 2), (0, -1), (1, -2), (2, -1))],
                    [((0,0), (0, 1), (0, -2), (-2, -1), (1, -2)), (), ((0, 0), (0, -2), (0, 1), (1, -2), (-2, 1)), ()]]}
SHADOW_ROTATION = {0 : (  0, (0, 0)),
                   1 : (270, (0, 1)),
                   2 : (180, (1, 0)),
                   3 : ( 90, (0, 0))}
SHADOW_ROTATION_I = {0 : (  0, (1, 0)),
                     1 : (270, (0, 2)),
                     2 : (180, (2, 0)),
                     3 : ( 90, (0, 1))}
DELAY_V = 4
def NextMinoQueue():
    nextMinoQueue = ['T', 'S', 'Z', 'L', 'J', 'O', 'I']
    return random.sample(nextMinoQueue, 7)

if __name__ == "__main__":
    pygame.init()

    size = [1280, 720]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Simple Tetris")

    done = False
    clock = pygame.time.Clock()

    imageBackground = pygame.image.load(BACKGROUND)
    imageMino = ['']
    for i in range(1, 8):
        imageMino.append(pygame.image.load(IMAGE_MINO[i]))
    imageNextMino = ['']
    for i in range(1, 8):
        imageNextMino.append(pygame.image.load(IMAGE_NEXT_MINO[i]))
    imageBlock = ['']
    for i in range(1, 8):
        imageBlock.append(pygame.image.load(IMAGE_BLOCK[i]))
    imageShadow = ['']
    for i in range(1, 8):
        imageShadow.append(pygame.image.load(IMAGE_SHADOW[i]))

    field = []
    for i in range(25):
        field.append([0]*12)

    ghostField = []
    for i in range(25):
        ghostField.append([0]*12)
    
    for i in range(25):
        field[i][10] = 8
        field[i][11] = 8
        ghostField[i][10] = 8
        ghostField[i][11] = 8

    random.seed(42)
    minoQueue = NextMinoQueue()
    for i in NextMinoQueue():
        minoQueue.append(i)

    def NextMino():
        curMino = minoQueue.pop(0)
        curPos = [0, 0]
        curRot = 0
        if curMino == 'I':
            curPos = [4, 4]
        else:
            curPos = [5, 4]
        for state in MINO_STATE[curMino][curRot]:
            field[curPos[0] + state[0]][curPos[1] + state[1]] = MINO_DICT[curMino]
        return curMino, curPos, curRot

    def Collide(mino, pos, rot, newrot, kick):
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
                    collideFlag = collideFlag and (ghostField[newPos[0] + state[0]][newPos[1] + state[1]] == 0)
                if collideFlag:
                    return newPos, newrot
            return pos, rot
        else:
            for state in MINO_STATE[mino][rot]:
                if not mino == 'I' and pos[1] + state[1] < 0:
                    collideFlag = False
                collideFlag = collideFlag and (ghostField[pos[0] + state[0]][pos[1] + state[1]] == 0)

            return not collideFlag

    curMino, curPos, curRot = NextMino()
    curHold = 0
    moveDelay = 0
    softDropDelay = 0
    hardDropDelay = 0
    clearDelay = 0
    lineClearFlag = False
    spinCWDelay = False
    spinCCWDelay = False
    holdDelay = False
    softDropFlag = False
    hardDropFlag = False

    while not done:

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        #Processing key input
        #Shift movement
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            if moveDelay > 2 or clearDelay > 0:
                pass
            else:
                try:
                    if moveDelay == 0:
                        moveDelay = 7
                    else :
                        moveDelay = DELAY_V
                    if not Collide(curMino, [curPos[0], curPos[1] - 1], curRot, curRot, False):
                        for state in MINO_STATE[curMino][curRot]:
                            field[curPos[0] + state[0]][curPos[1] + state[1]] = 0

                        curPos[1] = curPos[1] - 1

                        for state in MINO_STATE[curMino][curRot]:
                            field[curPos[0] + state[0]][curPos[1] + state[1]] = MINO_DICT[curMino]
                except:
                    pass

        elif pressed[pygame.K_d]:
            if moveDelay > 2 or clearDelay > 0:
                pass
            else:
                try:
                    if moveDelay == 0:
                        moveDelay = 7
                    else :
                        moveDelay = DELAY_V
                    if not Collide(curMino, [curPos[0], curPos[1] + 1], curRot, curRot, False):
                        for state in MINO_STATE[curMino][curRot]:
                            field[curPos[0] + state[0]][curPos[1] + state[1]] = 0

                        curPos[1] += 1

                        for state in MINO_STATE[curMino][curRot]:
                            field[curPos[0] + state[0]][curPos[1] + state[1]] = MINO_DICT[curMino]
                except:
                    pass
        
        elif not pressed[pygame.K_k] or not pressed[pygame.K_d]:
            moveDelay = 0

        #Spin Movement
        if pressed[pygame.K_j]:
            if spinCWDelay or clearDelay > 0:
                pass
            else:
                try:
                    spinCWDelay = True
                    newPos, newRot =  Collide(curMino, curPos, curRot, (curRot + 1) % 4, True)
                    for state in MINO_STATE[curMino][curRot]:
                            field[curPos[0] + state[0]][curPos[1] + state[1]] = 0

                    curPos = copy.deepcopy(newPos)
                    curRot = newRot

                    for state in MINO_STATE[curMino][curRot]:
                        field[curPos[0] + state[0]][curPos[1] + state[1]] = MINO_DICT[curMino]
                except:
                    pass
                        
        if not pressed[pygame.K_j]:
            spinCWDelay = False
        
        if pressed[pygame.K_l]:
            if spinCCWDelay or clearDelay > 0:
                pass
            else:
                try:
                    spinCCWDelay = True
                    newPos, newRot =  Collide(curMino, curPos, curRot, (curRot - 1) % 4, True)
                    for state in MINO_STATE[curMino][curRot]:
                            field[curPos[0] + state[0]][curPos[1] + state[1]] = 0

                    curPos = copy.deepcopy(newPos)
                    curRot = newRot

                    for state in MINO_STATE[curMino][curRot]:
                        field[curPos[0] + state[0]][curPos[1] + state[1]] = MINO_DICT[curMino]
                except:
                    pass
                        
        if not pressed[pygame.K_l]:
            spinCCWDelay = False
        
        #Hold Function
        if pressed[pygame.K_k]:
            if holdDelay or clearDelay > 0:
                pass
            else:
                holdDelay = True
                if curHold == 0:
                    curHold = curMino
                    for state in MINO_STATE[curMino][curRot]:
                        field[curPos[0] + state[0]][curPos[1] + state[1]] = 0

                    curMino, curPos, curRot = NextMino()
                else:
                    for state in MINO_STATE[curMino][curRot]:
                        field[curPos[0] + state[0]][curPos[1] + state[1]] = 0
                    tmp = curMino
                    curMino = curHold
                    curHold = tmp
                    curRot = 0
                    if curMino == 'I':
                        curPos = [4, 4]
                    else:
                        curPos = [5, 4]
                    for state in MINO_STATE[curMino][curRot]:
                        field[curPos[0] + state[0]][curPos[1] + state[1]] = MINO_DICT[curMino]

        #Soft Drop
        if pressed[pygame.K_s]:
            if softDropDelay > 0 or clearDelay > 0:
                pass
            else:
                try:
                    softDropDelay = DELAY_V
                    if not Collide(curMino, [curPos[0] + 1, curPos[1]], curRot, curRot, False):
                        for state in MINO_STATE[curMino][curRot]:
                            field[curPos[0] + state[0]][curPos[1] + state[1]] = 0

                        curPos[0] += 1

                        for state in MINO_STATE[curMino][curRot]:
                            field[curPos[0] + state[0]][curPos[1] + state[1]] = MINO_DICT[curMino]
                    else:
                        softDropFlag = True
                except:
                    softDropFlag = True
        
        if not pressed[pygame.K_s]:
            softDropDelay = 0
        
        #Hard Drop
        if pressed[pygame.K_SPACE]:
            if hardDropDelay > 0 or clearDelay > 0:
                pass
            else:
                hardDropFlag = True
                hardDropDelay = 10
        
        if not pressed[pygame.K_SPACE]:
            hardDropDelay = 0

        #Draw Screen
        screen.blit(imageBackground, (0, 0))

        posShadow = copy.deepcopy(curPos)
        rotShadow = curRot
        try:
            while True:
                if not Collide(curMino, [posShadow[0] + 1, posShadow[1]], rotShadow, curRot, False):
                    posShadow[0] += 1
                else:
                    break
        except:
            pass
        finally:
            if clearDelay == 0:
                if curMino == 'I':
                    screen.blit(pygame.transform.rotate(imageShadow[MINO_DICT[curMino]], SHADOW_ROTATION[curRot][0]),
                                (180 + 30 * (posShadow[1] - 1 + SHADOW_ROTATION_I[curRot][1][1]),
                                50 + 30 * (posShadow[0] - 5 + SHADOW_ROTATION_I[curRot][1][0])))
                elif curMino == 'O':
                    screen.blit(imageShadow[MINO_DICT[curMino]], (180 + 30 * (posShadow[1] - 0), 50 + 30 * (posShadow[0] - 5)))
                else:
                    screen.blit(pygame.transform.rotate(imageShadow[MINO_DICT[curMino]], SHADOW_ROTATION[curRot][0]),
                                (180 + 30 * (posShadow[1] - 1 + SHADOW_ROTATION[curRot][1][1]),
                                50 + 30 * (posShadow[0] - 5 + SHADOW_ROTATION[curRot][1][0])))
        if softDropFlag or hardDropFlag:
            holdDelay = False
            lineClearFlag = True
            
        if hardDropFlag:
            for state in MINO_STATE[curMino][curRot]:
                field[curPos[0] + state[0]][curPos[1] + state[1]] = 0

            for state in MINO_STATE[curMino][curRot]:
                field[posShadow[0] + state[0]][posShadow[1] + state[1]] = MINO_DICT[curMino]

            for state in MINO_STATE[curMino][curRot]:
                ghostField[posShadow[0] + state[0]][posShadow[1] + state[1]] = MINO_DICT[curMino]

            hardDropFlag = False
            softDropFlag = False
        
        if softDropFlag:
            for state in MINO_STATE[curMino][curRot]:
                field[curPos[0] + state[0]][curPos[1] + state[1]] = MINO_DICT[curMino]
                ghostField[curPos[0] + state[0]][curPos[1] + state[1]] = MINO_DICT[curMino]
            
            hardDropFlag = False
            softDropFlag = False
        
        if lineClearFlag:
            lineCleared = 0
            for i in range(4, 25):
                fullLine = True
                for j in range(10):
                    fullLine = False if field[i][j] == 0 else fullLine
                if fullLine:
                    lineCleared += 1
                    for j in range(10):
                        field[i][j] = 0
                        ghostField[i][j] = 0
            lineClearFlag = False
            clearDelay = 0
            if lineCleared != 0:
                print(lineCleared, "Line Clear")
                clearDelay = 10
            else:
                curMino, curPos, curRot = NextMino()
        
        if clearDelay == 1:
            flag = False
            for i in range(24):
                for j in range(10):
                    if field[i][j] != 0:
                        flag = True
                        break
                if flag:
                    break
            top = i
            i = 24
            while i >= top:
                emptyLine = True
                for j in range(10):
                    emptyLine = False if field[i][j] != 0 else emptyLine
                if emptyLine:
                    top += 1
                    for k in range(i, 2, -1):
                        for j in range(10):
                            field[k][j] = field[k - 1][j]
                            ghostField[k][j] = ghostField[k - 1][j]
                    i += 1
                i -= 1
                
            curMino, curPos, curRot = NextMino()
                        

        if len(minoQueue) < 6:
            for i in NextMinoQueue():
                minoQueue.append(i)

        for i in range(5):
            screen.blit(imageNextMino[MINO_DICT[minoQueue[i]]], (510 + 10, 110 + 10 + 90 * i))
        
        if curHold != 0:
            size = imageMino[MINO_DICT[curHold]].get_rect().size
            screen.blit(imageMino[MINO_DICT[curHold]], (100 - size[0] // 2, 175 - size[1] // 2))
            

        for i in range(4, 25):
            for j in range(10):
                if field[i][j] != 0:
                    screen.blit(imageBlock[field[i][j]], (180 + 30 * j, 50 + 30 * (i - 4)))

        moveDelay = moveDelay - 1 if moveDelay > 0 else 0
        hardDropDelay = hardDropDelay - 1 if hardDropDelay > 0 else 0
        softDropDelay = softDropDelay - 1 if softDropDelay > 0 else 0
        clearDelay = clearDelay - 1 if clearDelay > 0 else 0
        # print(curMino, curPos, curRot, moveDelay, softDropDelay, hardDropDelay)
        pygame.display.flip()

    pygame.quit()

