import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *
import pygame.freetype
import random
from socket import *
import threading
import time
from SimpleTetrisConstant import *
from SimpleTetrisGame import SimpleTetrisGame
from SimpleTetrisHelper import *
from SimpleTetrisClient import SimpleTetrisClient
from SimpleTetrisConfig import SimpleTetrisConfig

#TODO multiplayer

if __name__ == "__main__":
    #ANCHOR - INIT
    pygame.init()

    size = [1280, 720]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Simple Tetris")
    GAME_FONT = pygame.freetype.SysFont("Arial", 24)
    GAME_FONT.antialiased = True

    done = False
    clock = pygame.time.Clock()
    
    config = SimpleTetrisConfig()

    singlePlayFlag = False
    multiPlayFlag = False
    settingFlag = False
    menuFlag = True

    #ANCHOR - Load images
    imageBackground = pygame.image.load(resource_path(IMAGE_BACKGROUND))
    imageBackgroundMulti = pygame.image.load(resource_path(IMAGE_BACKGROUND_MULTI))
    imageMenu = pygame.image.load(resource_path(IMAGE_MENU))
    imageGameOver = pygame.image.load(resource_path(IMAGE_GAMEOVER))
    imageCombo = pygame.image.load(resource_path(IMAGE_COMBO))
    imageLine = pygame.image.load(resource_path(IMAGE_LINE))
    imageWin = pygame.image.load(resource_path(IMAGE_WIN))
    imageNum = []
    for i in range(10):
        imageNum.append(pygame.image.load(resource_path(IMAGE_NUM[i])))
    imageButton = []
    for i in range(8):
        imageButton.append(pygame.image.load(resource_path(IMAGE_BUTTON[i])))
    imageMino = ['']
    for i in range(1, 8):
        imageMino.append(pygame.image.load(resource_path(IMAGE_MINO[i])))
    imageNextMino = ['']
    for i in range(1, 8):
        imageNextMino.append(pygame.image.load(resource_path(IMAGE_NEXT_MINO[i])))
    imageBlock = ['']
    for i in range(1, 9):
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
            settingOver = False
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
                            settingOver = False
                        #MultiPlay button
                        elif event.pos[1] >= 423 and event.pos[1] <= 544:
                            singleOver = False
                            multiOver = True
                            exitOver = False
                            settingOver = False
                        #Exit button
                        elif event.pos[1] >= 569 and event.pos[1] <= 690:
                            singleOver = False
                            multiOver = False
                            exitOver = True
                            settingOver = False
                        else:
                            singleOver = False
                            multiOver = False
                            exitOver = False
                            settingOver = False
                    elif event.pos[0] >= 538 and event.pos[1] <= 982:
                        if event.pos[1] >= 569 and event.pos[1] <= 690:
                            singleOver = False
                            multiOver = False
                            exitOver = False
                            settingOver = True
                        else:
                            singleOver = False
                            multiOver = False
                            exitOver = False
                            settingOver = False
                    else:
                        singleOver = False
                        multiOver = False
                        exitOver = False
                        settingOver = False
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
                    elif event.pos[0] >= 538 and event.pos[1] <= 982:
                        if event.pos[1] >= 569 and event.pos[1] <= 690:
                            menuFlag = False
                            settingFlag = True

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
            if settingOver:
                screen.blit(imageButton[6], (538, 569))
            else:
                screen.blit(imageButton[7], (538, 569))

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
            if pressed[config.key_Left]:
                curGame.moveLeft()

            elif pressed[config.key_Right]:
                curGame.moveRight()

            elif not pressed[config.key_Left] or not pressed[config.key_Right]:
                curGame.moveDelay = 0

            #ANCHOR - Spin Movement
            if pressed[config.key_SpinCW]:
                curGame.spinCW()

            if not pressed[config.key_SpinCW]:
                curGame.spinCWDelay = False

            if pressed[config.key_SpinCCW]:
                curGame.spinCCW()

            if not pressed[config.key_SpinCCW]:
                curGame.spinCCWDelay = False

            #ANCHOR - Hold Function
            if pressed[config.key_Hold]:
                curGame.hold()

            #ANCHOR - Soft Drop
            if pressed[config.key_SoftDrop]:
                curGame.softDrop()
                if curGame.softLockFlag == True:
                    curGame.softLockFlag = False
                    curGame.softDropFlag = True
                    curGame.lockFlag = False

            if not pressed[config.key_SoftDrop]:
                curGame.softDropDelay = 0
                if curGame.lockFlag == True:
                    curGame.lockFlag = False
                    curGame.softLockFlag = True

            #ANCHOR - Hard Drop
            if pressed[config.key_HardDrop]:
                curGame.hardDrop()

            if not pressed[config.key_HardDrop]:
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
        if multiPlayFlag:
            networkManager = SimpleTetrisClient(config.server_ip)
            txt = ["Connecting..."]
            while not networkManager.ready:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                        multiPlayFlag = False
                        networkManager.ready = True

                if networkManager.logFlag > 0:
                    networkManager.lock.acquire()
                    txt.append(networkManager.log.get())
                    networkManager.logFlag -= 1
                    networkManager.lock.release()
                    if len(txt) > 10:
                        txt.pop(0)

                screen.fill((0, 0, 0))
                for i, t in enumerate(txt):
                    GAME_FONT.render_to(screen, (10, 10 + 24  * i), t, (255, 255, 255))

                pygame.display.flip()

            seed = networkManager.seed
            print(seed)
            random.seed(seed)
            curGame = SimpleTetrisGame(multiPlay = True)
            curGame.seed = seed

        while multiPlayFlag:
            clock.tick(60)

            #ANCHOR - Pygame event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    multiPlayFlag = False

            #SECTION - Processing key input
            #ANCHOR - Shift movement
            pressed = pygame.key.get_pressed()
            if pressed[config.key_Left]:
                curGame.moveLeft()

            elif pressed[config.key_Right]:
                curGame.moveRight()

            elif not pressed[config.key_Left] or not pressed[config.key_Right]:
                curGame.moveDelay = 0

            #ANCHOR - Spin Movement
            if pressed[config.key_SpinCW]:
                curGame.spinCW()

            if not pressed[config.key_SpinCW]:
                curGame.spinCWDelay = False

            if pressed[config.key_SpinCCW]:
                curGame.spinCCW()

            if not pressed[config.key_SpinCCW]:
                curGame.spinCCWDelay = False

            #ANCHOR - Hold Function
            if pressed[config.key_Hold]:
                curGame.hold()

            #ANCHOR - Soft Drop
            if pressed[config.key_SoftDrop]:
                curGame.softDrop()
                if curGame.softLockFlag == True:
                    curGame.softLockFlag = False
                    curGame.softDropFlag = True
                    curGame.lockFlag = False

            if not pressed[config.key_SoftDrop]:
                curGame.softDropDelay = 0
                if curGame.lockFlag == True:
                    curGame.lockFlag = False
                    curGame.softLockFlag = True

            #ANCHOR - Hard Drop
            if pressed[config.key_HardDrop]:
                curGame.hardDrop()

            if not pressed[config.key_HardDrop]:
                curGame.hardDropDelay = 0
            #!SECTION

            curGame.shadowCalc()

            #SECTION - Draw Screen
            #ANCHOR - BG
            screen.blit(imageBackgroundMulti, (0, 0))

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

            networkManager.sendData(curGame.zipData())

            #ANCHOR - attack line
            attack = 0
            if curGame.lastLineClearedDelay == 30:
                attack += min(curGame.recentComboCount // 2, 5)
                if curGame.lastTSpinFlag:
                    attack += curGame.lastLineCleared * 2
                else:
                    attack += curGame.lastLineCleared - 1
                if curGame.lastLineCleared == 4:
                    attack += 1
                if curGame.BTBCount == 2:
                    attack += 1

            if attack > 0:
                networkManager.sendData('ATTACK' + str(attack))
            
            #ANCHOR - attacked line
            networkManager.lock.acquire()
            attacked = len(networkManager.attackQueue) > 0
            networkManager.lock.release()
            if curGame.getMinoFlag and attacked:
                networkManager.lock.acquire()
                line = networkManager.attackQueue.pop(0)
                networkManager.lock.release()
                curGame.newLine(line)
            curGame.getMinoFlag = False
                
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
            
            networkManager.lock.acquire()
            f = 0
            for i, n in enumerate(networkManager.attackQueue):
                a = pygame.Surface((6, 30 * n - 4), pygame.SRCALPHA)
                a.fill((255 if i == 0 else 0, 255 if i != 0 else 0, 255 if i != 0 else 0, 255))
                f += n
                screen.blit(a, (168, 680 - 30 * f + 4))
            networkManager.lock.release()

            #ANCHOR - Field
            for i in range(4, 25):
                for j in range(10):
                    if curGame.field[i][j] != 0:
                        screen.blit(imageBlock[curGame.field[i][j]], (180 + 30 * j, 50 + 30 * (i - 4)))

            #ANCHOR - OppoField
            networkManager.lock.acquire()
            for i in range(4, 25):
                for j in range(10):
                    if networkManager.oppoField[i][j] != 0:
                        screen.blit(imageBlock[networkManager.oppoField[i][j]], (800 + 30 * j, 50 + 30 * (i - 4)))
            networkManager.lock.release()
            
            networkManager.lock.acquire()
            winFlag = networkManager.winFlag
            networkManager.lock.release()
            
            if curGame.gameOverFlag:
                print('YOULOSE')
                networkManager.sendData('YOUWIN')
                multiPlayFlag = False
                menuFlag = True
                screen.blit(imageGameOver, (205, 200))
                pygame.display.flip()
                delay = 60 * 3
                flag = True
                networkManager.close()
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
            if winFlag:
                multiPlayFlag = False
                menuFlag = True
                screen.blit(imageWin, (205, 200))
                pygame.display.flip()
                delay = 60 * 3
                flag = True
                networkManager.close()
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
        
        #SECTION - Setting Block
        if settingFlag:
            waitingInput = [False] * 7
            exitOver = False
            txt = [' Left : ' + pygame.key.name(config.key_Left),
                   ' Right : ' + pygame.key.name(config.key_Right),
                   ' Soft Drop : ' + pygame.key.name(config.key_SoftDrop),
                   ' Hard Drop : ' + pygame.key.name(config.key_HardDrop),
                   ' Hold : ' + pygame.key.name(config.key_Hold),
                   ' Spin CW : ' + pygame.key.name(config.key_SpinCW),
                   ' Spin CCW : ' + pygame.key.name(config.key_SpinCCW),]
        while settingFlag:
            clock.tick(60)

            #ANCHOR - Pygame event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    settingFlag = False
                #MouseOver
                elif event.type == pygame.MOUSEMOTION:
                    if not any(waitingInput):
                        for i in range(7):
                            if event.pos[1] >= 10 + 24 * i and event.pos[1] < 10 + 24 * (i + 1):
                                txt[i] = '>' + txt[i][1:]
                            else:
                                txt[i] = ' ' + txt[i][1:]
                        if event.pos[0] >= 74 and event.pos[0] <= 518:
                            if event.pos[1] >= 569 and event.pos[1] <= 690:
                                exitOver = True
                            else:
                                exitOver = False
                        else:
                            exitOver = False
                #MouseClick
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not any(waitingInput):
                        for i in range(7):
                            if event.pos[1] >= 10 + 24 * i and event.pos[1] < 10 + 24 * (i + 1):
                                waitingInput[i] = True
                        if event.pos[0] >= 74 and event.pos[0] <= 518:
                            #Exit button
                            if event.pos[1] >= 569 and event.pos[1] <= 690:
                                settingFlag = False
                                menuFlag = True
                                
            if any(waitingInput):
                key_ = -1
                pressed = pygame.key.get_pressed()
                for i, state in enumerate(pressed):
                    if state:
                        key_ = i
                        break
                if key_ != -1:
                    if waitingInput[0]:
                        config.key_Left = key_
                        config.writeConfig()
                        waitingInput[0] = False
                        txt[0] = '>Left : ' + pygame.key.name(config.key_Left)
                    elif waitingInput[1]:
                        config.key_Right = key_
                        config.writeConfig()
                        waitingInput[1] = False
                        txt[1] = '>Right : ' + pygame.key.name(config.key_Right)
                    elif waitingInput[2]:
                        config.key_SoftDrop = key_
                        config.writeConfig()
                        waitingInput[2] = False
                        txt[2] = '>SoftDrop : ' + pygame.key.name(config.key_SoftDrop)
                    elif waitingInput[3]:
                        config.key_HardDrop = key_
                        config.writeConfig()
                        waitingInput[3] = False
                        txt[3] = '>HardDrop : ' + pygame.key.name(config.key_HardDrop)
                    elif waitingInput[4]:
                        config.key_Hold = key_
                        config.writeConfig()
                        waitingInput[4] = False
                        txt[4] = '>Hold : ' + pygame.key.name(config.key_Hold)
                    elif waitingInput[5]:
                        config.key_SpinCW = key_
                        config.writeConfig()
                        waitingInput[5] = False
                        txt[5] = '>Spin CW : ' + pygame.key.name(config.key_SpinCW)
                    elif waitingInput[6]:
                        config.key_SpinCCW = key_
                        config.writeConfig()
                        waitingInput[6] = False
                        txt[6] = '>Spin CCW : ' + pygame.key.name(config.key_SpinCCW)

            #ANCHOR - Draw screen
            screen.fill((0, 0, 0))
            for i, t in enumerate(txt):
                GAME_FONT.render_to(screen, (10, 10 + 24  * i), t, (255, 255, 255))
            if exitOver:
                screen.blit(imageButton[4], (74, 569))
            else:
                screen.blit(imageButton[5], (74, 569))

            pygame.display.flip()
        #!SECTION

    pygame.quit()

