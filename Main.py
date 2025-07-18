import sys
import pygame
import Modules.dataRobot as dataRobot
import Modules.varGlobals as varGlobals

from Modules.communication import (
    runCom,
    send
)
from Skills.demoMode import (
    demo1
)
from Modules.algorithm import (
    rotatedImage
)
from Modules.colors import custom as cc, tts


###################################################################################################
#                            VARIABLE GLOBAL YANG DIINISIALISASI DIAWAL                           #
###################################################################################################

varGlobals.IP = '127.0.0.1'
varGlobals.PORT = '8081'


###################################################################################################
#                                          PRESS BUTTON                                           #
###################################################################################################

def pencetButton(text):

    data = bytearray(3)

    # PAKSA HURUF KECIL
    text = text.lower()
    if text == "run":
        simulation()

    elif text == "back":
        # mainMenu()
        sys.exit(0)

    elif text == "configuration":
        print("configuration")
        configuration()

    elif text == "save":
        print("save")
        runCom()
        mainMenu()

    elif text == "demo 1":
        demo1()

    elif text == "exit":
        sys.exit(0)


###################################################################################################
#                                        TEXT ACTION MENU                                         #
###################################################################################################

def fillText(inp_key, inputUser_rects):

    while True:
        
        varGlobals.screen.blit(varGlobals.bgConfig, (0, 0))

        pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, inputUser_rects['Save'], 3, border_radius=20)
        tts("Save", cc.RED_BROWN, inputUser_rects['Save'], varGlobals.screen, 50)
       
        for key, rect in inputUser_rects.items():
            if key in ["IP", "PORT"]:
                current_value = ""
                if key == "IP":
                    current_value = varGlobals.IP
                elif key == "PORT":
                    current_value = varGlobals.PORT
                
                if key == inp_key:
                    pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius = 20)
                    tts(current_value, cc.WHITE, rect, varGlobals.screen, 60)
                else:
                    pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 3, border_radius = 20)
                    tts(current_value, cc.RED_BROWN, rect, varGlobals.screen, 50)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if inp_key == "IP":
                        varGlobals.IP = varGlobals.IP[:-1]
                    elif inp_key == "PORT":
                        varGlobals.PORT = varGlobals.PORT[:-1]
                elif event.key == pygame.K_RETURN:
                    return
                else:
                    if inp_key == "IP":
                        varGlobals.IP += event.unicode
                    elif inp_key == "PORT":
                        if event.unicode.isdigit():
                            varGlobals.PORT += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not inputUser_rects[inp_key].collidepoint(event.pos):
                    return

        pygame.display.flip()
        varGlobals.clock.tick(120)


###################################################################################################
#                                          CONFIGURATION                                          #
###################################################################################################

def configuration():

    # BOOLEAN
    click = False
    varGlobals.runSim = False
    varGlobals.runMenu = False
    varGlobals.runConfig = True

    # WINDOW
    window_rect = pygame.Surface.get_rect(varGlobals.screen)

    # SET UP POSISI TEXT & UKURAN BUTTON
    PANJANG_BUTTON = varGlobals.res[0] * 0.094
    LEBAR_BUTTON = varGlobals.res[1] * 0.06
    PANJANG_INP_BUTTON = varGlobals.res[0] * 0.1
    LEBAR_INP_BUTTON = varGlobals.res[1] * 0.06

    # POSISI BUTTON
    SAVE_RECT = pygame.rect.Rect(window_rect.centerx - (PANJANG_BUTTON * (-1.42)),
                                 window_rect.centery - LEBAR_BUTTON * (-5),
                                 PANJANG_BUTTON * 2, LEBAR_BUTTON * 1.7)

    # POSISI INPUT USER
    INP_IP_RECT = pygame.rect.Rect(window_rect.centerx - (PANJANG_INP_BUTTON * (-0.78)),
                                   window_rect.centery - (LEBAR_INP_BUTTON * 1.66),
                                   PANJANG_INP_BUTTON * 3, LEBAR_INP_BUTTON * 1.7)
    
    INP_PORT_RECT = pygame.rect.Rect(window_rect.centerx - (PANJANG_INP_BUTTON * (-0.78)),
                                     window_rect.centery - LEBAR_INP_BUTTON * (-1.8),
                                     PANJANG_INP_BUTTON * 3, LEBAR_INP_BUTTON * 1.7)

    inputUser = {
        "Save" : SAVE_RECT,
        "IP" : INP_IP_RECT,
        "PORT" : INP_PORT_RECT
    }

    while varGlobals.runConfig:
        varGlobals.screen.blit(varGlobals.bgConfig, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runConfig = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                click = True

        mx, my = pygame.mouse.get_pos()

        for key, rect in inputUser.items():
            display_text = key
            if key == "IP":
                display_text = varGlobals.IP
            elif key == "PORT":
                display_text = varGlobals.PORT
            
            if rect.collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 5, border_radius = 20)
                tts(display_text, cc.RED_BROWN, rect, varGlobals.screen, 60)
                if click:
                    if key in ["IP", "PORT"]:
                        fillText(key, inputUser)
                    elif key == "Save":
                        pencetButton(key)
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 3, border_radius = 20)
                tts(display_text, cc.RED_BROWN, rect, varGlobals.screen, 50)

        click = False
        varGlobals.clock.tick(120)
        pygame.display.flip()


###################################################################################################
#                                            MAIN MENU                                            #
###################################################################################################

def mainMenu():

    # BOOLEAN
    click = False
    varGlobals.runSim = False
    varGlobals.runMenu = True
    varGlobals.runConfig = False

    # WINDOW
    window_rect = pygame.Surface.get_rect(varGlobals.screen)
    mainClock = pygame.time.Clock()

    # SET UP POSISI TEXT & UKURAN BUTTON
    PANJANG_BUTTON = varGlobals.res[0] * 0.1
    LEBAR_BUTTON = varGlobals.res[1] * 0.06
    PANJANG_STATUS = varGlobals.res[0] * 0.064
    LEBAR_STATUS = varGlobals.res[1] * 0.02

    # POSISI BUTTON
    RUN = pygame.rect.Rect(window_rect.centerx - (PANJANG_BUTTON * (-0.8)),
                            window_rect.centery - LEBAR_BUTTON * 2.6,
                            PANJANG_BUTTON * 3, LEBAR_BUTTON * 1.7)
    CONFIGURATION = pygame.rect.Rect(window_rect.centerx - (PANJANG_BUTTON * (-0.8)),
                            window_rect.centery - (LEBAR_BUTTON * 0.2),
                            PANJANG_BUTTON * 3, LEBAR_BUTTON * 1.7)
    EXIT = pygame.rect.Rect(window_rect.centerx - (PANJANG_BUTTON * (-0.8)),
                            window_rect.centery - (LEBAR_BUTTON * (-2.2)),
                            PANJANG_BUTTON * 3, LEBAR_BUTTON * 1.7)

    # PESAN DISCONNECT DAN CONNECTED
    STATUS = pygame.rect.Rect(window_rect.centerx - (PANJANG_STATUS * (-2.6)),
                            window_rect.centery - (LEBAR_STATUS * (-15.5)),
                            PANJANG_STATUS * 2, LEBAR_STATUS * 1.7)
    
    # BUTTON
    buttons = {
        "Run" : RUN,
        "Configuration" : CONFIGURATION,
        "Exit" : EXIT,
    }

    # STATUS
    status = {
        varGlobals.conServiceBot : STATUS
    }

    while varGlobals.runMenu:

        varGlobals.screen.blit(varGlobals.bgMenu, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runMenu = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                click = True

        # LOGIKA TOMBOL
        mx, my = pygame.mouse.get_pos()
        for button in buttons:
            if buttons[button].collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, buttons[button], 5, border_radius = 20)
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 60)
                if click:
                    pencetButton(button)
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, buttons[button], 3, border_radius = 20)
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 50)

        for myStatus in status:
            if varGlobals.serviceBot:
                varGlobals.conServiceBot = "Connected"
                pygame.draw.rect(varGlobals.screen, cc.GREEN, status[myStatus], border_radius = 20)
                tts(varGlobals.conServiceBot, cc.WHITE, status[myStatus], varGlobals.screen, 30)
            else:
                varGlobals.conServiceBot = "Disconnected"
                pygame.draw.rect(varGlobals.screen, cc.RED, status[myStatus], border_radius = 20)
                tts(varGlobals.conServiceBot, cc.WHITE, status[myStatus], varGlobals.screen, 30)

        click = False
        mainClock.tick(60)
        pygame.display.flip()

def simulation():

    # BOOLEAN
    click = False
    varGlobals.runSim = True
    varGlobals.runMenu = False
    varGlobals.runConfig = False

    # WINDOW
    window_rect = pygame.Surface.get_rect(varGlobals.screen)

    # SET UP POSISI TEXT
    X = varGlobals.screen.get_width()
    Y = varGlobals.screen.get_height()

    PANJANG_BUTTON = varGlobals.res[0] * 0.1
    LEBAR_BUTTON = varGlobals.res[1] * 0.06

    # POSISI TEXT
    BACK = pygame.rect.Rect(window_rect.centerx - (PANJANG_BUTTON * (-3.75)),
                            window_rect.centery - LEBAR_BUTTON * 7.8,
                            PANJANG_BUTTON * 1, LEBAR_BUTTON * 1.2)
    
    # SIMULASI MODE DEMO
    DEMO_1 = pygame.rect.Rect(window_rect.centerx - (PANJANG_BUTTON * (4.7)),
                            window_rect.centery - LEBAR_BUTTON * (-6.5),
                            PANJANG_BUTTON * 1.5, LEBAR_BUTTON * 1.2)
    DEMO_2 = pygame.rect.Rect(window_rect.centerx - (PANJANG_BUTTON * (3)),
                            window_rect.centery - LEBAR_BUTTON * (-6.5),
                            PANJANG_BUTTON * 1.5, LEBAR_BUTTON * 1.2)

    buttons = {
        "Back" : BACK,
        "Demo 1" : DEMO_1,
        "Demo 2" : DEMO_2
    }
    
    while varGlobals.runSim:

        infoRobot = [
            ("" + str(dataRobot.kompas), (80, 30)),
            ("" + str(dataRobot.xpos), (80, 76)),
            ("" + str(dataRobot.ypos), (80, 122))
        ]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runMenu = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                click = True

        varGlobals.screen.blit(varGlobals.bgSim, (0, 0))
        
        # # COBA OFFSET
        # pygame.draw.line(varGlobals.screen, cc.RED, (0, varGlobals.offsetY), (varGlobals.res[0], varGlobals.offsetY), 2)
        # pygame.draw.line(varGlobals.screen, cc.RED, (varGlobals.offsetX, 0), (varGlobals.offsetX, varGlobals.res[1]), 2)

        # LOGIKA TOMBOL
        mx, my = pygame.mouse.get_pos()
        for button in buttons:
            if buttons[button].collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, buttons[button], 5, border_radius = 20)
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 60)
                if click:
                    pencetButton(button)
            else:
                pygame.draw.rect(varGlobals.screen, cc.FTEK2, buttons[button], 3, border_radius = 20)
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 50)

        # for text_line, pos in infoRobot:
        #     tts(text_line, cc.RED_BROWN, pygame.Rect(pos[0], pos[1], 10, 10), varGlobals.screen, 30)
        
        # ROTASI IMAGE
        Xbot = varGlobals.offsetX + (dataRobot.ypos * varGlobals.skala) - varGlobals.offsetResetPosX
        Ybot = varGlobals.offsetY + (dataRobot.xpos * varGlobals.skala) - varGlobals.offsetResetPosY
        rotatedImage(varGlobals.bot, Xbot, Ybot, dataRobot.kompas + 90)
        rotatedImage(varGlobals.arrow, 1185, 275, dataRobot.kompas)

        click = False
        pygame.display.flip()
        varGlobals.clock.tick(60)

simulation()