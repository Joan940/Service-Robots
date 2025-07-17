import sys
import pygame
import Modules.varGlobals as varGlobals

from Modules.communication import (
    runCom,
    send
)
from Modules.colors import colors as cc, tts


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
        # print("run")
        # data[0] = 200
        # data[1] = 2
        # send(data)
        simulation()

    elif text == "back":
        mainMenu()

    elif text == "configuration":
        print("configuration")
        configuration()

    elif text == "save":
        print("save")
        runCom()
        mainMenu()

    elif text == "exit":
        sys.exit(0)


###################################################################################################
#                                        TEXT ACTION MENU                                         #
###################################################################################################

def fillText(inp_key, inputUser_rects):

    while True:
        
        varGlobals.screen.blit(varGlobals.bgConfig, (0, 0))

        pygame.draw.rect(varGlobals.screen, cc.FTEK2, inputUser_rects['Save'], 3, border_radius=20)
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
                pygame.draw.rect(varGlobals.screen, cc.FTEK2, rect, 5, border_radius = 20)
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
                pygame.draw.rect(varGlobals.screen, cc.FTEK2, buttons[button], 5, border_radius = 20)
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 60)
                if click:
                    pencetButton(button)
            else:
                pygame.draw.rect(varGlobals.screen, cc.FTEK2, buttons[button], 3, border_radius = 20)
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
    varGlobals.screen.blit(varGlobals.bgSim, (0, 0))

    # SET UP POSISI TEXT
    X = varGlobals.screen.get_width()
    Y = varGlobals.screen.get_height()

    # POSISI TEXT
    BACK = pygame.Rect(X -200, Y - 1060, 180, 130)

    buttons = {
        "Back" : BACK
    }

    while varGlobals.runSim:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runMenu = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                click = True

        # LOGIKA TOMBOL
        mx, my = pygame.mouse.get_pos()

        varGlobals.screen.blit(varGlobals.bgSim, (0, 0))

        for button in buttons:
            if buttons[button].collidepoint(mx, my):
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 40)
                if click:
                    pencetButton(button)
            else:
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 30)

        click = False
        pygame.display.flip()
        varGlobals.clock.tick(60)

mainMenu()