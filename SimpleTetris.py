import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *
import random
import time
from SimpleTetrisConstant import *
from SimpleTetrisGame import SimpleTetrisGame
from SimpleTetrisHelper import *

#TODO multiplayer

if __name__ == "__main__":
    #ANCHOR - INIT
    pygame.init()

    size = [1280, 720]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Simple Tetris")

    done = False
    clock = pygame.time.Clock()

    singlePlayFlag = False
    multiPlayFlag = False
    menuFlag = True

    #ANCHOR - Load images
    imageBackground = pygame.image.load(resource_path(IMAGE_BACKGROUND))
    imageMenu = pygame.image.load(resource_path(IMAGE_MENU))
    imageGameOver = pygame.image.load(resource_path(IMAGE_GAMEOVER))
    imageCombo = pygame.image.load(resource_path(IMAGE_COMBO))
    imageLine = pygame.image.load(resource_path(IMAGE_LINE))
    imageNum = []
    for i in range(10):
        imageNum.append(pygame.image.load(resource_path(IMAGE_NUM[i])))
    imageButton = []
    for i in range(6):
        imageButton.append(pygame.image.load(resource_path(IMAGE_BUTTON[i])))
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
    imageClear = []
    for i in range(11):
        imageClear.append(pygame.image.load(resource_path(IMAGE_CLEAR[i])))

    while not done:
        #SECTION - Menu Block
        if menuFlag:
            singleOver = False
            multiOver = False
            exitOver = False
        while menuFlag:
            clock.tick(60)

            #ANCHOR - Pygame event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    menuFlag = False
                #MouseOver
                elif event.type == pygame.MOUSEMOTION:
                    if event.pos[0] >= 74 and event.pos[0] <= 518:
                        #SinglePlay button
                        if event.pos[1] >= 277 and event.pos[1] <= 398:
                            singleOver = True
                            multiOver = False
                            exitOver = False
                        #MultiPlay button
                        elif event.pos[1] >= 423 and event.pos[1] <= 544:
                            singleOver = False
                            multiOver = True
                            exitOver = False
                        #Exit button
                        elif event.pos[1] >= 569 and event.pos[1] <= 690:
                            singleOver = False
                            multiOver = False
                            exitOver = True
                        else:
                            singleOver = False
                            multiOver = False
                            exitOver = False
                    else:
                        singleOver = False
                        multiOver = False
                        exitOver = False
                #MouseClick
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if event.pos[0] >= 74 and event.pos[0] <= 518:
                        #SinglePlay button
                        if event.pos[1] >= 277 and event.pos[1] <= 398:
                            singlePlayFlag = True
                            menuFlag = False
                        #MultiPlay button
                        elif event.pos[1] >= 423 and event.pos[1] <= 544:
                            multiPlayFlag = True
                            menuFlag = False
                        #Exit button
                        elif event.pos[1] >= 569 and event.pos[1] <= 690:
                            menuFlag = False
                            done = True

            #ANCHOR - Draw screen
            screen.blit(imageMenu, (0, 0))
            if singleOver:
                screen.blit(imageButton[0], (74, 277))
            else:
                screen.blit(imageButton[1], (74, 277))
            if multiOver:
                screen.blit(imageButton[2], (74, 423))
            else:
                screen.blit(imageButton[3], (74, 423))
            if exitOver:
                screen.blit(imageButton[4], (74, 569))
            else:
                screen.blit(imageButton[5], (74, 569))

            pygame.display.flip()
        #!SECTION

        #SECTION - Single Play block
        #ANCHOR - Single Play init
        if singlePlayFlag:
            seed = int(time.time())
            print(seed)
            random.seed(seed)
            curGame = SimpleTetrisGame()
            curGame.seed = seed
        while singlePlayFlag:
            clock.tick(60)

            #ANCHOR - Pygame event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    singlePlayFlag = False

            #SECTION - Processing key input
            #ANCHOR - Shift movement
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_a]:
                curGame.moveLeft()

            elif pressed[pygame.K_d]:
                curGame.moveRight()

            elif not pressed[pygame.K_k] or not pressed[pygame.K_d]:
                curGame.moveDelay = 0

            #ANCHOR - Spin Movement
            if pressed[pygame.K_j]:
                curGame.spinCW()

            if not pressed[pygame.K_j]:
                curGame.spinCWDelay = False

            if pressed[pygame.K_l]:
                curGame.spinCCW()

            if not pressed[pygame.K_l]:
                curGame.spinCCWDelay = False

            #ANCHOR - Hold Function
            if pressed[pygame.K_k]:
                curGame.hold()

            #ANCHOR - Soft Drop
            if pressed[pygame.K_s]:
                curGame.softDrop()
                if curGame.softLockFlag == True:
                    curGame.softLockFlag = False
                    curGame.softDropFlag = True
                    curGame.lockFlag = False

            if not pressed[pygame.K_s]:
                curGame.softDropDelay = 0
                if curGame.lockFlag == True:
                    curGame.lockFlag = False
                    curGame.softLockFlag = True

            #ANCHOR - Hard Drop
            if pressed[pygame.K_SPACE]:
                curGame.hardDrop()

            if not pressed[pygame.K_SPACE]:
                curGame.hardDropDelay = 0
            #!SECTION

            curGame.shadowCalc()
            
            #SECTION - Draw Screen
            #ANCHOR - BG
            screen.blit(imageBackground, (0, 0))

            #ANCHOR - Shadow Mino
            if curGame.clearDelay == 0:
                if curGame.curMino == 'I':
                    screen.blit(pygame.transform.rotate(imageShadow[MINO_DICT[curGame.curMino]],
                                                        SHADOW_ROTATION[curGame.rotShadow][0]),
                                (180 + 30 * (curGame.posShadow[1] - 1 + SHADOW_ROTATION_I[curGame.rotShadow][1][1]),
                                50 + 30 * (curGame.posShadow[0] - 5 + SHADOW_ROTATION_I[curGame.rotShadow][1][0])))
                elif curGame.curMino == 'O':
                    screen.blit(imageShadow[MINO_DICT[curGame.curMino]],
                                (180 + 30 * (curGame.posShadow[1] - 0), 50 + 30 * (curGame.posShadow[0] - 5)))
                else:
                    screen.blit(pygame.transform.rotate(imageShadow[MINO_DICT[curGame.curMino]],
                                                        SHADOW_ROTATION[curGame.rotShadow][0]),
                                (180 + 30 * (curGame.posShadow[1] - 1 + SHADOW_ROTATION[curGame.rotShadow][1][1]),
                                50 + 30 * (curGame.posShadow[0] - 5 + SHADOW_ROTATION[curGame.rotShadow][1][0])))
            
            curGame.tick()

            #ANCHOR - Cleared line
            if curGame.lastLineClearedDelay > 0:
                if curGame.recentComboCount > 1:
                    screen.blit(imageCombo, (10, 345))
                    if curGame.recentComboCount // 10 > 0:
                        screen.blit(imageNum[curGame.recentComboCount // 10], (90, 395))
                    screen.blit(imageNum[curGame.recentComboCount % 10], (120, 395))
                if curGame.lastTSpinFlag == True and curGame.BTBCount == 2:
                    screen.blit(imageClear[(curGame.lastLineCleared - 1) * 3 + 2], (15, 445))
                elif curGame.lastTSpinFlag == True:
                    screen.blit(imageClear[(curGame.lastLineCleared - 1) * 3 + 1], (15, 445))
                elif curGame.lastLineCleared == 4 and curGame.BTBCount == 2:
                    screen.blit(imageClear[(curGame.lastLineCleared - 1) * 3 + 1], (15, 445))
                else:
                    screen.blit(imageClear[(curGame.lastLineCleared - 1) * 3], (15, 445))

            #ANCHOR - Total cleared line
            screen.blit(imageLine, (510, 540))
            for i, s in enumerate(numStrip(curGame.totalLineCleared)):
                screen.blit(imageNum[s], (600 - 30 * i, 590))

            #ANCHOR - Next minos
            for i in range(5):
                screen.blit(imageNextMino[MINO_DICT[curGame.minoQueue[i]]], (510 + 10, 110 + 10 + 90 * i))

            #ANCHOR - Hold mino
            if curGame.curHold != 0:
                size = imageMino[MINO_DICT[curGame.curHold]].get_rect().size
                screen.blit(imageMino[MINO_DICT[curGame.curHold]], (100 - size[0] // 2, 175 - size[1] // 2))

            if curGame.holdFlag:
                s = pygame.Surface((130, 130), pygame.SRCALPHA)
                s.fill((0, 0, 0, 128))
                screen.blit(s, (35, 110))

            #ANCHOR - Field
            for i in range(4, 25):
                for j in range(10):
                    if curGame.field[i][j] != 0:
                        screen.blit(imageBlock[curGame.field[i][j]], (180 + 30 * j, 50 + 30 * (i - 4)))

            if curGame.gameOverFlag:
                singlePlayFlag = False
                menuFlag = True
                screen.blit(imageGameOver, (205, 200))
                pygame.display.flip()
                delay = 60 * 3
                flag = True
                while flag:
                    clock.tick(60)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            done = True
                            singlePlayFlag = False
                            flag = False
                        if event.type == pygame.KEYUP and delay == 0:
                            flag = False
                    delay = delay - 1 if delay > 0 else 0
            # print(curGame.curMino, curGame.curPos, curGame.curRot, curGame.moveDelay, curGame.softDropDelay, curGame.hardDropDelay)
            pygame.display.flip()
            #!SECTION
        #!SECTION

        #SECTION - Multi play block
        while multiPlayFlag:
            clock.tick(60)
            multiPlayFlag = False
            menuFlag = True
        #!SECTION

    pygame.quit()

