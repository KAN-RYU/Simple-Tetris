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
    
    singlePlayFlag = False
    multiPlayFlag = False
    menuFlag = True

    imageBackground = pygame.image.load(resource_path(BACKGROUND))
    imageMenu = pygame.image.load(resource_path(IMAGE_MENU))
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
        
    while not done:
        #Menu Block
        if menuFlag:
            singleOver = False
            multiOver = False
            exitOver = False
        while menuFlag:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    menuFlag = False
                elif event.type == pygame.MOUSEMOTION:
                    if event.pos[0] >= 74 and event.pos[0] <= 518:
                        if event.pos[1] >= 277 and event.pos[1] <= 398:
                            singleOver = True
                            multiOver = False
                            exitOver = False
                        elif event.pos[1] >= 423 and event.pos[1] <= 544:
                            singleOver = False
                            multiOver = True
                            exitOver = False
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
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if event.pos[0] >= 74 and event.pos[0] <= 518:
                        if event.pos[1] >= 277 and event.pos[1] <= 398:
                            singlePlayFlag = True
                            menuFlag = False
                        elif event.pos[1] >= 423 and event.pos[1] <= 544:
                            multiPlayFlag = True
                            menuFlag = False
                        elif event.pos[1] >= 569 and event.pos[1] <= 690:
                            menuFlag = False
                            done = True
                    
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

        #Single Play block
        if singlePlayFlag:
            random.seed(42)
            curGame = SimpleTetrisGame()
        while singlePlayFlag:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    singlePlayFlag = False

            #Processing key input
            #Shift movement
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_a]:
                curGame.moveLeft()

            elif pressed[pygame.K_d]:
                curGame.moveRight()

            elif not pressed[pygame.K_k] or not pressed[pygame.K_d]:
                curGame.moveDelay = 0

            #Spin Movement
            if pressed[pygame.K_j]:
                curGame.spinCW()

            if not pressed[pygame.K_j]:
                curGame.spinCWDelay = False

            if pressed[pygame.K_l]:
                curGame.spinCCW()

            if not pressed[pygame.K_l]:
                curGame.spinCCWDelay = False

            #Hold Function
            if pressed[pygame.K_k]:
                curGame.hold()

            #Soft Drop
            if pressed[pygame.K_s]:
                curGame.softDrop()

            if not pressed[pygame.K_s]:
                curGame.softDropDelay = 0

            #Hard Drop
            if pressed[pygame.K_SPACE]:
                curGame.hardDrop()

            if not pressed[pygame.K_SPACE]:
                curGame.hardDropDelay = 0

            #Draw Screen
            screen.blit(imageBackground, (0, 0))

            curGame.shadowCalc()
            
            if curGame.clearDelay == 0:
                if curGame.curMino == 'I':
                    screen.blit(pygame.transform.rotate(imageShadow[MINO_DICT[curGame.curMino]], 
                                                        SHADOW_ROTATION[curGame.curRot][0]),
                                (180 + 30 * (curGame.posShadow[1] - 1 + SHADOW_ROTATION_I[curGame.curRot][1][1]),
                                50 + 30 * (curGame.posShadow[0] - 5 + SHADOW_ROTATION_I[curGame.curRot][1][0])))
                elif curGame.curMino == 'O':
                    screen.blit(imageShadow[MINO_DICT[curGame.curMino]], 
                                (180 + 30 * (curGame.posShadow[1] - 0), 50 + 30 * (curGame.posShadow[0] - 5)))
                else:
                    screen.blit(pygame.transform.rotate(imageShadow[MINO_DICT[curGame.curMino]], 
                                                        SHADOW_ROTATION[curGame.curRot][0]),
                                (180 + 30 * (curGame.posShadow[1] - 1 + SHADOW_ROTATION[curGame.curRot][1][1]),
                                50 + 30 * (curGame.posShadow[0] - 5 + SHADOW_ROTATION[curGame.curRot][1][0])))
            
            curGame.tick()
            
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
            
            if curGame.gameOverFlag:
                singlePlayFlag = False
                menuFlag = True
            print(curGame.curMino, curGame.curPos, curGame.curRot, curGame.moveDelay, curGame.softDropDelay, curGame.hardDropDelay)
            pygame.display.flip()

    pygame.quit()

