import pygame
from pygame.locals import *
import random
import copy

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
MINO_STATE = {}
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
    imageBlock = ['']
    for i in range(1, 8):
        imageBlock.append(pygame.image.load(IMAGE_BLOCK[i]))
    imageShadow = ['']
    for i in range(1, 8):
        imageShadow.append(pygame.image.load(IMAGE_SHADOW[i]))

    field = []
    for i in range(25):
        field.append([0]*10)

    ghostField = []
    for i in range(25):
        ghostField.append([0]*10)

    random.seed(42)
    minoQueue = NextMinoQueue()
    for i in NextMinoQueue():
        minoQueue.append(i)

    def NextMino():
        curMino = minoQueue.pop(0)
        curPos = [0, 0]
        curRot = 0
        if curMino == 'T':
            field[4][4] = MINO_DICT[curMino]
            field[5][3] = MINO_DICT[curMino]
            field[5][4] = MINO_DICT[curMino]
            field[5][5] = MINO_DICT[curMino]
            curPos = [5, 4]
        elif curMino == 'S':
            field[4][4] = MINO_DICT[curMino]
            field[4][5] = MINO_DICT[curMino]
            field[5][3] = MINO_DICT[curMino]
            field[5][4] = MINO_DICT[curMino]
            curPos = [5, 4]
        elif curMino == 'Z':
            field[4][3] = MINO_DICT[curMino]
            field[4][4] = MINO_DICT[curMino]
            field[5][4] = MINO_DICT[curMino]
            field[5][5] = MINO_DICT[curMino]
            curPos = [5, 4]
        elif curMino == 'L':
            field[4][5] = MINO_DICT[curMino]
            field[5][3] = MINO_DICT[curMino]
            field[5][4] = MINO_DICT[curMino]
            field[5][5] = MINO_DICT[curMino]
            curPos = [5, 4]
        elif curMino == 'J':
            field[4][3] = MINO_DICT[curMino]
            field[5][3] = MINO_DICT[curMino]
            field[5][4] = MINO_DICT[curMino]
            field[5][5] = MINO_DICT[curMino]
            curPos = [5, 4]
        elif curMino == 'O':
            field[4][4] = MINO_DICT[curMino]
            field[4][5] = MINO_DICT[curMino]
            field[5][4] = MINO_DICT[curMino]
            field[5][5] = MINO_DICT[curMino]
            curPos = [5, 4]
        elif curMino == 'I':
            field[4][3] = MINO_DICT[curMino]
            field[4][4] = MINO_DICT[curMino]
            field[4][5] = MINO_DICT[curMino]
            field[4][6] = MINO_DICT[curMino]
            curPos = [4, 4]

        return curMino, curPos, curRot

    def Collide(block, pos, rot):
        if pos[0] > 25 or pos [1] < 0 or pos[1] > 9:
            raise
        if block == 'T':
            if pos[1] - 1 < 0:
                return True
            return  not (ghostField[pos[0]-1][pos[1]] == 0 and
                         ghostField[pos[0]][pos[1]-1] == 0 and
                         ghostField[pos[0]][pos[1]] == 0 and
                         ghostField[pos[0]][pos[1]+1] == 0)
        elif block == 'S':
            if pos[1] - 1 < 0:
                return True
            return  not (ghostField[pos[0]-1][pos[1]] == 0 and
                         ghostField[pos[0]-1][pos[1]+1] == 0 and
                         ghostField[pos[0]][pos[1]-1] == 0 and
                         ghostField[pos[0]][pos[1]] == 0)
        elif block == 'Z':
            if pos[1] - 1 < 0:
                return True
            return  not (ghostField[pos[0]-1][pos[1]] == 0 and
                         ghostField[pos[0]-1][pos[1]-1] == 0 and
                         ghostField[pos[0]][pos[1]] == 0 and
                         ghostField[pos[0]][pos[1]+1] == 0)
        elif block == 'L':
            if pos[1] - 1 < 0:
                return True
            return  not (ghostField[pos[0]-1][pos[1]+1] == 0 and
                         ghostField[pos[0]][pos[1]-1] == 0 and
                         ghostField[pos[0]][pos[1]] == 0 and
                         ghostField[pos[0]][pos[1]+1] == 0)
        elif block == 'J':
            if pos[1] - 1 < 0:
                return True
            return  not (ghostField[pos[0]-1][pos[1]-1] == 0 and
                         ghostField[pos[0]][pos[1]-1] == 0 and
                         ghostField[pos[0]][pos[1]] == 0 and
                         ghostField[pos[0]][pos[1]+1] == 0)
        elif block == 'O':
            return  not (ghostField[pos[0]-1][pos[1]] == 0 and
                         ghostField[pos[0]-1][pos[1]+1] == 0 and
                         ghostField[pos[0]][pos[1]] == 0 and
                         ghostField[pos[0]][pos[1]+1] == 0)
        elif block == 'I':
            if pos[1] - 1 < 0:
                return True
            return  not (ghostField[pos[0]][pos[1]-1] == 0 and
                         ghostField[pos[0]][pos[1]] == 0 and
                         ghostField[pos[0]][pos[1]+1] == 0 and
                         ghostField[pos[0]][pos[1]+2] == 0)

    curMino, curPos, curRot = NextMino()
    moveDelay = 0
    dropDelay = 0
    hardDropFlag = False
    
    
    while not done:

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        #Processing key input
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            if moveDelay > 0:
                pass
            else:
                try:
                    moveDelay = DELAY_V
                    if not Collide(curMino, [curPos[0], curPos[1] - 1], curRot):
                        if curMino == 'T':
                            field[curPos[0]-1][curPos[1]] = 0
                            field[curPos[0]][curPos[1]-1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]+1] = 0

                            curPos[1] = curPos[1] - 1 if curPos[1] > 0 else 0

                            field[curPos[0]-1][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]-1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+1] = MINO_DICT[curMino]

                        elif curMino == 'S':
                            field[curPos[0]-1][curPos[1]] = 0
                            field[curPos[0]-1][curPos[1]+1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]-1] = 0

                            curPos[1] = curPos[1] - 1 if curPos[1] > 0 else 0

                            field[curPos[0]-1][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]-1][curPos[1]+1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]-1] = MINO_DICT[curMino]

                        elif curMino == 'Z':
                            field[curPos[0]-1][curPos[1]] = 0
                            field[curPos[0]-1][curPos[1]-1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]+1] = 0

                            curPos[1] = curPos[1] - 1 if curPos[1] > 0 else 0

                            field[curPos[0]-1][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]-1][curPos[1]-1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+1] = MINO_DICT[curMino]

                        elif curMino == 'L':
                            field[curPos[0]-1][curPos[1]+1] = 0
                            field[curPos[0]][curPos[1]-1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]+1] = 0

                            curPos[1] = curPos[1] - 1 if curPos[1] > 0 else 0

                            field[curPos[0]-1][curPos[1]+1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]-1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+1] = MINO_DICT[curMino]

                        elif curMino == 'J':
                            field[curPos[0]-1][curPos[1]-1] = 0
                            field[curPos[0]][curPos[1]-1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]+1] = 0

                            curPos[1] = curPos[1] - 1 if curPos[1] > 0 else 0

                            field[curPos[0]-1][curPos[1]-1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]-1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+1] = MINO_DICT[curMino]

                        elif curMino == 'O':
                            field[curPos[0]-1][curPos[1]] = 0
                            field[curPos[0]-1][curPos[1]+1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]+1] = 0

                            curPos[1] = curPos[1] - 1 if curPos[1] > 0 else 0

                            field[curPos[0]-1][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]-1][curPos[1]+1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+1] = MINO_DICT[curMino]

                        elif curMino == 'I':
                            field[curPos[0]][curPos[1]-1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]+1] = 0
                            field[curPos[0]][curPos[1]+2] = 0

                            curPos[1] = curPos[1] - 1 if curPos[1] > 0 else 0

                            field[curPos[0]][curPos[1]-1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+2] = MINO_DICT[curMino]
                except:
                    pass

        if pressed[pygame.K_d]:
            if moveDelay > 0:
                pass
            else:
                try:
                    moveDelay = DELAY_V
                    if not Collide(curMino, [curPos[0], curPos[1] + 1], curRot):
                        if curMino == 'T':
                            field[curPos[0]-1][curPos[1]] = 0
                            field[curPos[0]][curPos[1]-1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]+1] = 0

                            curPos[1] = curPos[1] + 1

                            field[curPos[0]-1][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]-1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+1] = MINO_DICT[curMino]

                        elif curMino == 'S':
                            field[curPos[0]-1][curPos[1]] = 0
                            field[curPos[0]-1][curPos[1]+1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]-1] = 0

                            curPos[1] = curPos[1] + 1

                            field[curPos[0]-1][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]-1][curPos[1]+1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]-1] = MINO_DICT[curMino]

                        elif curMino == 'Z':
                            field[curPos[0]-1][curPos[1]] = 0
                            field[curPos[0]-1][curPos[1]-1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]+1] = 0

                            curPos[1] = curPos[1] + 1

                            field[curPos[0]-1][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]-1][curPos[1]-1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+1] = MINO_DICT[curMino]

                        elif curMino == 'L':
                            field[curPos[0]-1][curPos[1]+1] = 0
                            field[curPos[0]][curPos[1]-1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]+1] = 0

                            curPos[1] = curPos[1] + 1

                            field[curPos[0]-1][curPos[1]+1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]-1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+1] = MINO_DICT[curMino]

                        elif curMino == 'J':
                            field[curPos[0]-1][curPos[1]-1] = 0
                            field[curPos[0]][curPos[1]-1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]+1] = 0

                            curPos[1] = curPos[1] + 1

                            field[curPos[0]-1][curPos[1]-1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]-1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+1] = MINO_DICT[curMino]

                        elif curMino == 'O':
                            field[curPos[0]-1][curPos[1]] = 0
                            field[curPos[0]-1][curPos[1]+1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]+1] = 0

                            curPos[1] = curPos[1] + 1

                            field[curPos[0]-1][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]-1][curPos[1]+1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+1] = MINO_DICT[curMino]

                        elif curMino == 'I':
                            field[curPos[0]][curPos[1]-1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]+1] = 0
                            field[curPos[0]][curPos[1]+2] = 0

                            curPos[1] = curPos[1] + 1

                            field[curPos[0]][curPos[1]-1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+2] = MINO_DICT[curMino]
                except:
                    pass

        if pressed[pygame.K_s]:
            if moveDelay > 0:
                pass
            else:
                try:
                    moveDelay = DELAY_V
                    if not Collide(curMino, [curPos[0] + 1, curPos[1]], curRot):
                        if curMino == 'T':
                            field[curPos[0]-1][curPos[1]] = 0
                            field[curPos[0]][curPos[1]-1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]+1] = 0

                            curPos[0] += 1

                            field[curPos[0]-1][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]-1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+1] = MINO_DICT[curMino]

                        elif curMino == 'S':
                            field[curPos[0]-1][curPos[1]] = 0
                            field[curPos[0]-1][curPos[1]+1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]-1] = 0

                            curPos[0] += 1

                            field[curPos[0]-1][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]-1][curPos[1]+1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]-1] = MINO_DICT[curMino]

                        elif curMino == 'Z':
                            field[curPos[0]-1][curPos[1]] = 0
                            field[curPos[0]-1][curPos[1]-1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]+1] = 0

                            curPos[0] += 1

                            field[curPos[0]-1][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]-1][curPos[1]-1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+1] = MINO_DICT[curMino]

                        elif curMino == 'L':
                            field[curPos[0]-1][curPos[1]+1] = 0
                            field[curPos[0]][curPos[1]-1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]+1] = 0

                            curPos[0] += 1

                            field[curPos[0]-1][curPos[1]+1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]-1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+1] = MINO_DICT[curMino]

                        elif curMino == 'J':
                            field[curPos[0]-1][curPos[1]-1] = 0
                            field[curPos[0]][curPos[1]-1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]+1] = 0

                            curPos[0] += 1

                            field[curPos[0]-1][curPos[1]-1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]-1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+1] = MINO_DICT[curMino]

                        elif curMino == 'O':
                            field[curPos[0]-1][curPos[1]] = 0
                            field[curPos[0]-1][curPos[1]+1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]+1] = 0

                            curPos[0] += 1

                            field[curPos[0]-1][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]-1][curPos[1]+1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+1] = MINO_DICT[curMino]

                        elif curMino == 'I':
                            field[curPos[0]][curPos[1]-1] = 0
                            field[curPos[0]][curPos[1]] = 0
                            field[curPos[0]][curPos[1]+1] = 0
                            field[curPos[0]][curPos[1]+2] = 0

                            curPos[0] += 1

                            field[curPos[0]][curPos[1]-1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+1] = MINO_DICT[curMino]
                            field[curPos[0]][curPos[1]+2] = MINO_DICT[curMino]
                except:
                    pass
        if pressed[pygame.K_SPACE]:
            if dropDelay > 0:
                pass
            else:
                hardDropFlag = True
                dropDelay = 10

        screen.blit(imageBackground, (0, 0))

        posShadow = copy.deepcopy(curPos)
        rotShadow = curRot
        try:
            while True:
                if not Collide(curMino, [posShadow[0] + 1, posShadow[1]], rotShadow):
                    posShadow[0] += 1
                else:
                    break
        except:
            pass
        finally:
            if curMino == 'T':
                screen.blit(imageShadow[MINO_DICT[curMino]], (180 + 30 * (posShadow[1] - 1), 50 + 30 * (posShadow[0] - 5)))
            elif curMino == 'S':
                screen.blit(imageShadow[MINO_DICT[curMino]], (180 + 30 * (posShadow[1] - 1), 50 + 30 * (posShadow[0] - 5)))
            elif curMino == 'Z':
                screen.blit(imageShadow[MINO_DICT[curMino]], (180 + 30 * (posShadow[1] - 1), 50 + 30 * (posShadow[0] - 5)))
            elif curMino == 'L':
                screen.blit(imageShadow[MINO_DICT[curMino]], (180 + 30 * (posShadow[1] - 1), 50 + 30 * (posShadow[0] - 5)))
            elif curMino == 'J':
                screen.blit(imageShadow[MINO_DICT[curMino]], (180 + 30 * (posShadow[1] - 1), 50 + 30 * (posShadow[0] - 5)))
            elif curMino == 'O':
                screen.blit(imageShadow[MINO_DICT[curMino]], (180 + 30 * (posShadow[1] - 0), 50 + 30 * (posShadow[0] - 5)))
            elif curMino == 'I':
                screen.blit(imageShadow[MINO_DICT[curMino]], (180 + 30 * (posShadow[1] - 1), 50 + 30 * (posShadow[0] - 4)))
            if hardDropFlag:
                if curMino == 'T':
                    field[curPos[0]-1][curPos[1]] = 0
                    field[curPos[0]][curPos[1]-1] = 0
                    field[curPos[0]][curPos[1]] = 0
                    field[curPos[0]][curPos[1]+1] = 0
                    field[posShadow[0]-1][posShadow[1]] = MINO_DICT[curMino]
                    field[posShadow[0]][posShadow[1]-1] = MINO_DICT[curMino]
                    field[posShadow[0]][posShadow[1]] = MINO_DICT[curMino]
                    field[posShadow[0]][posShadow[1]+1] = MINO_DICT[curMino]
                    ghostField[posShadow[0]-1][posShadow[1]] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]-1] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]+1] = MINO_DICT[curMino]

                elif curMino == 'S':
                    field[curPos[0]-1][curPos[1]] = 0
                    field[curPos[0]-1][curPos[1]+1] = 0
                    field[curPos[0]][curPos[1]] = 0
                    field[curPos[0]][curPos[1]-1] = 0
                    field[posShadow[0]-1][posShadow[1]] = MINO_DICT[curMino]
                    field[posShadow[0]-1][posShadow[1]+1] = MINO_DICT[curMino]
                    field[posShadow[0]][posShadow[1]] = MINO_DICT[curMino]
                    field[posShadow[0]][posShadow[1]-1] = MINO_DICT[curMino]
                    ghostField[posShadow[0]-1][posShadow[1]] = MINO_DICT[curMino]
                    ghostField[posShadow[0]-1][posShadow[1]+1] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]-1] = MINO_DICT[curMino]

                elif curMino == 'Z':
                    field[curPos[0]-1][curPos[1]] = 0
                    field[curPos[0]-1][curPos[1]-1] = 0
                    field[curPos[0]][curPos[1]] = 0
                    field[curPos[0]][curPos[1]+1] = 0
                    field[posShadow[0]-1][posShadow[1]] = MINO_DICT[curMino]
                    field[posShadow[0]-1][posShadow[1]-1] = MINO_DICT[curMino]
                    field[posShadow[0]][posShadow[1]] = MINO_DICT[curMino]
                    field[posShadow[0]][posShadow[1]+1] = MINO_DICT[curMino]
                    ghostField[posShadow[0]-1][posShadow[1]] = MINO_DICT[curMino]
                    ghostField[posShadow[0]-1][posShadow[1]-1] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]+1] = MINO_DICT[curMino]

                elif curMino == 'L':
                    field[curPos[0]-1][curPos[1]+1] = 0
                    field[curPos[0]][curPos[1]-1] = 0
                    field[curPos[0]][curPos[1]] = 0
                    field[curPos[0]][curPos[1]+1] = 0
                    field[posShadow[0]-1][posShadow[1]+1] = MINO_DICT[curMino]
                    field[posShadow[0]][posShadow[1]-1] = MINO_DICT[curMino]
                    field[posShadow[0]][posShadow[1]] = MINO_DICT[curMino]
                    field[posShadow[0]][posShadow[1]+1] = MINO_DICT[curMino]
                    ghostField[posShadow[0]-1][posShadow[1]+1] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]-1] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]+1] = MINO_DICT[curMino]

                elif curMino == 'J':
                    field[curPos[0]-1][curPos[1]-1] = 0
                    field[curPos[0]][curPos[1]-1] = 0
                    field[curPos[0]][curPos[1]] = 0
                    field[curPos[0]][curPos[1]+1] = 0
                    field[posShadow[0]-1][posShadow[1]-1] = MINO_DICT[curMino]
                    field[posShadow[0]][posShadow[1]-1] = MINO_DICT[curMino]
                    field[posShadow[0]][posShadow[1]] = MINO_DICT[curMino]
                    field[posShadow[0]][posShadow[1]+1] = MINO_DICT[curMino]
                    ghostField[posShadow[0]-1][posShadow[1]-1] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]-1] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]+1] = MINO_DICT[curMino]

                elif curMino == 'O':
                    field[curPos[0]-1][curPos[1]] = 0
                    field[curPos[0]-1][curPos[1]+1] = 0
                    field[curPos[0]][curPos[1]] = 0
                    field[curPos[0]][curPos[1]+1] = 0
                    field[posShadow[0]-1][posShadow[1]] = MINO_DICT[curMino]
                    field[posShadow[0]-1][posShadow[1]+1] = MINO_DICT[curMino]
                    field[posShadow[0]][posShadow[1]] = MINO_DICT[curMino]
                    field[posShadow[0]][posShadow[1]+1] = MINO_DICT[curMino]
                    ghostField[posShadow[0]-1][posShadow[1]] = MINO_DICT[curMino]
                    ghostField[posShadow[0]-1][posShadow[1]+1] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]+1] = MINO_DICT[curMino]

                elif curMino == 'I':
                    field[curPos[0]][curPos[1]-1] = 0
                    field[curPos[0]][curPos[1]] = 0
                    field[curPos[0]][curPos[1]+1] = 0
                    field[curPos[0]][curPos[1]+2] = 0
                    field[posShadow[0]][posShadow[1]-1] = MINO_DICT[curMino]
                    field[posShadow[0]][posShadow[1]] = MINO_DICT[curMino]
                    field[posShadow[0]][posShadow[1]+1] = MINO_DICT[curMino]
                    field[posShadow[0]][posShadow[1]+2] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]-1] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]+1] = MINO_DICT[curMino]
                    ghostField[posShadow[0]][posShadow[1]+2] = MINO_DICT[curMino]

                hardDropFlag = False
                curMino, curPos, curRot = NextMino()

        if len(minoQueue) < 4:
            for i in NextMinoQueue():
                minoQueue.append(i)

        for i in range(4):
            screen.blit(imageMino[MINO_DICT[minoQueue[i]]], (510, 110 + 130 * i))

        for i in range(4, 25):
            for j in range(10):
                if field[i][j] != 0:
                    screen.blit(imageBlock[field[i][j]], (180 + 30 * j, 50 + 30 * (i - 4)))

        moveDelay = moveDelay - 1 if moveDelay > 0 else 0
        dropDelay = dropDelay - 1 if dropDelay > 0 else 0
        print(curMino, curPos, curRot, minoQueue, moveDelay, dropDelay)
        pygame.display.flip()

    pygame.quit()

